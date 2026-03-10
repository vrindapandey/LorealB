
#put a brand column
#Scrape ingredients and about the product for each unique product

import requests
import pandas as pd
import time
import re
#from bs4 import BeautifulSoup

# ---------------- CONFIG ---------------- #

# MAX_REVIEWS_PER_PRODUCT = 500
# PAGE_LIMIT = 100   # max allowed by BV is usually 100
# SLEEP_BETWEEN_REQUESTS = 0.5

# BAZAARVOICE_ENDPOINT = "https://api.bazaarvoice.com/data/reviews.json"

# PASSKEY = "calXm2DyQVjcCy9agq85vmTJv5ELuuBCF2sdg4BnJzJus"

# all_products = []

# # ---------------- URL LISTS ---------------- #

# bestsellers = ["https://www.sephora.com/product/libre-berry-crush-P520837?skuId=2919744&icid2=products%20grid:p520837:product",
#                "https://www.sephora.com/product/kayali-yum-boujee-marshmallow-81-eau-de-parfum-intense-travel-spray-P512449?skuId=2804839&icid2=products%20grid:p512449:product",
#                "https://www.sephora.com/product/kayali-vanilla-P439406?skuId=2163970&icid2=products%20grid:p439406:product",
#                "https://www.sephora.com/product/phlur-vanilla-skin-hair-body-fragrance-mist-P509258?skuId=2693349&icid2=products%20grid:p509258:product",
#                "https://www.sephora.com/product/eilish-1-eau-de-parfum-P520204?skuId=2948495&icid2=products%20grid:p520204:product",
#                "https://www.sephora.com/product/libre-berry-crush-travel-spray-P520822?skuId=2919769&icid2=products%20grid:p520822:product",
#                "https://www.sephora.com/product/paradoxe-eau-de-parfum-P501198?skuId=2591170&icid2=products%20grid:p501198:product",
#                "https://www.sephora.com/product/donna-born-in-roma-purple-melancholia-P520824?skuId=2930154&icid2=products%20grid:p520824:product",
#                "https://www.sephora.com/product/rare-eau-de-parfum-P517178?skuId=2888188&icid2=products%20grid:p517178:product",
#                "https://www.sephora.com/product/good-girl-blush-eau-de-parfum-P504996?skuId=2645026&icid2=products%20grid:p504996:product",
#                "https://www.sephora.com/product/glossier-glossier-you-eau-de-parfum-P504364?skuId=2649770&icid2=products%20grid:p504364:product"
#                ] #9:20 PM EST Sephora womens frag

# ---------------- MAIN SCRAPER CODE ---------------- #

df = pd.read_csv("sephora_reviews.csv")
#compress reviews to unique products by ID
#productsdf = df[['product_id', 'source_url']].drop_duplicates(subset='product_id') #make every unique product ID one entry 
productsdf = (
    df.groupby('product_id', as_index=False)
      .agg(
          source_url=('source_url', 'first'),
          avg_rating=('rating', 'mean'), #should include avg rating column as avg
          review_count=('rating', 'count')
      )
)

brands = []
ingredients = []
highlights = []
fragrance_family = []
scent_type = []
key_notes = []

for pid in productsdf["product_id"]:

    #print(pid)
    api_url = f"https://www.sephora.com/api/v3/users/profiles/current/product/{pid}"
    #if want more info api_url = api_url = f"https://www.sephora.com/api/v3/users/profiles/current/product/{pid}?countryCode=US&loc=EN-US"
    #api_url = f"https://www.sephora.com/api/catalog/products/{pid}"
    # https://www.sephora.com/api/v3/users/profiles/current/product/P512856?skipAddToRecentlyViewed=false&preferedSku=2804821&countryCode=US&loc=EN-US&cb=1772772652
    # api url from inspect network - fetch xmr - P512...?skipAddtorecentlyviewed
    r = requests.get(api_url, headers={"User-Agent": "Mozilla/5.0"})
    data = r.json()
    print(data.keys())
    # brand
    brand = data.get("ancillarySkus", [{}])[0].get("brandName")
    brands.append(brand)
    #brands.append(data["ancillarySkus"][0]["brandName"])
    #brands.append(data["brandName"]) #["displayName"]

    #remaining info not through that api url find how to extract
    # ingredients
    ingredient = data.get("currentSku", [{}])[0].get("ingredientDesc")
    ingredients.append(ingredient)

    # highlights
    h = [x["displayName"] for x in data.get("highlights", [])]
    highlights.append(", ".join(h))

    # fragrance details
    details = data.get("productDetails", {})

    fragrance_family.append(details.get("fragranceFamily"))
    scent_type.append(details.get("fragranceType"))
    key_notes.append(details.get("keyNotes"))

    time.sleep(0.3)
#time buffer to finish prev task
# brands = []
# highlights_list = []
# ingredients_list = []

# about_cols = {
#     "Fragrance Family": [],
#     "Scent Type": [],
#     "Key Notes": [],
#     "Fragrance Description": [],
#     "About the Bottle": [],
#     "About the Fragrance": []
# }

# for url in productsdf["source_url"]:

#     response = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
#     soup = BeautifulSoup(response.text, "html.parser")

#     brand_tag = soup.find("a", {"data-at":"brand_name"})
#     brand = brand_tag.text.strip() if brand_tag else None
#     brands.append(brand)

#     highlights = soup.select("div.css-fuws2b span.css-1d7qtkv, div.css-fuws2b span.css-1tihdel")
#     highlight_values = [h.text.strip() for h in highlights]
#     highlights_list.append(", ".join(highlight_values))

#     about_section = soup.select_one("div.css-1c3otrr")

#     about_data = {}

#     if about_section:
#         for b in about_section.find_all("b"):
#             label = b.text.replace(":", "").strip()
#             value = b.next_sibling.strip() if b.next_sibling else None
#             about_data[label] = value
#             for key in about_cols:
#                 about_cols[key].append(about_data.get(key))

#     ingredients_tag = soup.select_one("#ingredients div.css-yg260s")

#     ingredients = ingredients_tag.text.strip() if ingredients_tag else None
#     ingredients_list.append(ingredients)

#     time.sleep(1)

# productsdf["brand"] = brands
# productsdf["highlights"] = highlights_list
# productsdf["ingredients"] = ingredients_list

# for key in about_cols:
#     productsdf[key] = about_cols[key]


productsdf.to_csv("product_info.csv", index=False) #in a new csv all_products with columns product_id, source_url from the csv


# ---------------- EXPORT ---------------- #

# df = pd.DataFrame(all_products)
# df.to_csv("bestseller_info.csv", index=False)

# print(f"💾 Saved bestseller info to bestseller_info.csv")