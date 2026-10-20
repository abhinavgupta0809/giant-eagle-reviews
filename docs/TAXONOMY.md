# Giant Eagle review taxonomy

Written 2026-10-20 after reading all 164 reviews (Apr 20 to Oct 20, 2026); extended the same day to 327 reviews over 12 months (Oct 20, 2025 to Oct 20, 2026), which added Recipes & Meal Ideas. The six labels carry over from earlier runs; the categories are specific to a grocery app.

## Labels (up to two, first is primary)

- **Specific Praise**: praises a named feature, service, person, or use.
- **Specific Complaint**: names a concrete problem.
- **Feature Request**: asks for something to be added, changed, or brought back.
- **Generic Good / Generic Bad**: approval or disapproval with nothing specific ("great", "terrible app").
- **Nonsense**: off-topic or unreadable.

## Categories (up to two)

| Category | Use when the review is about |
|---|---|
| Login & Sign-in | Can't log in, forced sign-outs, passkeys, password resets, email codes, "stay signed in" ignored |
| Checkout & Payment | Cart, checkout errors, payment methods failing, myPerks Pay charges, health-benefit cards |
| Crashes & Speed | Crashes, freezes, lag, timeouts, won't load, won't install |
| Shopping List & Favorites | The shopping list, favorites, "previously purchased" |
| Barcode Scanner | Camera scanning and in-store price checks |
| Search & Product Info | Search results, item availability online, item locations in store, photos, product details |
| Design & Navigation | Confusing layout, hard to navigate, ease of use as a design property |
| Privacy & Permissions | Location prompts, personal data asked for, cookies, device lock requirements |
| Coupons & Deals | Digital coupons, coupon filters and expiry dates, promo codes, sale pricing, rebates |
| myPerks & Loyalty Card | myPerks points, the Advantage/perks card, wallet and widget card display |
| Prices & Selection | Price level, brand and product range, store stock and quality as a store |
| Curbside Pickup | Ordering for pickup and the pickup experience |
| Delivery | Delivery fees, tips, bag fees, delivery partners, drop-off |
| Order Changes & Time Slots | Editing a placed order, keeping or choosing a time slot |
| Order Quality | Missing, wrong, spoiled, or poor-quality items in an order; accuracy praise |
| Support & Refunds | Contacting the company, replies, refunds |
| Pharmacy | Pharmacy features and the separate pharmacy app |
| Staff & Service | Named or described associates, shoppers, curbside staff |
| Saves Time & Effort | The app replacing a store trip: busy schedules, limited mobility, no car |
| Recipes & Meal Ideas | Recipes, meal planning, adding ingredients from a recipe |
| Other | Anything else specific |

## Fields

- `sentiment_rating` 1 to 5 from the words alone. `rating_mismatch` when stars and sentiment differ by 2 or more.
- `regression_claim` when the reviewer says it got worse ("since the update", "no longer").
- `competitors` lists other grocers or apps named. Kroger is listed when named even though it is the pending acquirer.
