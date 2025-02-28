import os
import pandas as pd
import re

# Compute the directory 
current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, "..", "data")
os.makedirs(data_dir, exist_ok=True)

input_file = os.path.join(data_dir, "historical_food_products.csv")
output_file = os.path.join(data_dir, "historical_food_products_clean.csv")

# Load the CSV
df = pd.read_csv(input_file, engine="python", on_bad_lines='skip')

# Clean
df["price_clean"] = (
    df["price"]
    .str.replace("R\\$", "", regex=True)
    .str.strip()
    .str.replace(",", ".")
)
df["price_clean"] = pd.to_numeric(df["price_clean"], errors="coerce")

df = df.dropna(subset=["price_clean"])

pattern = re.compile(r'\b(?:pack|Unidades|pacote|combo|kit|multipack|Premium)\b', re.IGNORECASE)
df_unitary = df[~df["name"].str.contains(pattern, na=False)]

def remove_outliers(group):
    Q1 = group["price_clean"].quantile(0.25)
    Q3 = group["price_clean"].quantile(0.75)
    IQR = Q3 - Q1
    return group[(group["price_clean"] >= Q1 - 1.5 * IQR) & (group["price_clean"] <= Q3 + 1.5 * IQR)]

df_clean = df_unitary.groupby("category", group_keys=False).apply(
    lambda g: remove_outliers(g.drop(columns=["category"])).assign(category=g.name)
)

df_clean.to_csv(output_file, index=False)

print(f"Data cleaning complete. Cleaned data saved to '{output_file}'.")
