# Re-importing pandas and reloading the dataset, as the code execution state was reset
import pandas as pd

# Load the dataset again
new_file_path = 'model_training/api_response_cleaned_2.csv'
new_data = pd.read_csv(new_file_path)

# Simplifying the genre labels so that each movie has only one genre
# The simplest approach is to take the first genre listed for each movie
new_data['simplified_genre'] = new_data['genre'].apply(lambda x: x.split(',')[0])

# Checking the distribution of the simplified genres
simplified_genre_distribution = new_data['simplified_genre'].value_counts()

simplified_genre_distribution.head(10)  # Displaying the top 10 genres for brevity