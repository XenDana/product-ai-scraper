# main.py
from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
import json
import asyncio
import os

app = FastAPI()

@app.post("/product-review")
async def product_review(request: dict):
    asyncio.create_task(scrape(request['url'], request['product_id']))  # Schedule scrape asynchronously
    return {"status": "scraping started"}

@app.get("/product-review")
async def product_review(id):
    # Read the JSON file with the name "id.json"
    with open(f"{id}.json", 'r') as json_file:
        data = json.load(json_file)
    return data

# To run the application, use: uvicorn main:app --reload``

async def scrape(url, product_id):
    # Set up Firefox options
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    # Specify the path to the geckodriver if it's not in your PATH
    script_dir = os.path.dirname(os.path.abspath(__file__))
    service = Service(executable_path=os.path.join(script_dir, 'geckodriver'))

    # Create a new instance of the Firefox driver
    driver = webdriver.Firefox(service=service, options=options)

    # Navigate to a webpage
    driver.get(url)

    x_pixels = 800  # Set the number of pixels to scroll down
    driver.execute_script(f"window.scrollBy(0, {x_pixels});")

    # Wait for a few seconds to see the results
    time.sleep(10)

    # Example: Find the search box and perform a search
    review_feed_element = driver.find_element(By.ID, "review-feed")

    reviews = []

    for review_element in review_feed_element.find_elements(By.XPATH, ".//article"):
        try:
            review = {}
            star_rating_element = review_element.find_element(By.XPATH, ".//div[@data-testid='icnStarRating']")
            review_star = star_rating_element.get_attribute("aria-label")
            review_description = review_element.find_element(By.XPATH, ".//span[@data-testid='lblItemUlasan']").text
            if review_star == 'bintang 1':
                review["review_star"] = 1
            elif review_star == 'bintang 2':
                review["review_star"] = 2
            elif review_star == 'bintang 3':
                review["review_star"] = 3
            elif review_star == 'bintang 4':
                review["review_star"] = 4
            elif review_star == 'bintang 5':
                review["review_star"] = 5
            
            review["review_description"] = review_description
            reviews.append(review)
        except Exception as e:
            # print(f"Error occurred: {e}")
            continue
        

    # Wait for a few seconds to see the results
    driver.implicitly_wait(5)

    with open(product_id + '.json', 'w') as json_file:
        json.dump(reviews, json_file, ensure_ascii=False, indent=4) 

    # Close the browser
    driver.quit()