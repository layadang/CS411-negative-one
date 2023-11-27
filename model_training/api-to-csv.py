import os
import requests
import csv

def make_api_request(api_url, params, headers):
    response = requests.get(api_url, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def save_to_csv(data, csv_file):
    with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Write the data
        for row in data:
            writer.writerow(row.values())

if __name__ == "__main__":
    # Get the absolute path of the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    api_url = "https://moviesdatabase.p.rapidapi.com/titles"
    params = {
        'startYear': '2022',
        'titleType': 'movie',
        'sort': 'year.incr',
        'endYear': '2024',
        'page': 1
    }

    headers = {
        "X-RapidAPI-Key": "deba0d8e00msh8e8b85337b08fc9p10c542jsn1c6116b93fb4",
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }

    # Construct the absolute path for the CSV file
    csv_file_path = os.path.join(script_dir, 'api_response.csv')

    while True:
        # Make the API request
        response_data = make_api_request(api_url, params, headers)

        if response_data:
            # Save the current page to a CSV file
            save_to_csv(response_data['results'], csv_file_path)

            # Check if there are more pages
            next_page = response_data.get('next', '')
            if not next_page:
                print(f"All pages retrieved. Data saved to {csv_file_path}")
                break

            # Update the 'page' parameter to fetch the next page of results
            params['page'] += 1
        else:
            print("Failed to retrieve data from the API.")
            break
