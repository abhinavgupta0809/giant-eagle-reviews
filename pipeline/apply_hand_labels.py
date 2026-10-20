"""Write the annotated CSV from hand labels instead of the LLM.

The Giant Eagle corpus is 164 reviews, small enough to read and label by hand, so
analysis/hand_labels.csv replaces the annotate step. The output has exactly the
columns annotate.py writes, so build_site_data reads it unchanged.
"""
from collections import Counter
import csv

from . import config
from .annotate import ANNOTATION_COLUMNS, ROOT
from .annotation_support import load_taxonomy
from .common import ScrapeError, cli


def split(text):
    return [v.strip() for v in text.split(' | ')] if text else []


def main():
    taxonomy = load_taxonomy(ROOT / 'analysis/taxonomy.json')
    with (config.DATA_DIR / 'raw_reviews.csv').open(encoding='utf-8', newline='') as handle:
        raw = list(csv.DictReader(handle))
    with (ROOT / 'analysis/hand_labels.csv').open(encoding='utf-8', newline='') as handle:
        labels = {row['review_id']: row for row in csv.DictReader(handle)}
    if set(labels) != {r['review_id'] for r in raw}:
        raise ScrapeError('Hand labels and raw reviews cover different review IDs')
    texts = Counter(r['review_text'].strip().lower() for r in raw)
    out = []
    for row in raw:
        hand = labels[row['review_id']]
        fields = dict.fromkeys(ANNOTATION_COLUMNS, '')
        values = {key: split(hand[key]) for key in ('labels', 'categories', 'competitors')}
        for key, limit in (('labels', taxonomy['max_labels']), ('categories', taxonomy['max_categories'])):
            if len(values[key]) > limit:
                raise ScrapeError(f'Too many {key} for {row["review_id"]}')
        for key in values:
            if any(v not in taxonomy[key] for v in values[key]):
                raise ScrapeError(f'Unknown {key} for {row["review_id"]}')
        sentiment = int(hand['sentiment_rating'])
        specific = bool(set(values['labels']) & set(taxonomy['specific_labels']))
        fields.update(labels=', '.join(values['labels']), categories=', '.join(values['categories']),
                      sentiment_rating=str(sentiment), language='en', needs_translation='FALSE',
                      topic=hand['topic'], competitors=', '.join(values['competitors']),
                      regression_claim=hand['regression_claim'],
                      rating_mismatch='TRUE' if abs(int(row['rating']) - sentiment) >= taxonomy['mismatch_threshold'] else 'FALSE',
                      is_low_signal='FALSE' if specific else 'TRUE',
                      is_duplicate_text='TRUE' if texts[row['review_text'].strip().lower()] > 1 else 'FALSE',
                      is_truncated='FALSE')
        out.append({**{k: row[k] for k in config.COLUMNS}, **fields})
    target = config.DATA_DIR / 'annotated_reviews.csv'
    with target.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=[*config.COLUMNS, *ANNOTATION_COLUMNS])
        writer.writeheader()
        writer.writerows(out)
    print(f'Wrote {len(out)} hand-labeled reviews to {target}')


if __name__ == '__main__':
    cli(main)
