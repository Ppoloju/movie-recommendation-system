#!/usr/bin/env python3
"""
Movie Recommendation System
----------------------------
A simple movie recommender that runs in the terminal.

The menu is grouped: first choose a category, then an action inside it.

Data files (plain text, kept in the same folder):
    movies.txt       the movie database
                     Title | Year | Language | Genres | Rating | Tags | Description
    my_ratings.txt   movies you have rated        Title|score
    seen.txt         movies you have watched     one title per line
    watchlist.txt    movies you want to watch     one title per line

Run:   python recommendation.py      (on Windows:  py recommendation.py)
"""

import random          # used for the surprise pick

DATA_FILE = "movies.txt"
RATINGS_FILE = "my_ratings.txt"
SEEN_FILE = "seen.txt"
WATCHLIST_FILE = "watchlist.txt"


# ---------------------------------------------------------------------------
# 1. FILE HANDLING
# ---------------------------------------------------------------------------
def split_words(text, title_case=False):
    """Split a field like 'Action,Drama' or 'action drama' into a list."""
    text = text.replace(",", " ")
    words = []
    for word in text.split():
        if title_case:
            word = word.title()
        words.append(word)
    return words


def load_movies():
    """Read movies.txt and return a list of dictionaries."""
    movies = []
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line == "" or line.startswith("#"):
                continue                        # skip empty lines and comments

            parts = line.split("|")
            if len(parts) != 7:
                print("  (skipped bad line: " + line + ")")
                continue

            try:
                year = int(parts[1])
                rating = float(parts[4])
            except ValueError:
                print("  (skipped bad line: " + line + ")")
                continue

            movie = {
                "title": parts[0].strip(),
                "year": year,
                "language": parts[2].strip(),
                "genres": split_words(parts[3], title_case=True),
                "rating": rating,
                "tags": split_words(parts[5]),
                "description": parts[6].strip(),
            }
            movies.append(movie)
    return movies


def load_lines(file_name):
    """Read a text file and return its non-empty lines as a list."""
    try:
        file = open(file_name, "r", encoding="utf-8")
    except FileNotFoundError:
        return []                       # the file has not been made yet
    lines = []
    for line in file:
        line = line.strip()
        if line != "":
            lines.append(line)
    file.close()
    return lines


def write_lines(file_name, lines):
    """Save a list of strings into a text file (one string per line)."""
    with open(file_name, "w", encoding="utf-8") as file:
        for line in lines:
            file.write(line + "\n")


def load_ratings():
    """Read my_ratings.txt and return a dictionary {title: score}."""
    ratings = {}
    for line in load_lines(RATINGS_FILE):
        if "|" in line:
            title, score = line.split("|", 1)
            try:
                ratings[title.strip()] = float(score)
            except ValueError:
                pass                    # ignore a broken line
    return ratings


def save_rating(title, score):
    """Add one rating to my_ratings.txt."""
    ratings = load_ratings()
    ratings[title] = score
    lines = []
    for name in ratings:
        lines.append(name + "|" + str(ratings[name]))
    write_lines(RATINGS_FILE, lines)


def watched_titles():
    """Titles you have watched: marked as seen OR already rated."""
    result = load_lines(SEEN_FILE)
    for title in load_ratings():
        if title not in result:
            result.append(title)
    return result


# ---------------------------------------------------------------------------
# 2. HELPERS
# ---------------------------------------------------------------------------
def show_menu(title, options, back_label):
    """Print a numbered menu (0 is always the way back)."""
    print("")
    print("=" * 54)
    print("  " + title)
    print("=" * 54)
    for i in range(len(options)):
        print("  " + str(i + 1) + ". " + options[i])
    print("  0. " + back_label)
    print("=" * 54)


def read_number(prompt, low, high):
    """Ask until the user types a number between low and high."""
    while True:
        text = input(prompt).strip()
        try:
            value = float(text)
        except ValueError:
            print("  Please enter a number.")
            continue
        if low <= value <= high:
            return value
        print("  Please enter a number from " + str(low) + " to " + str(high) + ".")


def by_rating(movie):
    """Key used to sort movies: highest public rating first."""
    return movie["rating"]


def sort_movies(movies):
    return sorted(movies, key=by_rating, reverse=True)


def find_movies(movies, keyword):
    """Return every movie whose title contains the keyword."""
    keyword = keyword.lower()
    found = []
    for movie in movies:
        if keyword in movie["title"].lower():
            found.append(movie)
    return found


def find_exact(movies, title):
    """Return the movie whose title is exactly this one."""
    for movie in movies:
        if movie["title"] == title:
            return movie
    return None


def choose_movie(movies, keyword):
    """Return ONE movie, asking the user when several titles match."""
    matches = find_movies(movies, keyword)
    if len(matches) == 0:
        print('  No movie found for "' + keyword + '".')
        return None
    if len(matches) == 1:
        return matches[0]
    print("  More than one movie matches your input:")
    show_movies(matches)
    number = int(read_number("  Choose a number: ", 1, len(matches)))
    return matches[number - 1]


def movie_line(number, movie, watched, extra="", show_rating=True):
    """One printed line for a movie: number, title, facts and status."""
    text = (str(number) + ". " + movie["title"] +
            " (" + str(movie["year"]) + ") - " +
            movie["language"] + " - " +
            ", ".join(movie["genres"]))
    if show_rating:
        text = text + " - " + str(movie["rating"]) + "/10"
    if extra != "":
        text = text + "  " + extra
    if movie["title"] in watched:
        text = text + "  [seen]"
    return text


def show_movies(movies):
    """Print a list of movies in a simple numbered format."""
    if len(movies) == 0:
        print("  (no movies to show)")
        return
    watched = watched_titles()
    for i in range(len(movies)):
        print("  " + movie_line(i + 1, movies[i], watched))


def show_details(movie):
    """Print everything known about one movie."""
    ratings = load_ratings()
    watched = watched_titles()
    watchlist = load_lines(WATCHLIST_FILE)

    print("")
    print("  " + movie["title"] + " (" + str(movie["year"]) + ")")
    print("  Language      : " + movie["language"])
    print("  Genres        : " + ", ".join(movie["genres"]))
    print("  Tags          : " + ", ".join(movie["tags"]))
    print("  Rating        : " + str(movie["rating"]) + "/10 by others")
    if movie["title"] in ratings:
        print("  Your rating   : " + str(ratings[movie["title"]]) + "/10")
    else:
        print("  Your rating   : not rated yet")
    if movie["title"] in watched:
        print("  Seen          : yes")
    else:
        print("  Seen          : no")
    if movie["title"] in watchlist:
        print("  On watchlist  : yes")
    print("  Story         : " + movie["description"])
    print("")


# ---------------------------------------------------------------------------
# 3. RECOMMENDATION LOGIC
# ---------------------------------------------------------------------------
def similarity(a, b):
    """How similar two movies are, between 0.0 and 1.0.

    Genres count double because they matter more than tags,
    and movies of the same language get a small bonus.
    """
    genres_a, genres_b = set(a["genres"]), set(b["genres"])
    tags_a, tags_b = set(a["tags"]), set(b["tags"])

    same = len(genres_a & genres_b) * 2 + len(tags_a & tags_b)
    total = len(genres_a | genres_b) * 2 + len(tags_a | tags_b)
    if total == 0:
        return 0.0
    score = same / total
    if a["language"] == b["language"]:
        score = score + 0.1
    if score > 1.0:
        score = 1.0
    return score


def get_score(pair):
    """Key used to sort (score, movie) pairs: highest score first."""
    return pair[0]


def similar_movies(movies, chosen, count=5):
    """The 'count' movies most similar to the chosen one."""
    scores = []
    for movie in movies:
        if movie["title"] != chosen["title"]:
            scores.append((similarity(chosen, movie), movie))
    scores.sort(key=get_score, reverse=True)

    watched = watched_titles()
    for i in range(min(count, len(scores))):
        score, movie = scores[i]
        extra = str(int(score * 100)) + "% match | " + str(movie["rating"]) + "/10 by others"
        print("  " + movie_line(i + 1, movie, watched, extra, show_rating=False))
    print("")


def genre_scores(movies, ratings):
    """How much you like every genre, based on the movies you rated."""
    scores = {}
    for title in ratings:
        movie = find_exact(movies, title)
        if movie is None:
            continue
        for genre in movie["genres"]:
            scores[genre] = scores.get(genre, 0) + ratings[title]
    return scores


def recommend(movies):
    """Recommendations from your ratings, skipping what you have already seen.

    Uses three things: your own ratings (the genre profile),
    your seen status (already watched movies are skipped)
    and the rating given by other people (to break ties).
    """
    ratings = load_ratings()
    if len(ratings) == 0:
        print("  You have not rated any movie yet.")
        print("  Choose My list - Rate a movie and rate 2 or 3 movies first.")
        return

    watched = watched_titles()
    profile = genre_scores(movies, ratings)

    result = []
    skipped = 0
    for movie in movies:
        if movie["title"] in watched:
            skipped = skipped + 1
            continue
        total = 0
        for genre in movie["genres"]:
            total = total + profile.get(genre, 0)
        taste = total / len(movie["genres"])
        result.append((taste + movie["rating"], movie))

    result.sort(key=get_score, reverse=True)
    if len(result) == 0:
        print("  You have seen every movie in the database!")
        return

    print("  Based on " + str(len(ratings)) + " of your ratings, " +
          str(skipped) + " already seen movie(s) skipped:")
    print("")
    for i in range(min(10, len(result))):
        score, movie = result[i]
        print("  " + movie_line(i + 1, movie, [],
                                str(movie["rating"]) + "/10 by others",
                                show_rating=False))
    print("")


def surprise_me(movies):
    """A random movie you have not watched yet, with full details."""
    watched = watched_titles()
    fresh = []
    for movie in movies:
        if movie["title"] not in watched:
            fresh.append(movie)
    if len(fresh) == 0:
        fresh = movies
    print("  Tonight's pick:")
    show_details(random.choice(fresh))


# ---------------------------------------------------------------------------
# 4. MENU ACTIONS  (each one is used by a submenu)
# ---------------------------------------------------------------------------
def browse_by_genre(movies):
    """Genre filter. Accepts one genre or several, e.g. Action,Drama."""
    text = input("  Genres: ").strip()
    wanted = split_words(text)
    if len(wanted) == 0:
        print("  No genre entered.")
        return
    wanted = [g.lower() for g in wanted]

    matched = []
    for movie in movies:
        hits = 0
        for genre in movie["genres"]:
            if genre.lower() in wanted:
                hits = hits + 1
        if hits > 0:
            matched.append((hits, movie))
    matched.sort(key=match_key, reverse=True)

    if len(matched) == 0:
        print("  (no movies found for those genres)")
        return

    watched = watched_titles()
    print("")
    for i in range(len(matched)):
        hits, movie = matched[i]
        extra = ""
        if len(wanted) > 1:
            extra = "(" + str(hits) + "/" + str(len(wanted)) + " genres)"
        print("  " + movie_line(i + 1, movie, watched, extra))
    print("")


def match_key(pair):
    """Key for genre matches: most matching genres first, then rating."""
    return (pair[0], pair[1]["rating"])


def browse_by_language(movies):
    language = input("  Language: ").strip().lower()
    found = []
    for movie in movies:
        if movie["language"].lower() == language:
            found.append(movie)
    if len(found) == 0:
        print("  (no movies found)")
        return
    print("")
    show_movies(sort_movies(found))
    print("")


def browse_by_year(movies):
    """Year search. Digits only, and part of a year works too (201 -> 2010-2019)."""
    text = input("  Year: ").strip()
    if text == "" or not text.isdigit():
        print("  Please enter a year using digits, for example 2019.")
        return
    found = []
    for movie in movies:
        if text in str(movie["year"]):
            found.append(movie)
    if len(found) == 0:
        print("  (no movies found for that year)")
        return
    print("")
    show_movies(sort_movies(found))
    print("")


def browse_all(movies):
    print("")
    show_movies(sort_movies(movies))
    print("")


def show_similar(movies):
    keyword = input("  Title you liked: ").strip()
    chosen = choose_movie(movies, keyword)
    if chosen is None:
        return
    print("")
    print('  Movies similar to "' + chosen["title"] + '":')
    similar_movies(movies, chosen, 5)


def rate_movie(movies):
    keyword = input("  Which movie do you want to rate: ").strip()
    chosen = choose_movie(movies, keyword)
    if chosen is None:
        return
    score = read_number('  Your score for "' + chosen["title"] + '" (1-10): ', 1, 10)
    save_rating(chosen["title"], score)
    print("  Saved: " + chosen["title"] + " = " + str(score) + "/10")
    print("  (a rated movie counts as seen from now on)")


def mark_seen(movies):
    keyword = input("  Title: ").strip()
    chosen = choose_movie(movies, keyword)
    if chosen is None:
        return
    seen = load_lines(SEEN_FILE)
    if chosen["title"] in seen:
        print("  Already marked as seen.")
        return
    seen.append(chosen["title"])
    write_lines(SEEN_FILE, seen)
    print('  Marked "' + chosen["title"] + '" as seen.')


def show_rated(movies):
    ratings = load_ratings()
    if len(ratings) == 0:
        print("  You have not rated any movie yet.")
        return
    print("")
    for title in ratings:
        movie = find_exact(movies, title)
        line = "  " + title + "  - you: " + str(ratings[title]) + "/10"
        if movie is not None:
            line = line + " - others: " + str(movie["rating"]) + "/10"
        print(line)
    print("")


def show_seen(movies):
    watched = watched_titles()
    if len(watched) == 0:
        print("  You have not watched anything yet.")
        return
    print("")
    print("  You have seen " + str(len(watched)) + " movie(s):")
    for title in watched:
        print("  - " + title)
    print("")


def show_watchlist(movies):
    items = load_lines(WATCHLIST_FILE)
    print("  Your watchlist:")
    if len(items) == 0:
        print("    (empty)")
    for name in items:
        print("    - " + name)

    keyword = input("  Add a movie? Type a title, or press Enter to go back: ").strip()
    if keyword == "":
        return
    chosen = choose_movie(movies, keyword)
    if chosen is None:
        return
    if chosen["title"] in items:
        print("  Already on your watchlist.")
        return
    items.append(chosen["title"])
    write_lines(WATCHLIST_FILE, items)
    print('  Added "' + chosen["title"] + '" to your watchlist.')


def movie_details(movies):
    keyword = input("  Title: ").strip()
    chosen = choose_movie(movies, keyword)
    if chosen is None:
        return
    show_details(chosen)


def add_movie():
    """Append a new movie to movies.txt with every detail."""
    print("  Press Enter at the title to cancel:")
    title = input("  Title: ").strip()
    if title == "":
        print("  Cancelled.")
        return
    year = int(read_number("  Year (1900-2100): ", 1900, 2100))
    language = input("  Language: ").strip()
    if language == "":
        print("  Cancelled.")
        return
    genres = input("  Genres: ").strip()
    if genres == "":
        print("  Cancelled.")
        return
    tags = input("  Tags: ").strip()
    rating = read_number("  Rating (0-10): ", 0, 10)
    description = input("  Description: ").strip()

    line = (title + " | " + str(year) + " | " + language + " | " +
            genres + " | " + str(rating) + " | " + tags + " | " +
            description + "\n")
    with open(DATA_FILE, "a", encoding="utf-8") as file:
        file.write(line)
    print('  Added "' + title + '" to ' + DATA_FILE + ".")


# ---------------------------------------------------------------------------
# 5. MENUS AND MAIN PROGRAM
# ---------------------------------------------------------------------------
def menu_browse(movies):
    while True:
        show_menu("BROWSE MOVIES",
                  ["By genre", "By language", "By year", "All movies"], "Back")
        choice = int(read_number("  Choice: ", 0, 4))
        if choice == 0:
            return
        elif choice == 1:
            browse_by_genre(movies)
        elif choice == 2:
            browse_by_language(movies)
        elif choice == 3:
            browse_by_year(movies)
        elif choice == 4:
            browse_all(movies)


def menu_recommend(movies):
    while True:
        show_menu("GET RECOMMENDATIONS",
                  ["From my ratings", "Similar to a movie", "Surprise me"], "Back")
        choice = int(read_number("  Choice: ", 0, 3))
        if choice == 0:
            return
        elif choice == 1:
            recommend(movies)
        elif choice == 2:
            show_similar(movies)
        elif choice == 3:
            surprise_me(movies)


def menu_my_list(movies):
    while True:
        show_menu("MY LIST",
                  ["Rate a movie", "Mark a movie as seen", "My watchlist",
                   "Movies I have rated", "Movies I have seen"], "Back")
        choice = int(read_number("  Choice: ", 0, 5))
        if choice == 0:
            return
        elif choice == 1:
            rate_movie(movies)
        elif choice == 2:
            mark_seen(movies)
        elif choice == 3:
            show_watchlist(movies)
        elif choice == 4:
            show_rated(movies)
        elif choice == 5:
            show_seen(movies)


MAIN_MENU = ["Browse movies", "Get recommendations", "My list",
             "Movie details", "Add a movie"]


def main():
    movies = load_movies()
    print("Loaded " + str(len(movies)) + " movies from " + DATA_FILE + ".")

    while True:
        show_menu("MOVIE RECOMMENDATION SYSTEM", MAIN_MENU, "Exit")
        choice = int(read_number("  Choice: ", 0, 5))

        if choice == 0:
            print("Goodbye! Happy watching.")
            break
        elif choice == 1:
            menu_browse(movies)
        elif choice == 2:
            menu_recommend(movies)
        elif choice == 3:
            menu_my_list(movies)
        elif choice == 4:
            movie_details(movies)
        elif choice == 5:
            add_movie()
            movies = load_movies()      # reload so the new movie can be found


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram stopped. Bye!")
