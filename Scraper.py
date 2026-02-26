from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

#controls
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
toprated = ["https://www.sephora.com/product/light-blue-eau-de-toilette-travel-spray-P516185?skuId=2863355&icid2=products%20grid:p516185:product",
            "https://www.sephora.com/product/indecent-cherry-eau-de-parfum-P520182?skuId=2948586&icid2=products%20grid:p520182:product",
            "https://www.sephora.com/product/mini-l-imperatrice-eau-de-toilette-set-P517211?skuId=2863488&icid2=products%20grid:p517211:product",
            "https://www.sephora.com/product/mini-flora-gorgeous-gardenia-eau-de-parfum-duo-set-P514862?skuId=2909539&icid2=products%20grid:p514862:product",
            "https://www.sephora.com/product/eilish-2-eau-de-parfum-travel-spray-P520152?skuId=2948453&icid2=products%20grid:p520152:product",
            "https://www.sephora.com/product/bloom-ambrosia-doro-eau-de-parfum-travel-spray-P520382?skuId=2931970&icid2=products%20grid:p520382:product",
            "https://www.sephora.com/product/kilian-good-girl-gone-bad-travel-spray-P479710?skuId=2530459&icid2=products%20grid:p479710:product",
            "https://www.sephora.com/product/jpg-le-male-elixir-4-22-oz-shower-gel-travel-spray-0-5-oz-P518157?skuId=2907111&icid2=products%20grid:p518157:product",
            "https://www.sephora.com/product/barenia-eau-de-parfum-set-60ml-15ml-feh25-P518531?skuId=2909414&icid2=products%20grid:p518531:product",
            "https://www.sephora.com/product/dolce-gabbana-the-one-gold-eau-de-parfum-intense-P513593?skuId=2821114&icid2=products%20grid:p513593:product",
            "https://www.sephora.com/product/terre-d-hermes-eau-de-parfum-intense-travel-spray-P516659?skuId=2880029&icid2=products%20grid:p516659:product"
            ] # 9:28 PM EST Sephora womens frag

categories = {
    "bestsellers": bestsellers,
    "toprated": toprated
}

all_reviews = []

#scroll and load review helper func
import time

def lazy_scroll(driver, pause=2, steps=4):
    for _ in range(steps):
        # Scroll until "Reviews" text is visible
        driver.execute_script("""
        const el = Array.from(document.querySelectorAll('*'))
        .find(e => e.textContent.trim() === 'Reviews');
        if (el) el.scrollIntoView({behavior: 'smooth', block: 'center'});
        """)
        time.sleep(3)
        # driver.execute_script(
        #     "window.scrollBy(0, document.body.scrollHeight / arguments[0]);",
        #     steps
        # )
        #time.sleep(pause)

#extract visible reviews func
from selenium.common.exceptions import NoSuchElementException

def extract_reviews(driver, category, url, collected, limit=500):
    # reviews = driver.find_elements(By.CSS_SELECTOR, "div[data-comp*='Review ']")

    reviews = driver.find_elements(
    By.XPATH,
    "//div[@data-comp='Review Review BaseComponent ']"
)
    print("Reviews found:", len(reviews))

    for r in reviews:
        try:
            text = r.find_element(
                By.XPATH,
                ".//div[string-length(normalize-space(text())) > 20]"
            ).text

            rating = r.find_element(
                By.XPATH,
                ".//span[contains(@aria-label,'stars')]"
            ).get_attribute("aria-label")

            author = r.find_element(
                By.XPATH,
                ".//a[@data-at='nickname']"
            ).text

            collected.append({
                "category": category,
                "source_url": url,
                "rating": rating,
                "review_text": text,
                "author": author
            })

        except:
            continue
    # for r in reviews:
    #     if len(collected) >= limit:
    #         return collected

    #     try:
    #         text_el = r.find_elements(By.CSS_SELECTOR, "div.css-2482tk")
    #         if not text_el:
    #             continue

    #         review_text = text_el[0].text.strip()

    #         rating = r.find_element(By.CSS_SELECTOR, "span[aria-label*='stars']").get_attribute("aria-label")
    #         author = r.find_element(By.CSS_SELECTOR, "a[data-at='nickname']").text

    #         collected.append({
    #             "category": category,
    #             "source_url": url,
    #             "rating": rating,
    #             "review_text": review_text,
    #             "author": author
    #         })

    #     except NoSuchElementException:
    #         continue

    # return collected

#scraping driver func
MAX_REVIEWS_PER_CATEGORY = 500

for category, urls in categories.items():
    print(f"\nStarting category: {category}")

    category_reviews = 0   # y reset per category

    for x, url in enumerate(urls):
        if category_reviews >= MAX_REVIEWS_PER_CATEGORY:
            break

        print(f"  Loading product {x+1}/{len(urls)}")

        driver.get(url)
        from selenium.webdriver.common.by import By
        time.sleep(2)

        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"Found {len(iframes)} iframes")

        review_iframe = None

        for i, iframe in enumerate(iframes):
            try:
                driver.switch_to.frame(iframe)
                if "Recommended" in driver.page_source or "Reviews" in driver.page_source:
                    review_iframe = iframe
                    print(f"✅ Reviews iframe found at index {i}")
                    driver.switch_to.frame(review_iframe)

                    prev_count = 0

                    while category_reviews < MAX_REVIEWS_PER_CATEGORY:
                        reviews = driver.find_elements(
                            By.XPATH,
                            "//div[@data-comp='Review Review BaseComponent ']"
                        )

                        print("Reviews found:", len(reviews))

                        if len(reviews) == prev_count:
                            break

                        prev_count = len(reviews)

                        extract_reviews(
                            driver,
                            category,
                            url,
                            all_reviews,
                            limit=MAX_REVIEWS_PER_CATEGORY
                        )

                        category_reviews = sum(
                            1 for r in all_reviews if r["category"] == category
                        )

                        driver.execute_script(
                            "window.scrollTo(0, document.body.scrollHeight);"
                        )
                        time.sleep(2)

                    driver.switch_to.default_content()
                    break
                driver.switch_to.default_content()
            except:
                driver.switch_to.default_content()

        if not review_iframe:
            print("❌ No review iframe found, skipping product")
            continue
        # iframes = driver.find_elements(By.TAG_NAME, "iframe")
        # print("IFRAMES FOUND:", len(iframes))
        #time.sleep(3)

    # prev_count = 0

    # while len(all_reviews) < 500:
    #     reviews = driver.find_elements(
    #         By.XPATH,
    #         "//div[@data-comp='Review Review BaseComponent ']"
    #     )

    #     if len(reviews) == prev_count:
    #         break

    #     prev_count = len(reviews)

    #     for r in reviews:
    #         try:
    #             text = r.find_element(
    #                 By.XPATH,
    #                 ".//div[string-length(normalize-space(text())) > 20]"
    #             ).text

    #             rating = r.find_element(
    #                 By.XPATH,
    #                 ".//span[contains(@aria-label,'stars')]"
    #             ).get_attribute("aria-label")

    #             author = r.find_element(
    #                 By.XPATH,
    #                 ".//a[@data-at='nickname']"
    #             ).text

    #             all_reviews.append({
    #                 "category": category,
    #                 "source_url": url,
    #                 "rating": rating,
    #                 "review_text": text,
    #                 "author": author
    #             })

    #         except:
    #             continue

        # scroll INSIDE iframe
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        driver.switch_to.default_content()

        # previous_count = -1

        # while category_reviews < MAX_REVIEWS_PER_CATEGORY:
        #     lazy_scroll(driver)

        #     before = len(all_reviews)

        #     extract_reviews(
        #         driver,
        #         category,
        #         url,
        #         all_reviews,
        #         limit=MAX_REVIEWS_PER_CATEGORY
        #     )

        #     after = len(all_reviews)
        #     category_reviews = sum(1 for r in all_reviews if r["category"] == category)

        #     if after == before or after == previous_count:
        #         break  # no new reviews loading

        #     previous_count = after

        print(f"    Collected {category_reviews} reviews so far")

    print(f"SUCCESS: Finished {category} with {category_reviews} reviews")

#export to one spreadsheet
import pandas as pd

df = pd.DataFrame(all_reviews)
df.to_csv("sephora_reviews.csv", index=False)

print(f"\nSaved {len(df)} total reviews to sephora_reviews.csv")



#scrape from 0-10 of the bestseller and toprated
#create a 


#needed functionality:
#load reviews from bestsellers
#append reviews
#continue loading and appending till reaches 500 (maybe need y indec)
#some kind of success message mb
#reset y if there's y
#load reviews from toprated
#append reviews
#continue till reaches 500 
#append all reviews with category (list) and their respective source urls (x index)
#some kind of success message mb
#increment x and reset y
#convert all reviews to csv

# for x in range(10):
#     url = bestsellers[x]

#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     wait = WebDriverWait(driver, 10)

#     #wait till a review is present
#     #wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-comp='Review']"))) #generic
#     wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-comp*='Review Review BaseComponent ']")))

#     #reviews = driver.find_elements(By.CSS_SELECTOR, "div[data-comp='Review']") #generic
#     reviews = driver.find_elements(By.CSS_SELECTOR, "div[data-comp='Review Review BaseComponent ']")
#     #print(f"Found {len(reviews)} reviews")

#     data = []

#     for review in reviews:
#         try:
#             # Review text
#             text = review.find_element(By.CSS_SELECTOR, "div.css-2482tk").text
        
#             # Rating (convert "5 stars" → 5)
#             rating_str = review.find_element(By.CSS_SELECTOR, "span[aria-label*='stars']").get_attribute("aria-label")
#             rating = int(rating_str.split()[0])
        
#             # Author
#             author = review.find_element(By.CSS_SELECTOR, "a[data-at='nickname']").text
        
#             data.append({
#                 "author": author,
#                 "rating": rating,
#                 "review_text": text
#         })
        
#         except Exception as e:
#             print("Skipped one review:", e)


#     while len(data) < 500:
#         try:
#             load_more = driver.find_element(By.XPATH, "//button[contains(text(),'Load More')]")
#             load_more.click()
#             time.sleep(2)

#             reviews = driver.find_elements(By.CSS_SELECTOR, "div[data-comp='Review ']")
#             print("Total reviews:", len(reviews))
#         except:
#             break

# for category, urls in {
#     "bestsellers": bestselling,
#     "toprated": toprate
# }.items():

#     for url in urls:
#         driver.get(url)

#         # load reviews (scroll logic)
#         # find review elements

#         for review in reviews:
#             all_reviews.append({
#                 "category": category,
#                 "rating": rating,
#                 "review_text": text,
#                 "author": author,
#                 "source_url": url
#             })