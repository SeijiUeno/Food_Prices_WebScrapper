import csv
import os
import datetime  # Make sure this import is here
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Setup logging to only display the date (YYYY-MM-DD)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d'
)

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
    )
    return webdriver.Chrome(options=chrome_options)

def scrape_category(driver, category, url):
    results = []
    try:
        logging.info(f"Processing category: {category} -> {url}")
        driver.get(url)
        
        # Use an explicit wait for the product grid to load (up to 10 seconds)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.grid.grid-cols-2.md\\:grid-cols-3.lg\\:grid-cols-4.xl\\:grid-cols-5")
            )
        )
        
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        
        # Locate the product grid using a CSS selector
        product_grid = soup.select_one("div.grid.grid-cols-2.md\\:grid-cols-3.lg\\:grid-cols-4.xl\\:grid-cols-5")
        if not product_grid:
            logging.warning(f"  Product grid not found for category: {category}")
            return results
        
        # Find all product cards (<a> elements) inside the grid
        products = product_grid.find_all("a", recursive=False)
        if not products:
            logging.warning(f"  No products found for category: {category}")
            return results
        
        for product in products:
            # Extract product name from the <h2> tag
            h2 = product.find("h2")
            name = h2.get_text(strip=True) if h2 else "N/A"
            
            # Extract product price from the expected <span> tag
            price_tag = product.find("span", class_="text-base font-bold text-default-dark")
            price = price_tag.get_text(strip=True) if price_tag else "N/A"
            
            results.append({
                "date": datetime.datetime.now().strftime('%Y-%m-%d'),
                "category": category,
                "name": name,
                "price": price,
                "source": url  # Record the source URL for reference
            })
            logging.info(f"  Product: {name} - Price: {price}")
    
    except Exception as e:
        logging.error(f"Error processing category {category}: {e}")
    return results

def main():
    categories = [
        "arroz",
        "feijao",
        "leite",
        "macarrao",
        "acucar",
        "sal",
        "farinha"
    ]
    
    base_url = "https://mercado.carrefour.com.br/busca/{}"
    all_results = []
    driver = setup_driver()
    
    try:
        for category in categories:
            url = base_url.format(category)
            results = scrape_category(driver, category, url)
            all_results.extend(results)
    finally:
        driver.quit()
    
    # Ensure the subdirectory exists
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    
    # Append today's data to the historical CSV file.
    file_name = os.path.join(output_dir, "historical_food_products.csv")
    file_exists = os.path.exists(file_name)
    fieldnames = ["date", "category", "name", "price", "source"]
    
    with open(file_name, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for product in all_results:
            writer.writerow(product)
    
    logging.info("Scraping complete! Data appended to 'historical_food_products.csv'.")

if __name__ == "__main__":
    main()
