import pandas as pd
from transformers import pipeline

# Load the CSV file
df = pd.read_csv("historical_food_products.csv")

# Clean the price column: remove the currency symbol and convert to float
df["price_clean"] = (
    df["price"]
    .str.replace("R\\$", "", regex=True)
    .str.strip()
    .str.replace(",", ".")
)
df["price_clean"] = pd.to_numeric(df["price_clean"], errors="coerce")
df = df.dropna(subset=["price_clean"])

# Setup a zero-shot classification pipeline using a model such as facebook/bart-large-mnli
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define candidate labels:
# "unitary product" means a single item sale;
# "pack or premium product" indicates multiple items in a pack or a premium offering.
candidate_labels = ["unitary product", "pack or premium product"]

# Function to classify each product based on its name
def classify_product(name):
    # Run the classifier on the product name
    result = classifier(name, candidate_labels)
    # The model returns scores for each candidate label;
    # we choose the label with the highest score.
    predicted_label = result["labels"][0]
    confidence = result["scores"][0]
    return predicted_label, confidence

# Apply the classifier to each product name and store the results
df["classification"], df["confidence"] = zip(*df["name"].apply(lambda x: classify_product(x) if isinstance(x, str) else ("unknown", 0)))

# Optionally, display some of the classified product names so you can review the decisions
print("Sample of product classifications:")
print(df[["name", "classification", "confidence"]].head(10))

# Filter the DataFrame to keep only unitary products
df_unitary = df[df["classification"] == "unitary product"]

# Function to remove price outliers using the IQR method per category
def remove_outliers(group):
    Q1 = group["price_clean"].quantile(0.25)
    Q3 = group["price_clean"].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return group[(group["price_clean"] >= lower_bound) & (group["price_clean"] <= upper_bound)]

# Remove outliers on a per-category basis
df_clean = df_unitary.groupby("category", group_keys=False).apply(remove_outliers)

# Save the cleaned data to a new CSV file
df_clean.to_csv("historical_food_products_cleaned.csv", index=False)

print("Data cleaning complete. Cleaned data saved to 'historical_food_products__smart_cleaned.csv'.")