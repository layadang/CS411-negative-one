import os
import requests
import json

def make_api_request(url, params, headers):
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return None

def convert_to_json(data):
    def process_entry(entry):
        # Check if all required attributes are present
        if all(attr in entry for attr in ['titleText', 'releaseYear', 'genres', 'plot']):
            # Check if 'genres' attribute is present
            genres_data = entry.get('genres')
            if genres_data:
                genres = genres_data.get('genres', [])
                genre_str = ', '.join([genre['text'] for genre in genres])
            else:
                genre_str = ''

            plot = entry['plot']
            plot_text = plot['plotText']['plainText'] if plot and plot.get('plotText') else None

            json_entry = {
                "title": entry['titleText']['text'],
                "year": entry['releaseYear']['year'],
                "genre": genre_str,
                "plot": plot_text
            }

            return json_entry
        else:
            # If any required attribute is missing, return None
            return None

    result = {
        "page": 1,
        "next": "",
        "entries": len(data),
        "results": []
    }

    for entry in data:
        json_entry = process_entry(entry)
        if json_entry:
            result["results"].append(json_entry)

    return result

def save_to_json(json_data, json_file):
    # Load existing JSON data from the file, if it exists
    existing_data = []
    if os.path.exists(json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as existing_file:
                # Check if the file is empty or not
                file_content = existing_file.read()
                if file_content.strip():
                    existing_data = json.loads(file_content)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading existing JSON data: {e}")

    # Append the current page's data to the existing data
    existing_data.append(json_data)

    # Save the combined data to the file
    with open(json_file, 'w', encoding='utf-8') as json_file:
        json.dump(existing_data, json_file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # Get the absolute path of the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    api_url = "https://moviesdatabase.p.rapidapi.com/titles"
    params = {
        'info': 'base_info',
        # Iterate through year 2022, 2023, and 2024 each once to get the full api_response
        # It seems like api's own year range filter is inaccurate
        'year': '2024',
        'titleType': 'movie',
        'page': 1
    }

    headers = {
        "X-RapidAPI-Key": "deba0d8e00msh8e8b85337b08fc9p10c542jsn1c6116b93fb4",
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }

    # Construct the absolute path for the JSON file
    json_file_path = os.path.join(script_dir, 'api_response.json')

    while True:
        # Make the API request
        response_data = make_api_request(api_url, params, headers)

        if response_data:
            # Convert and save the JSON format
            json_data = convert_to_json(response_data['results'])
            save_to_json(json_data, json_file_path)

            # Check if there are more pages
            next_page = response_data.get('next', '')
            if not next_page:
                print(f"All pages retrieved. Data saved to {json_file_path}")
                break

            # Update the 'page' parameter to fetch the next page of results
            # NOTE: if page number exceeds maximum page result, API automatically returns page 1 over and over again
            # DO NOT LEAVE THE API RUNNING AND MONITOR AT ALL TIMES
            params['page'] += 1
        else:
            print("Failed to retrieve data from the API.")
            break
