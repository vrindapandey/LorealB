
#put a brand column
#Scrape ingredients and about the product for each unique product

import requests
import pandas as pd
import time
import re
import json
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0"
}

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
descriptionF = []
highlights = []
fragrance_family = []
scent_type = []
key_notes = []

#notes:
# api is only fetching comerce data
#try this api for product data: https://www.sephora.com/api/catalog/products/{productId}
#fix those fields and finish product scraper then move to analyzer for insights

for source in productsdf["source_url"]:

    print("Scraping:", source)
    html = requests.get(source, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")

    product_json = None

    for script in soup.find_all("script"):
        if '"page":{"product"' in script.text:
            product_json = script.text
            break

    if not product_json:
        print("Product JSON not found:", source)
        continue

    start = product_json.find('{"page":{"product"')
    end = product_json.rfind('}}}') + 3

    json_text = product_json[start:end]

    data = json.loads(json_text)

    product = data["page"]["product"]

    # Brand
    brands.append(product.get("brand", {}).get("displayName"))

    # Ingredients
    ingredients.append(product.get("currentSku", {}).get("ingredientDesc"))

    # Highlights
    highlight = [h["displayName"] for h in product.get("highlights", [])]
    highlights.append(", ".join(highlight))

    # Fragrance info
    fragrance_family.append(product.get("fragranceFamily"))
    scent_type.append(product.get("fragranceType"))
    key_notes.append(product.get("keyNotes"))

    time.sleep(3)

    print("Done")
    

productsdf['Brand'] = brands
print(brands)
productsdf['Highlights'] = highlights
print(highlights)
productsdf['Fragrance Family'] = fragrance_family
print(fragrance_family)
productsdf['Scent Type'] = scent_type
print(scent_type)
productsdf['Key Notes'] = key_notes
print(key_notes)
productsdf['Ingredients'] = ingredients
print(ingredients)

productsdf.to_csv("product_info.csv", index=False) #in a new csv all_products with columns product_id, source_url from the csv
