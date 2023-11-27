import pandas as pd

# Load your CSV file
csv_file_path = "model_training/api_response.csv"
df = pd.read_csv(csv_file_path)

# Drop duplicated columns
df = df.loc[:, ~df.columns.duplicated()]

# Save the updated DataFrame back to a CSV file
df.to_csv("model_training/api_response_cleaned.csv", index=False)
