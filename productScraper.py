
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
highlights = []
fragrance_family = []
scent_type = []
key_notes = []

#long description
#aboutFragrance
#aboutBottle

#notes:
# api is only fetching comerce data
#try this api for product data: https://www.sephora.com/api/catalog/products/{productId}

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

    #debugging
    #print(product.keys())
    #print(product["currentSku"].keys())
    #print(product["productDetails"].keys())
    #print(product.get("productDetails",{}).get("brand"))
    #print(product.get("productDetails",{}).get("shortDescription"))
    #print(json.dumps(product, indent=2)[:1000])

    # Brand
    brands.append(product.get("currentSku", {}).get("brandName"))

    # Ingredients
    ingredients.append(product.get("currentSku", {}).get("ingredientDesc"))
    

    # Highlights
    highlight_list = product.get("currentSku", {}).get("highlights")
    highlight_texts = [h.get("altText") for h in highlight_list]
    highlights.append(", ".join(highlight_texts))
    #print(highlight_list)
    # highlight_names = [h.get("displayName") for h in highlight_list if "displayName" in h]
    # highlights.append(", ".join(highlight_names))

    # highlight = [h["displayName"] for h in product.get("highlights", [])]
    # highlights.append(", ".join(highlight))

    # Fragrance info - within shortDescription
    details = product.get("productDetails", {})
    short_desc = details.get("shortDescription", "")

    family_match = re.search(r"Fragrance Family:\s*</?(?:b|strong)?[^>]*>\s*([^<]+)", short_desc)
    scent_match = re.search(r"Scent Type:\s*</?(?:b|strong)?[^>]*>\s*([^<]+)", short_desc)
    notes_match = re.search(r"Key Notes:\s*</?(?:b|strong)?[^>]*>\s*([^<]+)", short_desc)

    family = family_match.group(1).strip() if family_match else None
    scent = scent_match.group(1).strip() if scent_match else None
    notes = notes_match.group(1).strip() if notes_match else None

    fragrance_family.append(family)
    scent_type.append(scent)
    key_notes.append(notes)

    # family = None
    # scent = None
    # notes = None

    # print(desc_soup)

    # for p in desc_soup.find_all("p"):
    #     strong = p.find("strong")
    #     if not strong:
    #         continue

    #     label = strong.text.strip()
    #     value = p.get_text().replace(strong.text, "").strip()

    #     if "Fragrance Family" in label:
    #         family = value
    #     elif "Scent Type" in label:
    #         scent = value
    #     elif "Key Notes" in label:
    #         notes = value

    # fragrance_family.append(product.get("currentSku", {}).get("ingredientDesc"))
    # scent_type.append(product.get("currentSku", {}).get("ingredientDesc"))
    # key_notes.append(product.get("currentSku", {}).get("ingredientDesc"))

    time.sleep(2)

    print("Done")
    

productsdf['Brand'] = brands
#print(brands) #nones
productsdf['Highlights'] = highlights
# print(highlights) #quotes
productsdf['Fragrance Family'] = fragrance_family
# print(fragrance_family) #nones
productsdf['Scent Type'] = scent_type
# print(scent_type) #nones
productsdf['Key Notes'] = key_notes
# print(key_notes) #nones
productsdf['Ingredients'] = ingredients
# print(ingredients)

productsdf.to_csv("product_info.csv", index=False) #in a new csv all_products with columns product_id, source_url from the csv
