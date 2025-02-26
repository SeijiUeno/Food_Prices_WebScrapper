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

# Initialize the webdriver; adjust the executable_path if not in your PATH.
driver = webdriver.Chrome(options=chrome_options)

# ----- Load the target URL -----
url = "https://mercado.carrefour.com.br/mercearia/alimentos-basicos/arroz"
driver.get(url)

# Wait for the page to fully load dynamic content (adjust sleep time if needed)
time.sleep(5)

# ----- Parse the Rendered HTML -----
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# Locate the product grid
product_list = soup.find("ul", class_="grid grid-cols-2 xl:grid-cols-5 md:grid-cols-4")
if not product_list:
    print("Product grid not found!")
    products = []
else:
    products = product_list.find_all("li")

results = []

# Extract product name and price from each product entry
for li in products:
    article = li.find("article")
    if article:
        # Extract product name from the <h3> tag (or its <a> child)
        h3 = article.find("h3")
        name = h3.get_text(strip=True) if h3 else "N/A"
        
        # Extract price from the <span> with data-test-id="price"
        price_tag = article.find("span", {"data-test-id": "price"})
        price = price_tag.get_text(strip=True) if price_tag else "N/A"
        
        results.append({"name": name, "price": price})
        print(f"Product: {name} - Price: {price}")

# ----- Save the Results to a CSV File -----
with open("products.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["name", "price"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for product in results:
        writer.writerow(product)

# Clean up by closing the Selenium driver
driver.quit()

