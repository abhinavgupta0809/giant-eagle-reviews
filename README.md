# Giant Eagle app reviews + Kroger's filings

An independent, unofficial dashboard of every public Google Play (English) and US App Store review
of the main Giant Eagle app from Oct 20, 2025 to Oct 20, 2026: 327 reviews, each labeled by hand and
browsable, read next to Kroger's SEC filings on its pending acquisition of Giant Eagle. Built for a
student project on Gen Z engagement with Giant Eagle. Run 6 of a series (Perplexity, Indeed,
Claude, Wispr Flow, Snapchat, Giant Eagle). Not affiliated with Giant Eagle or Kroger.

- Site: `site/` (static HTML, CSS, JavaScript; no build step)
- Findings: `analysis/insights.json`; taxonomy: `docs/TAXONOMY.md` (categories plus the brief-area map in `analysis/taxonomy.json`)
- Labels: `analysis/hand_labels.csv` (written from `analysis/hand_labels_by_index.txt` for the first six months and `analysis/hand_labels_by_index_12mo_new.txt` for the rest; the index files use positions in the CSV they were written against); `pipeline/apply_hand_labels.py` writes `data/annotated_reviews.csv`
- Blind second pass: `analysis/gold_set.csv`; agreement in `docs/handover/02-eval.md` (97.56% primary label, 95.77% primary category)
- Filings: `analysis/kroger_metrics.json` (every quarter links to its EDGAR release) and `analysis/filings_crosswalk.json` (verbatim quotes, checked against the filing text)

Things specific to this run:

- **Small corpus, so no LLM labeling.** Six months held 164 written reviews; Abhinav widened it to 12 months, 327 reviews (242 Android, 85 iOS).
  They were read and labeled by hand instead of through `pipeline/annotate*.py`; no API spend.
  Category fade threshold is 10 reviews (not 30), versions show from 8 reviews, and the trend chart is monthly.
- **Giant Eagle is private.** The filings layer is Kroger's (agreement Jul 1, 2026; close expected fiscal 2027).
- **Play Spanish returned zero reviews** and crashes the pinned scraper, so `PLAY_LANGS` is English only.
- **Why the store says 4.5.** `analysis/store_rating.json` (from `pipeline/store_rating.py`) holds the Play and App Store listing ratings and every written Play review's stars by year; the Overview explains the gap from it.
- **Tests were not updated** for the new taxonomy; `tests/` still pins Snapchat fixtures and counts.

```sh
# Rebuild from the hand labels
.venv/bin/python -m pipeline.store_rating      # dated snapshot of store ratings and written-review stars by year
.venv/bin/python -m pipeline.apply_hand_labels
.venv/bin/python -m pipeline.evaluate --annotations data/annotated_reviews.csv
.venv/bin/python -m pipeline.build_site_data
cd site && python3 -m http.server 8766
```

## Original pipeline notes (from the Snapchat run)

```sh
.venv/bin/python -m pipeline.annotate_batch --dry-run
.venv/bin/python -m pipeline.annotate_batch submit --yes --max-cost 6
.venv/bin/python -m pipeline.annotate_batch collect     # repeat until every batch has ended
.venv/bin/python -m pipeline.annotate --yes             # retries failures, writes the CSV
.venv/bin/python -m pipeline.build_site_data
```

## Review collection

Phase 01 collects free public Google Play and App Store reviews. Python 3.11 is required.
No API key is needed for collection. Phase 02 adds annotation and gold-set evaluation;
the site build and deployment are separate phases.

```sh
python3.11 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/python -m pipeline.scrape_play
.venv/bin/python -m pipeline.scrape_appstore
.venv/bin/python -m pipeline.merge
```

`pipeline/config.py` defines application IDs, Play language and iOS storefront order, the review window,
200,000-row cap (never reached in this run), seed, page size, delays, retries, and timeouts. Dependencies,
including transitive dependencies, are pinned in `requirements.txt`.

The first scraper creates `data/run.json` with one UTC run time shared by both
scrapers and the merge. The inclusive interval ends at that time. Completed pages
are atomically checkpointed under `data/interim/.checkpoints/`. Rerunning the same
commands resumes unfinished streams and skips completed streams. Checkpoints hold
only allowlisted review fields and pagination metadata. Source JSONL files are
published only after every configured stream completes successfully; the merge
requires matching completion metadata. A zero-row source, block, unrecognized
schema, repeated page, or exhausted retry exits nonzero. Errors never log response
bodies or reviewer objects. Interruption can refetch the last uncheckpointed page
without duplicating review IDs.

For a new run, use a **fresh** directory consistently for all three commands, e.g.
`--data-dir data/2026-10-10`. Optional `--run-time 2026-10-10T12:00:00Z` sets a
reproducible run time when first creating that directory. The same directory
cannot be reused with a different run time or configuration.

Outputs:

- `data/interim/play.jsonl` and `appstore.jsonl`: normalized, sanitized reviews.
- `data/raw_reviews.csv`: the exact handover columns; review bodies are preserved
  verbatim. Empty/whitespace-only bodies are excluded. Dedupe uses prefixed review
  IDs. Android `country` is empty and `store_lang` records the first Play language
  stream that returned the ID; iOS keeps the first storefront in `country` and has
  empty `store_lang`. Play passes the fixed `PLAY_COUNTRY = "us"` to the library;
  that request parameter is not exported as review geography.
- `data/daily_true_counts.csv`: unique retrieved reviews per platform and UTC day
  **before** capping, with columns `platform,date_utc,count`.
- `data/volume_report.md`: generated counts before/after cap, text statistics,
  language/storefront contributions, feed stop reasons, and hours from run time
  to the newest retrieved review per platform before capping.

If necessary, sampling uses proportional platform/day quotas with largest
remainders, then uniform random sampling inside each group with the fixed seed.
The total is exactly the cap, and each quota differs from its ideal share by less
than one row. Results are stable even if input row order changes.

Coverage is limited to what the configured locale feeds expose. App Store feeds
can stop at a page limit before covering the whole window; an HTTP 400/404 beyond page
one is treated as a page boundary only if the previous page still succeeds.
HTTP 403/429 and server/network failures are never accepted as normal exhaustion.
Daily true counts describe the retrieved corpus, not all reviews on the stores.
Country is an iOS retrieval storefront, not reviewer residence. `store_lang` is
the Play request code, not an inferred review language. No code is replaced when
its stream is empty or duplicates another; overlap counts and identical ID sets
are recorded in the report. No review text is translated. Reviewer identity fields and developer reply text are
discarded at parse time; free-form review bodies are kept as required.

The pinned [google-play-scraper](https://github.com/JoMingyu/google-play-scraper)
suppresses exceptions in its pagination routine. A narrow adapter surfaces fetch
failures through that catch, adds request timeouts/status checks, and uses the
library's newest-first pagination and continuation tokens. Offline tests cover
that adapter so dependency changes cannot silently hide a block.

Interim data, run logs, the preserved `data.run1/`, local environments, and secrets
are gitignored. Final CSVs, the volume report, and `data/run.json` are visible to
Git for a later user-authorized commit. For the 01b configuration change, move
the phase-01 `data/` directory to `data.run1/` before running fresh; keep the backup.
All test
fixtures are synthetic, sanitized examples; pytest disables socket connections
for every test. The public endpoint may change independently of these tests.

## Annotation and evaluation (phase 02)

Copy `.env.example` to `.env` locally and set `ANTHROPIC_API_KEY` before a paid
run. Never commit or print the key. Start with the estimates:

```sh
.venv/bin/python -m pipeline.annotate --gold --dry-run
.venv/bin/python -m pipeline.annotate --dry-run
```

The dry run does not use the API or write files. It reports selected rows,
distinct normalized texts, existing cache hits, approximate tokens, and cost.
The token heuristic is UTF-8 bytes divided by three; output includes an allowance
for translation. The estimate assumes one five-minute prompt-cache write followed
by hits. Retries, cache expiration, additional thinking, and injected schema
tokens can increase actual usage. Dated prices in `pipeline/config.py` are used
only for this estimate. Paid runs fetch the current public pricing table and
print response token usage and its cost at that tariff, excluding account discounts.

```sh
.venv/bin/python -m pipeline.annotate --gold
.venv/bin/python -m pipeline.evaluate
```

Gold mode writes `data/interim/gold_annotations.csv`; the evaluator writes
`docs/handover/02-eval.md` with computed metrics, a confusion matrix, category
counts, and every label/category/low-signal disagreement. Failed annotations count
as misses; sentiment MAE is calculated over scored rows, with missing rows reported.

The prompt is loaded verbatim between the markers in `docs/annotation_prompt.md`.
Taxonomy values and limits are loaded from `analysis/taxonomy.json`. Each distinct
lowercase, whitespace-collapsed title plus body is sent once, using its first
row's star rating. Only `i`, `stars`, `title`, and `text` are sent in the user
message. `--batch-size N` changes the default 25-review request size.

Validated results are appended and flushed to `data/interim/annotations.jsonl`,
keyed by SHA-256 of prompt, model, and normalized text. Cache hits incur no API
calls; changing the prompt or configured model invalidates them. Interrupted
final cache records are discarded on resume; other corruption fails loudly.
A cache lock prevents concurrent runs from spending on the same keys. Validation
failures trigger one whole-batch retry, then one single-review fallback for each
still-invalid result. Final failures remain in the CSV with `annotation_error`;
annotation-dependent fields are empty, while duplicate/truncation flags are still
computed from the source. Authentication or exhausted transport errors stop the
run before publishing a new output, preserving validated cache entries.

`--limit N` annotates the first N uncached keys for a smoke test. The output keeps
every input row in order; uncached keys outside the limit have an explicit
`annotation_error`. All 12 source columns are retained alongside 14 annotation
columns. Gold mode retains only gold rows in source order; duplicate flags always
use the entire raw corpus.

The full run requires `--yes` and prints its estimate before proceeding. Abhinav
runs it after Claude signs off on gold agreement:

```sh
.venv/bin/python -m pipeline.annotate --yes
```

For a large corpus, split `data/raw_reviews.csv` into shards by a hash of the text key, run one
`annotate` per shard with its own `--raw`, `--cache`, and `--output`, concatenate the shard caches
into `data/interim/annotations.jsonl`, then run the main command. It finds everything cached.

## Deploy

The site is the `site/` folder: static HTML, CSS, JavaScript, and generated data, with no build step.
The Vercel project imports this GitHub repository with root directory `site`. A push to `main`
redeploys.
