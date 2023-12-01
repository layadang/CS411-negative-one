import json
import csv

def json_to_csv(json_data, csv_filename):
    header = json_data[0]['results'][0].keys()

    with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=header)
        writer.writeheader()

        for page_data in json_data:
            for entry in page_data['results']:
                writer.writerow(entry)

# Specify the JSON file name
json_filename = 'model_training/api_response.json'

# Specify the output CSV file name
output_csv_filename = 'model_training/api_response.csv'

# Read JSON data from file
with open(json_filename, 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

# Call the function
json_to_csv(json_data, output_csv_filename)
