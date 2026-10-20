# Phase 02 gold-set evaluation

Gold rows: 327

Rows with annotation_error: 0

## Agreement

| Metric | Matches | Rows | Value | Target | Status |
| --- | --- | --- | --- | --- | --- |
| Primary label accuracy | 317 | 327 | 96.94% | 85.00% | PASS |
| Label set overlap | 321 | 327 | 98.17% | — | — |
| Primary category agreement | 265 | 279 | 94.98% | 80.00% | PASS |
| Low-signal agreement | 44 | 48 | 91.67% | — | — |
| Sentiment within one point | 327 | 327 | 100.00% | — | — |

Sentiment mean absolute error: 0.2508 over 327 scored rows. Missing/failed sentiment rows: 0. Within-one-point accuracy uses every gold row; missing/failed results count as misses. Failed annotations also count as misses on label/category/low-signal metrics.

## Primary-label confusion matrix

| Gold primary label | Specific Praise | Specific Complaint | Feature Request | Generic Good | Generic Bad | Nonsense | (missing) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Specific Praise | 81 | 2 | 0 | 1 | 0 | 0 | 0 |
| Specific Complaint | 0 | 187 | 0 | 0 | 1 | 0 | 0 |
| Feature Request | 0 | 2 | 5 | 0 | 0 | 0 | 0 |
| Generic Good | 4 | 0 | 0 | 35 | 0 | 0 | 0 |
| Generic Bad | 0 | 0 | 0 | 0 | 8 | 0 | 0 |
| Nonsense | 0 | 0 | 0 | 0 | 0 | 1 | 0 |

## Per-category agreement

Gold count includes each row whose gold category set contains that category. A match requires the model's primary category to equal that category; a two-category gold row can appear in two denominators.

| Category | Gold count | Primary-category matches | Agreement |
| --- | --- | --- | --- |
| Login &amp; Sign-in | 42 | 38 | 90.48% |
| Checkout &amp; Payment | 38 | 29 | 76.32% |
| Crashes &amp; Speed | 48 | 37 | 77.08% |
| Shopping List &amp; Favorites | 11 | 8 | 72.73% |
| Barcode Scanner | 8 | 7 | 87.50% |
| Search &amp; Product Info | 15 | 9 | 60.00% |
| Design &amp; Navigation | 16 | 8 | 50.00% |
| Privacy &amp; Permissions | 6 | 4 | 66.67% |
| Coupons &amp; Deals | 33 | 23 | 69.70% |
| myPerks &amp; Loyalty Card | 16 | 8 | 50.00% |
| Prices &amp; Selection | 27 | 16 | 59.26% |
| Curbside Pickup | 22 | 16 | 72.73% |
| Delivery | 17 | 15 | 88.24% |
| Order Changes &amp; Time Slots | 7 | 6 | 85.71% |
| Order Quality | 10 | 5 | 50.00% |
| Support &amp; Refunds | 13 | 1 | 7.69% |
| Pharmacy | 7 | 6 | 85.71% |
| Staff &amp; Service | 37 | 18 | 48.65% |
| Saves Time &amp; Effort | 16 | 10 | 62.50% |
| Recipes &amp; Meal Ideas | 1 | 1 | 100.00% |
| Other | 2 | 0 | 0.00% |

## All label/category/low-signal disagreements (22)

Every disagreement on primary label, primary category, or low-signal agreement is included once. Text is sliced to 300 Unicode characters before Markdown escaping; no row limit is applied.

| Review ID | Stars | Review text (first 300 characters) | Gold labels | Gold categories | Model labels | Model categories | Model topic |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ios_13306053955 | 5 | Excellent Customer Service, convenience, savings, pleasant attitudes, total satisfaction | Generic Good |  | Specific Praise | Staff &amp; Service, Coupons &amp; Deals | service, convenience, savings |
| play_d284748a-52c0-495a-9e60-a5493e1898cd | 1 | As of November 1 I am unable to order in the app. I have tried uninstalling and reinstalling and on different devices but it doesn't work. I use this every week for groceries and have for years. | Specific Complaint | Crashes &amp; Speed | Specific Complaint | Checkout &amp; Payment, Crashes &amp; Speed | can't order since Nov 1 |
| ios_13379403951 | 5 | Easy shopping and they’re always on time. Customer service is friendly ,professional and proactive. | Specific Praise | Staff &amp; Service | Specific Praise | Delivery, Staff &amp; Service | on-time, friendly service |
| play_2a691da3-c57b-492f-b870-d4ad285acca8 | 5 | I love that it allows you to put notes in for substitutions!!! it's also very convenient to add items from pictures of the circular. you can use your perks points and there are online manufacturer coupons right in the app that you can use. and it goes by what's available in your store. easy to use.  | Specific Praise | Coupons &amp; Deals \| myPerks &amp; Loyalty Card | Specific Praise | Order Changes &amp; Time Slots, Coupons &amp; Deals | substitution notes, circular, coupons |
| play_9c0892f7-fc74-498b-9999-2738b17098d5 | 1 | no substitutions on alcohol. why can't I replace if you advertise you have it and you don't. poor service | Specific Complaint | Order Quality \| Search &amp; Product Info | Specific Complaint | Order Changes &amp; Time Slots | no substitutions on alcohol |
| play_f6aafbf7-c3a2-406c-8d5f-79b51e51b8e9 | 5 | I've placed weekly orders for delivery with the Giant Eagle Stelzer/McCutcheon store for years. Love the staff; they treat me like family. I know they choose the best products I ask for. This is a huge help for me since I can no longer shop in person. | Specific Praise | Staff &amp; Service \| Saves Time &amp; Effort | Specific Praise | Delivery, Staff &amp; Service | delivery staff treat me like family |
| play_867ab500-c975-4c21-8918-23afe578a86f | 5 | Very easy to navigate! | Specific Praise | Design &amp; Navigation | Generic Good |  |  |
| play_20148dcc-8971-4394-87b2-cdf5580ecb37 | 5 | Thank you! The app works again! | Generic Good |  | Specific Praise | Crashes &amp; Speed | app works again |
| play_f8f9fefe-53e0-4670-ac1f-a3b3151c18d7 | 5 | Glitch is fixed, back to loving my Giant Eagle app. | Generic Good |  | Specific Praise | Crashes &amp; Speed | glitch fixed |
| play_155e265b-d393-44d7-b932-7f94f15909e2 | 5 | Now works great👍 | Generic Good |  | Specific Praise | Crashes &amp; Speed | works again |
| ios_13669935293 | 5 | Great service quality food. | Specific Praise | Prices &amp; Selection | Specific Praise | Staff &amp; Service, Order Quality | service and food quality |
| ios_13738709931 | 1 | My app has a glitch in it when I try to access my pay direct it just tells me I changed my pin so now I can’t use it anymore, and I have tried to get Support to get this taken care of, and I can’t find help anywhere | Specific Complaint | Checkout &amp; Payment \| Support &amp; Refunds | Specific Complaint | myPerks &amp; Loyalty Card, Support &amp; Refunds | myPerks Pay PIN glitch, no support |
| play_6b54ad1c-f3a4-4052-a5aa-dc8778c5ad85 | 3 | I use the service because I am disabled. It is wonderful. the only problem I have is I try not to buy much produce using this service because the clerks do not always pick very good produce i have gotten produce that I have had to throw away the same day.It was bought. | Specific Praise \| Specific Complaint | Saves Time &amp; Effort \| Order Quality | Specific Complaint, Specific Praise | Order Quality, Saves Time &amp; Effort | disabled shopper, poorly picked produce |
| play_b101240f-9a40-42af-96f9-fbcf5e54c405 | 1 | My main issue is with the my perks pay option that Giant Eagle offers for its gas station locations. what isn't made clear is that when you purchase gas using this feature, it can take up to three business days for them to attempt to take the money out of your account and if they take it at a point  | Specific Complaint | Checkout &amp; Payment | Specific Complaint | myPerks &amp; Loyalty Card, Checkout &amp; Payment | myPerks Pay delayed charge and fee |
| play_fa11b887-66ab-4625-90a3-8e1b173c6d6d | 3 | works just too expensive for a time slot | Specific Complaint | Order Changes &amp; Time Slots | Specific Complaint | Delivery | time slot fee too high |
| play_913e22fd-1c53-437b-be08-3b63950af627 | 2 | I wanted to report that the digital coupons used to have a "food only" option. also you cannot replicate the function of "food only" filter by selecting multiple options, the other options disappear when you click 1. please put back your filtering options | Feature Request \| Specific Complaint | Coupons &amp; Deals | Specific Complaint, Feature Request | Coupons &amp; Deals | coupon food-only filter removed |
| play_5d37f8f4-c93e-4b74-aab2-d8707cc25d04 | 1 | horrible pot pies 4 peas two carrot slices loaded with throw away chicken ever day | Specific Complaint | Prices &amp; Selection | Specific Complaint | Order Quality | poor pot pie quality |
| play_bd8178bf-6392-4b5c-897a-c7d806fafafa | 3 | bring back the option to filter coupons by expiration. with the new update, the expiration dates are no longer visible anywhere, even when clicking on the coupon. this should be easy to see at a glance. | Feature Request \| Specific Complaint | Coupons &amp; Deals | Specific Complaint, Feature Request | Coupons &amp; Deals | coupon expiry filter removed |
| play_0d61fdbd-778e-4c2b-a328-4f66d361f2c7 | 4 | Every time I do delivery they never have everything you need, especially if it's on sale. | Specific Complaint | Order Quality \| Prices &amp; Selection | Specific Complaint | Delivery, Order Quality | delivery missing items, especially sale items |
| play_22271c05-6d6a-4183-83d6-1ba5d41b83a7 | 1 | Microsoft has blocked the app and on line | Specific Complaint | Other | Generic Bad |  |  |
| play_fe9aec16-477c-46aa-9d34-4055084081f7 | 4 | Good quality of inventory items, baked goods, produce, but way too pricey even with Perks | Specific Praise \| Specific Complaint | Prices &amp; Selection | Specific Complaint, Specific Praise | Prices &amp; Selection, myPerks &amp; Loyalty Card | good quality, pricey even with perks |
| ios_14633877707 | 1 | Sorry to give a bad review but I had to try five times to confirm an order pick up and the app is very slow | Specific Complaint | Crashes &amp; Speed \| Curbside Pickup | Specific Complaint | Checkout &amp; Payment, Crashes &amp; Speed | five tries to confirm pickup order |
