# Review volume report

Run time UTC: 2026-10-20T12:44:58Z

Window: 2025-10-20T12:44:58Z through 2026-10-20T12:44:58Z, inclusive.

Total rows before cap: 327

Total rows after cap: 327

Cap: 200000; sampling seed: 42.

Counts before cap are unique, nonempty reviews retrieved from the configured locales. They are not the total universe of store reviews: feeds can stop before the window is covered. Country is populated only for iOS and records the first storefront that returned a review, not reviewer residence. Android country is empty; store_lang records the first Play language stream that returned each review.

## By platform

| Platform | Before cap | After cap |
| --- | --- | --- |
| android | 242 | 242 |
| ios | 85 | 85 |

## iOS by storefront

| Storefront | Before cap | After cap |
| --- | --- | --- |
| us | 85 | 85 |

## Android by store_lang

| Store language | Before cap | After cap |
| --- | --- | --- |
| en | 242 | 242 |

## By UTC week (Monday start)

| Week starting | Before cap | After cap |
| --- | --- | --- |
| 2025-10-20 | 4 | 4 |
| 2025-10-27 | 15 | 15 |
| 2025-11-03 | 12 | 12 |
| 2025-11-10 | 5 | 5 |
| 2025-11-17 | 6 | 6 |
| 2025-11-24 | 8 | 8 |
| 2025-12-01 | 5 | 5 |
| 2025-12-08 | 7 | 7 |
| 2025-12-15 | 10 | 10 |
| 2025-12-22 | 2 | 2 |
| 2025-12-29 | 3 | 3 |
| 2026-01-05 | 7 | 7 |
| 2026-01-12 | 6 | 6 |
| 2026-01-19 | 11 | 11 |
| 2026-01-26 | 5 | 5 |
| 2026-02-02 | 6 | 6 |
| 2026-02-09 | 9 | 9 |
| 2026-02-23 | 6 | 6 |
| 2026-03-02 | 7 | 7 |
| 2026-03-09 | 3 | 3 |
| 2026-03-16 | 6 | 6 |
| 2026-03-23 | 10 | 10 |
| 2026-03-30 | 3 | 3 |
| 2026-04-06 | 3 | 3 |
| 2026-04-13 | 4 | 4 |
| 2026-04-20 | 5 | 5 |
| 2026-04-27 | 5 | 5 |
| 2026-05-04 | 9 | 9 |
| 2026-05-11 | 3 | 3 |
| 2026-05-18 | 5 | 5 |
| 2026-05-25 | 6 | 6 |
| 2026-06-01 | 11 | 11 |
| 2026-06-08 | 8 | 8 |
| 2026-06-15 | 6 | 6 |
| 2026-06-22 | 7 | 7 |
| 2026-06-29 | 7 | 7 |
| 2026-07-06 | 3 | 3 |
| 2026-07-13 | 4 | 4 |
| 2026-07-20 | 5 | 5 |
| 2026-07-27 | 15 | 15 |
| 2026-08-03 | 5 | 5 |
| 2026-08-10 | 4 | 4 |
| 2026-08-17 | 9 | 9 |
| 2026-08-24 | 7 | 7 |
| 2026-08-31 | 6 | 6 |
| 2026-09-07 | 8 | 8 |
| 2026-09-14 | 5 | 5 |
| 2026-09-21 | 10 | 10 |
| 2026-09-28 | 2 | 2 |
| 2026-10-05 | 4 | 4 |
| 2026-10-12 | 5 | 5 |

## By star rating per platform

| Platform | Stars | Before cap | After cap |
| --- | --- | --- | --- |
| android | 1 | 95 | 95 |
| android | 2 | 20 | 20 |
| android | 3 | 22 | 22 |
| android | 4 | 21 | 21 |
| android | 5 | 84 | 84 |
| ios | 1 | 28 | 28 |
| ios | 2 | 10 | 10 |
| ios | 3 | 9 | 9 |
| ios | 4 | 4 | 4 |
| ios | 5 | 34 | 34 |

## Review text lengths and shares

Lengths count Unicode characters in the unmodified body. Words use whitespace splitting; this is not language-aware tokenization. P90 uses linear interpolation.

| Dataset | Platform | Rows | Median chars | P90 chars | Under 4 words | Non-ASCII |
| --- | --- | --- | --- | --- | --- | --- |
| Before cap | all | 327 | 86.0 | 317.8 | 8.56% | 15.29% |
| Before cap | android | 242 | 80.0 | 314.0 | 10.33% | 6.61% |
| Before cap | ios | 85 | 102.0 | 327.0 | 3.53% | 40.00% |
| After cap | all | 327 | 86.0 | 317.8 | 8.56% | 15.29% |
| After cap | android | 242 | 80.0 | 314.0 | 10.33% | 6.61% |
| After cap | ios | 85 | 102.0 | 327.0 | 3.53% | 40.00% |

## Date ranges

| Dataset | Platform | Earliest date | Latest date |
| --- | --- | --- | --- |
| Before cap | android | 2025-10-22 | 2026-10-17 |
| Before cap | ios | 2025-10-24 | 2026-10-08 |
| After cap | android | 2025-10-22 | 2026-10-17 |
| After cap | ios | 2025-10-24 | 2026-10-08 |

Hours between run time and newest review (before cap): android: 61.59 hours; ios: 280.03 hours.

## Google Play language contributions (before cap)

| Language | Pages served | Rows fetched | In-window rows | Unique added | Overlapping IDs by first language | Same IDs as | Stop reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| en | 3 | 600 | 242 | 242 | — | — | window_edge |

## App Store pages served per storefront (before cap)

| Storefront | Pages served | Rows fetched | In-window rows | Unique added | Stop reason | Rejected page |
| --- | --- | --- | --- | --- | --- | --- |
| us | 3 | 150 | 85 | 85 | window_edge | — |

## Locales with no in-window reviews

None.
