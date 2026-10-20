"""Annotate through the Message Batches API (half price, runs in parallel).

Writes into the same cache as annotate.py, so afterwards `python -m pipeline.annotate --yes` only
retries what failed here and writes the CSV. Usage:
    python -m pipeline.annotate_batch --dry-run
    python -m pipeline.annotate_batch submit --yes --max-cost 10
    python -m pipeline.annotate_batch collect      # repeat until every batch has ended
"""
import argparse
from decimal import Decimal
import json
import os
from pathlib import Path

import anthropic
from dotenv import load_dotenv

from . import config
from .annotate import (
    ROOT, approximate_tokens, build_plan, cache_key, cache_lock, cost_limit, dry_estimate,
    load_cache, load_raw, append_cache, repair_cache, text_key, user_payload,
)
from .annotation_support import Usage, live_prices, load_prompt, load_taxonomy, output_schema, validate_batch
from .common import ScrapeError, atomic_text, cli

# Batch requests bill at half the standard rate.
BATCH_DISCOUNT = Decimal("0.5")
REQUESTS_PER_BATCH = 500


def client():
    load_dotenv(ROOT / ".env", override=False)
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not key:
        raise ScrapeError("ANTHROPIC_API_KEY is not set; no API calls made")
    return anthropic.Anthropic(api_key=key, max_retries=3, timeout=120.0)


def params(batch, prompt, model, schema):
    return {
        "model": model,
        "system": [{"type": "text", "text": prompt, "cache_control": {"type": "ephemeral"}}],
        "messages": [{"role": "user", "content": json.dumps(user_payload(batch), ensure_ascii=False)}],
        "output_config": {"format": {"type": "json_schema", "schema": schema}},
        "max_tokens": min(128_000, max(1024, sum(512 + approximate_tokens(row["review_text"]) for _, row in batch))),
    }


def submit(args, prompt, taxonomy, schema):
    corpus = load_raw(args.raw)
    cache, _ = load_cache(args.cache, taxonomy)
    representatives, pending = build_plan(corpus, prompt, args.model, cache, args.limit)
    estimate = dry_estimate(corpus, representatives, pending, prompt, schema, args.model, args.batch_size, cache)
    print(f"Batch API estimate (half price): ${estimate['cost'] * float(BATCH_DISCOUNT):.4f}")
    if args.dry_run:
        print("Dry run: zero API calls; no files written")
        return
    if not args.yes:
        raise ScrapeError("Submitting batches requires --yes; no API calls made")
    if estimate["cost"] * float(BATCH_DISCOUNT) > float(args.max_cost):
        raise ScrapeError(f"Estimate exceeds --max-cost ${args.max_cost}; nothing submitted")
    if args.manifest.exists():
        raise ScrapeError(f"{args.manifest} exists; collect or remove it before submitting again")
    chunks = [pending[i:i + args.batch_size] for i in range(0, len(pending), args.batch_size)]
    sdk, manifest = client(), {"prompt_hash": cache_key(prompt, args.model, ""), "batches": {}}
    for start in range(0, len(chunks), REQUESTS_PER_BATCH):
        group = chunks[start:start + REQUESTS_PER_BATCH]
        requests = [{"custom_id": f"r{start + n}", "params": params(chunk, prompt, args.model, schema)} for n, chunk in enumerate(group)]
        batch = sdk.messages.batches.create(requests=requests)
        manifest["batches"][batch.id] = {f"r{start + n}": [key for key, _ in chunk] for n, chunk in enumerate(group)}
        print(f"Submitted {batch.id}: {len(requests)} requests", flush=True)
        with atomic_text(args.manifest) as handle:
            json.dump(manifest, handle)
    print(f"Manifest: {args.manifest}")


def collect(args, prompt, taxonomy):
    try:
        manifest = json.loads(args.manifest.read_text())
    except OSError:
        raise ScrapeError(f"No manifest at {args.manifest}") from None
    sdk, usage = client(), Usage(max_cost=Decimal("1e9"))
    prices = {tier: {name: Decimal(str(rate)) * BATCH_DISCOUNT for name, rate in rates.items()}
              for tier, rates in (config.ANNOTATION_ESTIMATE_PRICES if args.offline_prices else live_prices()).items()}
    open_batches, written, failed = 0, 0, 0
    with cache_lock(args.cache):
        cache, offset = load_cache(args.cache, taxonomy)
        repair_cache(args.cache, offset)
        for batch_id, requests in manifest["batches"].items():
            status = sdk.messages.batches.retrieve(batch_id)
            counts = status.request_counts
            print(f"{batch_id}: {status.processing_status}; succeeded={counts.succeeded} errored={counts.errored} processing={counts.processing}", flush=True)
            if status.processing_status != "ended":
                open_batches += 1
                continue
            for item in sdk.messages.batches.results(batch_id):
                keys = requests[item.custom_id]
                if item.result.type != "succeeded":
                    failed += len(keys)
                    continue
                message = item.result.message
                usage.add(message.usage, prices)
                if message.stop_reason != "end_turn":
                    failed += len(keys)
                    continue
                try:
                    payload = json.loads("".join(block.text for block in message.content if block.type == "text"))
                except ValueError:
                    failed += len(keys)
                    continue
                valid, errors = validate_batch(payload, len(keys), taxonomy)
                failed += len(errors)
                for i, result in valid.items():
                    digest = cache_key(prompt, args.model, keys[i])
                    if digest not in cache:
                        append_cache(args.cache, digest, result)
                        cache[digest] = result
                        written += 1
    usage.summary()
    print(f"New cache records: {written}; reviews to retry with annotate.py: {failed}; batches still running: {open_batches}")


def arguments(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", nargs="?", choices=["submit", "collect"], default="submit")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--yes", action="store_true")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--offline-prices", action="store_true")
    parser.add_argument("--max-cost", type=cost_limit, default=Decimal("5.00"), metavar="USD")
    parser.add_argument("--batch-size", type=int, default=config.ANNOTATION_BATCH_SIZE)
    parser.add_argument("--model", default=config.ANNOTATION_MODEL, choices=[config.ANNOTATION_MODEL])
    parser.add_argument("--raw", type=Path, default=config.DATA_DIR / "raw_reviews.csv")
    parser.add_argument("--cache", type=Path, default=config.DATA_DIR / "interim/annotations.jsonl")
    parser.add_argument("--manifest", type=Path, default=config.DATA_DIR / "interim/batch_manifest.json")
    parser.add_argument("--prompt", type=Path, default=ROOT / "docs/annotation_prompt.md")
    parser.add_argument("--taxonomy", type=Path, default=ROOT / "analysis/taxonomy.json")
    return parser.parse_args(argv)


def main():
    args = arguments()
    prompt, taxonomy = load_prompt(args.prompt), load_taxonomy(args.taxonomy)
    if args.action == "collect":
        collect(args, prompt, taxonomy)
    else:
        submit(args, prompt, taxonomy, output_schema(taxonomy))


if __name__ == "__main__":
    cli(main)
