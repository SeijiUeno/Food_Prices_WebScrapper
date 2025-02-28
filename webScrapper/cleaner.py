import pandas as pd
import re

# Load the CSV file with historical product data
df = pd.read_csv("historical_food_products.csv")

# Clean the price column: remove currency symbol and replace comma with dot
df["price_clean"] = (
    df["price"]
    .str.replace("R\\$", "", regex=True)
    .str.strip()
    .str.replace(",", ".")
)
df["price_clean"] = pd.to_numeric(df["price_clean"], errors="coerce")

# Drop rows where the price could not be converted
df = df.dropna(subset=["price_clean"])

# Define a regex pattern to filter out non-unitary products (packs, combos, premium items)
pattern = re.compile(r'\b(?:pack|Unidades|pacote|combo|kit|multipack|Premium)\b', re.IGNORECASE)
df_unitary = df[~df["name"].str.contains(pattern, na=False)]

# Function to remove outliers per category using the IQR method
def remove_outliers(group):
    Q1 = group["price_clean"].quantile(0.25)
    Q3 = group["price_clean"].quantile(0.75)
    IQR = Q3 - Q1
    # Keep rows within the range [Q1 - 1.5*IQR, Q3 + 1.5*IQR]
    return group[(group["price_clean"] >= Q1 - 1.5 * IQR) & (group["price_clean"] <= Q3 + 1.5 * IQR)]

# Group by 'category' and explicitly drop the grouping column before applying outlier removal.
# Then, reassign the grouping column using the group's name.
df_clean = df_unitary.groupby("category", group_keys=False).apply(
    lambda g: remove_outliers(g.drop(columns=["category"])).assign(category=g.name)
)

# Optionally, save the cleaned data to a new CSV file
df_clean.to_csv("historical_food_products_clean.csv", index=False)

print("Data cleaning complete. Cleaned data saved to 'historical_food_products_clean.csv'.")
