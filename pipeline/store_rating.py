"""Snapshot the store-listing ratings and the all-time written-review stars by year.

The dashboard reads written reviews from the last 12 months, which average far below the
rating shown on the store. This snapshot explains the gap with the stores' own numbers:
how many ratings carry text, and how written-review stars moved year by year. Only the
star, the year, and nothing about the reviewer is kept.
"""
from collections import defaultdict
from datetime import datetime, timezone
import json

import requests
from google_play_scraper import Sort, app, reviews

from . import config
from .annotate import ROOT
from .common import ScrapeError, cli


def main():
    listing = app(config.PLAY_APP_ID, lang='en', country=config.PLAY_COUNTRY)
    histogram = listing['histogram']
    stars, token = [], None
    while True:
        batch, token = reviews(config.PLAY_APP_ID, lang='en', country=config.PLAY_COUNTRY, sort=Sort.NEWEST,
                               count=config.PAGE_SIZE, continuation_token=token)
        stars += [(r['at'].year, r['score']) for r in batch]
        if not batch or not token:
            break
    if not stars:
        raise ScrapeError('Play returned no written reviews')
    years = defaultdict(list)
    for year, score in stars:
        years[year].append(score)
    response = requests.get('https://itunes.apple.com/lookup', params={'id': config.APPSTORE_ID, 'country': 'us'}, timeout=config.HTTP_TIMEOUT)
    response.raise_for_status()
    ios = response.json()['results'][0]
    snapshot = {
        'fetched_at': datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z'),
        'play': {'score': listing['score'], 'ratings': listing['ratings'], 'listed_reviews': listing.get('reviews'),
                 'histogram': histogram, 'histogram_ratings': sum(histogram),
                 'histogram_star_sum': sum((i + 1) * n for i, n in enumerate(histogram)),
                 'written': {'count': len(stars), 'star_sum': sum(s for _, s in stars),
                             'by_year': [{'year': y, 'n': len(v), 'star_sum': sum(v), 'five': v.count(5)} for y, v in sorted(years.items())]}},
        'appstore': {'score': ios['averageUserRating'], 'ratings': ios['userRatingCount']},
    }
    target = ROOT / 'analysis/store_rating.json'
    target.write_text(json.dumps(snapshot, indent=1) + '\n', encoding='utf-8')
    print(f"Play {listing['score']:.2f} from {listing['ratings']:,} ratings; {len(stars):,} written reviews; App Store {ios['averageUserRating']:.2f} from {ios['userRatingCount']:,}")


if __name__ == '__main__':
    cli(main)
