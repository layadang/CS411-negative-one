from google.cloud import aiplatform
import os

# Set Google credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "secret/vertex.json"

# Set your project and location
project = "cas-411-negative-one"
location = "us-central1"

# Initialize AI Platform client
aiplatform.init(project=project, location=location)

# Specify the new model ID
model_id = "8606926444695650304"

# Get the model endpoint
endpoint = aiplatform.Endpoint(model_id)

# Make predictions using the endpoint
# Adjust the input data format based on your model's expected input
input_data = [
  {
    "title": "The Hunger Games",
    "year": "2012",
    "genre": "Action, Adventure, Science Fiction",
    "plot": "In a dystopian future, Katniss Everdeen volunteers to take her younger sister's place in a deadly televised competition.",
    "prompt": "DON'T GIVE GENRE. Based on this movie, please recommend 10 similar movies."
  },
  {
    "title": "Catching Fire",
    "year": "2013",
    "genre": "Action, Adventure, Science Fiction",
    "plot": "Katniss Everdeen and Peeta Mellark become symbols of rebellion against the Capitol after they win the 74th Hunger Games.",
    "prompt": "DON'T GIVE GENRE. Based on this movie, please recommend 10 similar movies."
  },
  {
    "title": "Mockingjay",
    "year": "2014",
    "genre": "Action, Adventure, Science Fiction",
    "plot": "Katniss Everdeen becomes the Mockingjay, a symbol of hope for the rebellion against the Capitol.",
    "prompt": "DON'T GIVE GENRE. Based on this movie, please recommend 10 similar movies."
  },
  {
    "title": "Divergent",
    "year": "2014",
    "genre": "Action, Adventure, Science Fiction",
    "plot": "Tris Prior discovers she is Divergent and must choose a faction to belong to.",
    "prompt": "DON'T GIVE GENRE. Based on this movie, please recommend 10 similar movies."
  },
  {
    "title": "Insurgent",
    "year": "2015",
    "genre": "Action, Adventure, Science Fiction",
    "plot": "Tris Prior and the Divergents continue their fight against the Erudite.",
    "prompt": "DON'T GIVE GENRE. Based on this movie, please recommend 10 similar movies."
  },
  {
    "title": "Allegiant",
    "year": "2016",
    "genre": "Action, Adventure, Science Fiction",
    "plot": "Tris Prior must make a choice that will determine the fate of humanity.",
    "prompt": "DON'T GIVE GENRE. Based on this movie, please recommend 10 similar movies."
  },
  {
    "title": "The Maze Runner",
    "year": "2014",
    "genre": "Action, Adventure, Science Fiction",
    "plot": "Thomas is dropped into a mysterious maze.",
    "prompt": "DON'T GIVE GENRE. Based on this movie, please recommend 10 similar movies."
  },
  {
    "title": "The Scorch Trials",
    "year": "2015",
    "genre": "Action, Adventure, Science Fiction",
    "plot": "Thomas and the other Gladers escape the Maze and enter the Scorch.",
    "prompt": "DON'T GIVE GENRE. Based on this movie, please recommend 10 similar movies."
  },
  {
    "title": "The Maze Runner: The Death Cure",
    "year": "2017",
    "genre": "Action, Adventure, Science Fiction",
    "plot": "Thomas and the other Gladers must find a way to stop WCKD.",
    "prompt": "DON'T GIVE GENRE. Based on this movie, please recommend 10 similar movies."
  },
  {
    "title": "Percy Jackson & the Olympians: The Lightning Thief",
    "year": "",
    "genre": "",
    "plot": "",
    "prompt": "DON'T GIVE GENRE. Based on this movie, please recommend 10 similar movies."
  }
]

flattened_input_data = []
for instance in input_data:
  flattened_input_data.append(instance)

response = endpoint.predict(instances=flattened_input_data)

# Log the request and response
print("Request:", input_data)
print("Response:", response)
