
import requests
import pandas as pd
import time
import re

# ---------------- CONFIG ---------------- #

MAX_REVIEWS_PER_PRODUCT = 500
PAGE_LIMIT = 100   # max allowed by BV is usually 100
SLEEP_BETWEEN_REQUESTS = 0.5

BAZAARVOICE_ENDPOINT = "https://api.bazaarvoice.com/data/reviews.json"

PASSKEY = "calXm2DyQVjcCy9agq85vmTJv5ELuuBCF2sdg4BnJzJus"

all_products = []

# ---------------- URL LISTS ---------------- #

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
               ] #9:20 PM EST Sephora womens frag

# ---------------- EXPORT ---------------- #

df = pd.DataFrame(all_products)
df.to_csv("bestseller_info.csv", index=False)

print(f"💾 Saved bestseller info to bestseller_info.csv")