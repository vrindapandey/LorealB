import requests
import pandas as pd
import time
import re


MAX_REVIEWS_PER_PRODUCT = 500
PAGE_LIMIT = 100   # max allowed by BV is usually 100
SLEEP_BETWEEN_REQUESTS = 0.5

BAZAARVOICE_ENDPOINT = "https://api.bazaarvoice.com/data/reviews.json"

PASSKEY = "calXm2DyQVjcCy9agq85vmTJv5ELuuBCF2sdg4BnJzJus"


bestsellers = ["https://www.sephora.com/product/libre-berry-crush-P520837?skuId=2919744&icid2=products%20grid:p520837:product",
               "https://www.sephora.com/product/kayali-yum-boujee-marshmallow-81-eau-de-parfum-intense-travel-spray-P512449?skuId=2804839&icid2=products%20grid:p512449:product",
               "https://www.sephora.com/product/kayali-vanilla-P439406?skuId=2163970&icid2=products%20grid:p439406:product",
               "https://www.sephora.com/product/phlur-vanilla-skin-hair-body-fragrance-mist-P509258?skuId=2693349&icid2=products%20grid:p509258:product",
               "https://www.sephora.com/product/eilish-1-eau-de-parfum-P520204?skuId=2948495&icid2=products%20grid:p520204:product",
               "https://www.sephora.com/product/libre-berry-crush-travel-spray-P520822?skuId=2919769&icid2=products%20grid:p520822:product",
               "https://www.sephora.com/product/paradoxe-eau-de-parfum-P501198?skuId=2591170&icid2=products%20grid:p501198:product",
               "https://www.sephora.com/product/donna-born-in-roma-purple-melancholia-P520824?skuId=2930154&icid2=products%20grid:p520824:product",
               "https://www.sephora.com/product/rare-eau-de-parfum-P517178?skuId=2888188&icid2=products%20grid:p517178:product",
               "https://www.sephora.com/product/good-girl-blush-eau-de-parfum-P504996?skuId=2645026&icid2=products%20grid:p504996:product",
               "https://www.sephora.com/product/glossier-glossier-you-eau-de-parfum-P504364?skuId=2649770&icid2=products%20grid:p504364:product"
               ] #9:20 PM EST Sephora womens frag 2/24/2026
# toprated = ["https://www.sephora.com/product/light-blue-eau-de-toilette-travel-spray-P516185?skuId=2863355&icid2=products%20grid:p516185:product",
#             "https://www.sephora.com/product/indecent-cherry-eau-de-parfum-P520182?skuId=2948586&icid2=products%20grid:p520182:product",
#             "https://www.sephora.com/product/mini-l-imperatrice-eau-de-toilette-set-P517211?skuId=2863488&icid2=products%20grid:p517211:product",
#             "https://www.sephora.com/product/mini-flora-gorgeous-gardenia-eau-de-parfum-duo-set-P514862?skuId=2909539&icid2=products%20grid:p514862:product",
#             "https://www.sephora.com/product/eilish-2-eau-de-parfum-travel-spray-P520152?skuId=2948453&icid2=products%20grid:p520152:product",
#             "https://www.sephora.com/product/bloom-ambrosia-doro-eau-de-parfum-travel-spray-P520382?skuId=2931970&icid2=products%20grid:p520382:product",
#             "https://www.sephora.com/product/kilian-good-girl-gone-bad-travel-spray-P479710?skuId=2530459&icid2=products%20grid:p479710:product",
#             "https://www.sephora.com/product/jpg-le-male-elixir-4-22-oz-shower-gel-travel-spray-0-5-oz-P518157?skuId=2907111&icid2=products%20grid:p518157:product",
#             "https://www.sephora.com/product/barenia-eau-de-parfum-set-60ml-15ml-feh25-P518531?skuId=2909414&icid2=products%20grid:p518531:product",
#             "https://www.sephora.com/product/dolce-gabbana-the-one-gold-eau-de-parfum-intense-P513593?skuId=2821114&icid2=products%20grid:p513593:product",
#             "https://www.sephora.com/product/terre-d-hermes-eau-de-parfum-intense-travel-spray-P516659?skuId=2880029&icid2=products%20grid:p516659:product"
#             ] # 9:28 PM EST Sephora womens frag

# categories = {
#     "bestsellers": bestsellers,
#     "toprated": toprated
# }

def extract_product_id(url):
    """Extracts P# from Sephora URL""" #product#
    match = re.search(r"(P\d+)", url)
    return match.group(1) if match else None


def fetch_reviews(product_id, offset):
    params = {
        "Filter": f"ProductId:{product_id}",
        "Sort": "SubmissionTime:desc",
        "Limit": PAGE_LIMIT,
        "Offset": offset,
        "Include": "Products,Comments",
        "Stats": "Reviews",
        "passkey": PASSKEY,
        "apiversion": "5.4",
        "Locale": "en_US"
    }

    response = requests.get(BAZAARVOICE_ENDPOINT, params=params)
    response.raise_for_status()
    return response.json()


#add product level to original scraper or change logic structure to just scrape about info

all_reviews = []

for idx, url in enumerate(bestsellers):
    print(f"\n  ▶ Loading product {idx + 1}/{len(bestsellers)}")
    print(f"    URL: {url}")

    product_id = extract_product_id(url)
    if not product_id:
        print("    ❌ Could not extract ProductId, skipping")
        continue

    offset = 0
    product_review_count = 0

    while product_review_count < MAX_REVIEWS_PER_PRODUCT:
        data = fetch_reviews(product_id, offset)
        reviews = data.get("Results", [])

        if not reviews:
            break

        for r in reviews:
            all_reviews.append({
                "source_url": url,
                "product_id": product_id,
                "rating": r.get("Rating"),
                "review_text": r.get("ReviewText"),
                "title": r.get("Title"),
                "author": r.get("UserNickname"),
                #"submission_time": r.get("SubmissionTime")
            })

            product_review_count += 1
            if product_review_count >= MAX_REVIEWS_PER_PRODUCT:
                break

        offset += PAGE_LIMIT
        time.sleep(SLEEP_BETWEEN_REQUESTS)

    print(f"    ✅ Finished product with {product_review_count} reviews")

print("\n🎉 SCRAPING COMPLETE")

# ---------------- EXPORT ---------------- #

df = pd.DataFrame(all_reviews)
df.to_csv("sephora_reviews.csv", index=False)

print(f"💾 Saved {len(df)} total reviews to sephoraN_reviews.csv")
