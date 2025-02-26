import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# ----- Setup Selenium -----
chrome_options = Options()
chrome_options.add_argument("--headless")       # Run headless (without GUI)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# This code assumes that the ChromeDriver is in your PATH.
driver = webdriver.Chrome(options=chrome_options)

# ----- List of Basic Food Categories -----
categories = [
    "arroz",
    "feijao",
    "leite",
    "macarrao",
    "acucar",
    "sal",
    "farinha"
]

base_url = "https://mercado.carrefour.com.br/mercearia/alimentos-basicos/{}"
results = []

for category in categories:
    url = base_url.format(category)
    print(f"Processing category: {category} -> {url}")
    driver.get(url)
    
    # Wait for the page to fully load dynamic content (adjust time as needed)
    time.sleep(5)
    
    # Parse the rendered HTML with BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    
    # Locate the product grid. Adjust the class if the site layout changes.
    product_list = soup.find("ul", class_="grid grid-cols-2 xl:grid-cols-5 md:grid-cols-4")
    if not product_list:
        print(f"  Product grid not found for category: {category}")
        continue
    
    products = product_list.find_all("li")
    if not products:
        print(f"  No products found for category: {category}")
        continue
    
    for li in products:
        article = li.find("article")
        if article:
            # Extract the product name from the <h3> tag
            h3 = article.find("h3")
            name = h3.get_text(strip=True) if h3 else "N/A"
            
            # Extract the product price from the <span> with data-test-id="price"
            price_tag = article.find("span", {"data-test-id": "price"})
            price = price_tag.get_text(strip=True) if price_tag else "N/A"
            
            results.append({"category": category, "name": name, "price": price})
            print(f"  Product: {name} - Price: {price}")

# ----- Save the results to a CSV file -----
with open("basic_food_products.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["category", "name", "price"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for product in results:
        writer.writerow(product)

driver.quit()
print("Scraping complete! Results saved to 'basic_food_products.csv'.")
