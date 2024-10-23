import csv
import re
from tabulate import tabulate
from colorama import Fore, Style, init
import matplotlib.pyplot as plt

# Sets up colorama for colored terminal output
init(autoreset=True)

# Loads CSV data from a file
def load_csv(filename):
    try:
        with open(filename, mode='r', encoding='ISO-8859-1') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)  # Grab the headers from the first line
            data = [dict(zip(headers, row)) for row in csv_reader if row]  # Create a list of dictionaries for each row
        return data
    except FileNotFoundError:
        print(Fore.RED + "Oops! The file wasn't found.")  # Show error if file is missing
        return []  # Return an empty list if the file isn't there

# Cleans up votes to make sure they're integers
def clean_votes(votes_str):
    cleaned_str = re.sub(r'\D', '', votes_str)  # Remove non-digit characters
    return int(cleaned_str) if cleaned_str else 0  # Convert to int or return 0 if empty

# Cleans up ratings and convert them to floats
def clean_rating(rating):
    try:
        return float(rating.strip()) if rating.strip() else 0.0  # Convert to float or return 0.0 if empty
    except ValueError:
        return 0.0  # Return 0.0 for any bad ratings

# Makes sure the year is a four-digit number
def clean_year(year_str):
    cleaned_str = re.sub(r'\D', '', year_str)  # Remove non-digit characters
    return cleaned_str if len(cleaned_str) == 4 else '0'  # Return the year or '0' if it's not valid

# Filters movies based on search term, rating, genre, and director
def filter_movies(data, search_term, rating_filter=None, genre_filter=None, director_filter=None):
    filtered_movies = []

    # Checks if the rating filter is valid
    if rating_filter:
        operator = rating_filter[0]
        try:
            rating_value = float(rating_filter[1:])  # Convert filter to float
        except ValueError:
            print(Fore.RED + "Uh-oh! Invalid rating filter. Use '<' or '>' followed by a number.")
            return filtered_movies  # Return empty if filter is invalid

    # Cleans up the search term for year filtering
    cleaned_search_term = clean_year(search_term)

    for row in data:
        # Checks for exact matches for year and genre
        matches_year = clean_year(row.get('Year', '')) == cleaned_search_term
        matches_genre = genre_filter.lower() in row.get('Genre', '').lower() if genre_filter else True
        matches_director = director_filter.lower() in row.get('Director', '').lower() if director_filter else True

        # Fuzzy matches for movie name
        matches_name = search_term.lower() in row.get('Name', '').lower()

        # If it matches then adds it to the list
        if (matches_year or matches_name) and matches_genre and matches_director:
            if rating_filter:
                if operator == '>' and clean_rating(row.get('Rating', '0')) > rating_value:
                    filtered_movies.append(row)
                elif operator == '<' and clean_rating(row.get('Rating', '0')) < rating_value:
                    filtered_movies.append(row)
            else:
                filtered_movies.append(row)  # Just add it if there's no rating filter

    return filtered_movies

# Sorts movies by a specific attribute
def sort_movies(movies, sort_by="rating"):
    if sort_by == "rating":
        movies.sort(key=lambda x: clean_rating(x.get('Rating', '0')), reverse=True)
    elif sort_by == "votes":
        movies.sort(key=lambda x: clean_votes(x.get('Votes', '0')), reverse=True)
    elif sort_by == "year":
        movies.sort(key=lambda x: clean_year(x.get('Year', '0')), reverse=True)
    return movies

# Visualizes the top n movies
def visualize_top_movies(movies, top_n=10):
    top_movies = sort_movies(movies, sort_by="rating")[:top_n]

    names = [movie['Name'] for movie in top_movies]
    ratings = [clean_rating(movie.get('Rating', '0')) for movie in top_movies]

    plt.figure(figsize=(10, 6))
    plt.barh(names, ratings, color='skyblue')  # Changed 'sky blue' to 'skyblue'
    plt.xlabel("Rating")
    plt.ylabel("Movie")
    plt.title(f"Top {top_n} Movies by Rating")
    plt.gca().invert_yaxis()  # Show highest rating at the top
    plt.show()

# Main function to run the program
def main():
    filename = r"C:\CODSOFT INTERN\CSV FILES CODSOFT\IMDb Movies India.csv"  # Update with your CSV file path
    data = load_csv(filename)

    if not data:
        return  # Exit if no data found

    print(Fore.YELLOW + Style.BRIGHT + "Welcome to the IMDb Movie Search!\n")

    # Ask for search input
    search_term = input(Fore.YELLOW + "Enter SEARCH term (movie name, year)...(press ENTER to skip): ")
    rating_filter = input(Fore.YELLOW + "Enter RATING filter (< or > followed by a number)...(press ENTER to skip): ")
    genre_filter = input(Fore.YELLOW + "Enter GENRE to filter by...(press ENTER to skip): ")
    director_filter = input(Fore.YELLOW + "Enter DIRECTOR to filter by...(press ENTER to skip): ")

    filtered_result = filter_movies(data, search_term, rating_filter, genre_filter, director_filter)

    if filtered_result:
        print(Fore.YELLOW + f"\nMovies found for {search_term} {rating_filter} {genre_filter} {director_filter}:\n")

        sort_choice = input(
            Fore.YELLOW + "Do you want to sort by 'rating', 'votes', or 'year'?.(press ENTER to skip): ").lower()
        if sort_choice:
            filtered_result = sort_movies(filtered_result, sort_by=sort_choice)

        # Prepare and display the movie table
        movie_table = []
        for movie in filtered_result:
            movie_table.append([
                movie['Name'],
                movie['Year'],
                movie['Genre'],
                movie['Director'],
                movie.get('Actor 1', 'N/A'),
                movie.get('Actor 2', 'N/A'),
                movie.get('Actor 3', 'N/A'),
                movie.get('Rating', 'N/A'),
                movie.get('Votes', 'N/A')
            ])

        print(tabulate(movie_table,
                       headers=['Movie Name', 'Year', 'Genre', 'Director', 'Actor 1', 'Actor 2', 'Actor 3', 'Rating', 'Votes'],
                       tablefmt='fancy_grid'))

        visualize_choice = input(Fore.YELLOW + "Wanna see a visual of the top movies? (y/n): ").lower()
        if visualize_choice == "y":
            top_n = int(input(Fore.YELLOW + "How many top movies do you want to see? "))
            visualize_top_movies(filtered_result, top_n=top_n)

    else:
        print(Fore.RED + "Sorry! No movies found... Check your search term or filters.")

# Runs the main function
if __name__ == '__main__':
    main()
