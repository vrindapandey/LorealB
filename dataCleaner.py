import pandas as pd

# Load CSV
df = pd.read_csv("origSephora.csv")

# Inspect
# print(df.head())
# print(df.info())
# print(df.columns)

df = df[df["category"] != "toprated"] #remove toprated entries

#remove libre travel size
df = df[df["source_url"] != "https://www.sephora.com/product/libre-berry-crush-travel-spray-P520822?skuId=2919769&icid2=products%20grid:p520822:product"]

df = df.drop(columns=["submission_time"]) #remove time column
df = df.drop(columns=["category"]) #remove category column

df.to_csv("sephora_reviews.csv", index=False) 

