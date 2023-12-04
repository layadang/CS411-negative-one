import re

# The result string
result_string = """Based on the movies you mentioned, here are 10 other movies you may also enjoy:

1. Fight Club (1999)
2. The Matrix (1999)
3. Interstellar (2014)
4. Goodfellas (1990)
5. The Departed (2006)
6. Memento (2000)
7. The Prestige (2006)
8. Seven (1995)
9. The Usual Suspects (1995)
10. Heat (1995)
"""

# Use regular expression to match movie names and years
movie_matches = re.findall(r'\d+\.\s+(.+)\s+\((\d{4})\)', result_string)

# Create a list of movie objects with names and years
movies_list = [{"title": match[0], "year": int(match[1])} for match in movie_matches]

# Print the resulting list
print(movies_list)
