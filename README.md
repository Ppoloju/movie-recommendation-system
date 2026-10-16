# Movie Recommendation System in Python

A simple command-line movie recommender written in Python. It keeps a text database of movies with descriptions, lets you browse them, rate what you watch, track what you have already seen, and turns that into personal recommendations.

This project was developed as a case study for the Semester 2 Programming for Problem Solving in Python course.

The code is written in a beginner-friendly style: only basic Python (variables, lists, dictionaries, sets, loops, functions, `if / elif`, file handling and the built-in `random` module).

## Features

### Movie Database

- 200 movies stored in a plain text file (`movies.txt`)
- Three languages: Telugu (64), Hindi (66), English (70)
- 18 genres: Action, Drama, Romance, Comedy, Sci-Fi, Horror, Thriller, Crime, Adventure, Fantasy, Mystery, Family, Sports, War, Biography, Animation, Musical, History
- Every movie carries a year, language, genres, public rating out of 10, keyword tags and a one line description

### Recommendations

- **From my ratings** — your ratings build a genre profile; already seen movies are skipped and the public rating of other people breaks ties
- **Similar to a movie** — a match percentage based on shared genres and tags
- **Surprise me** — a random movie you have not watched yet, shown with full details

### Tracking

- Rate movies 1-10 (a rated movie automatically counts as seen)
- Mark movies as seen without rating them
- Keep a watchlist of titles you want to watch
- Browse with one genre or several at once — movies matching more of your genres are listed first
- Browse by year — type a full year (`2019`) or just part of one (`201` lists 2010-2019)

### Data Management

- File handling for the database and all personal files
- Add a new movie from the menu with every detail, appended to `movies.txt`
- Bad lines in the database are reported and skipped instead of crashing

## How to Run

### Option 1: Using Python 3 (Linux/Mac)

```bash
python3 --version
python3 recommendation.py
```

### Option 2: Using Python (Windows)

```bash
py recommendation.py
```

Note: On some Windows machines `python` opens the Microsoft Store prompt instead of running. Use `py recommendation.py` in that case.

### Option 3: Using an Online Compiler

1. Visit Programiz or OnlineGDB
2. Paste the code from `recommendation.py`
3. Create the `movies.txt` database in the same editor (or use the one from this repository)
4. Click **Run**

Note: Online compilers have limited file access, so the personal files may not persist between runs.

## Usage

The menu is grouped: choose a category first, then an action inside it.

```
MOVIE RECOMMENDATION SYSTEM
  1. Browse movies            -> By genre | By language | By year | All movies
  2. Get recommendations      -> From my ratings | Similar to a movie | Surprise me
  3. My list                  -> Rate a movie | Mark a movie as seen | My watchlist
                                 | Movies I have rated | Movies I have seen
  4. Movie details
  5. Add a movie
  0. Exit
```

Every submenu has `0. Back`, so you never leave the program by accident.

### Why each menu item exists

| Menu item | Context - why it is there |
|---|---|
| **1. Browse movies** | The plain database view. Grouping the four filters (genre, language, year, all) in one submenu keeps the main menu short instead of showing four separate entries. |
| **- By genre** | The most common way to choose a movie. It accepts one genre or several, and lists movies matching more of your genres first, so one answer works for both cases. |
| **- By language** | This project holds Telugu, Hindi and English movies, so filtering by language is a first class choice. |
| **- By year** | Finds the movies of a year you remember (release year, festival, birthday list) without needing a title. Typing part of a year works too, so one prompt covers both a single year and a decade. |
| **- All movies** | Full list sorted by public rating, useful as an overview of the database. |
| **2. Get recommendations** | The reason the program exists. It is a category so the three different methods stay together. |
| **- From my ratings** | Personalised picks: your ratings form the genre profile, seen movies are skipped, and the rating given by other people balances the score. |
| **- Similar to a movie** | For when you already know one movie you like and want more of the same. |
| **- Surprise me** | Helps to decide quickly: one random movie you have not seen, printed with full details. |
| **3. My list** | All your own data lives in one category, so the main menu does not fill up with rating, seen and watchlist actions. |
| **- Rate a movie** | Feeds the recommendation engine. Rating also marks the movie as seen, because you only rate what you watched. |
| **- Mark a movie as seen** | Seen status without a score, for movies you watched but do not want to judge. Seen movies are never recommended again. |
| **- My watchlist** | Movies you intend to watch later, so the program is useful before and after watching. |
| **- Movies I have rated** | Shows your own scores next to the public rating, so you can compare your taste with everyone else's. |
| **- Movies I have seen** | Your watch history at a glance. |
| **4. Movie details** | Shows one complete record: description, tags, public rating, your rating, seen status and watchlist status - everything the recommendations are built on. |
| **5. Add a movie** | Keeps the database growing without editing `movies.txt` by hand. |
| **0. Exit** | Clean way to close the program (Ctrl+C is handled too). |

## Example Session

```
Loaded 200 movies from movies.txt.

======================================================
  MOVIE RECOMMENDATION SYSTEM
======================================================
  1. Browse movies
  2. Get recommendations
  3. My list
  4. Movie details
  5. Add a movie
  0. Exit
======================================================
  Choice: 1
======================================================
  BROWSE MOVIES
======================================================
  1. By genre
  2. By language
  3. By year
  4. All movies
  0. Back
======================================================
  Choice: 1
  Genres: horror
  1. Get Out (2017) - English - Horror, Mystery, Thriller - 7.7/10
  2. The Conjuring (2013) - English - Horror, Thriller - 7.5/10
  3. A Quiet Place (2018) - English - Horror, Sci-Fi - 7.5/10
  4. Stree (2018) - Hindi - Horror, Comedy - 7.1/10
  5. Stree 2 (2024) - Hindi - Horror, Comedy - 7.0/10
  6. Shaitaan (2024) - Hindi - Horror, Thriller - 7.0/10
  7. Nosferatu (2024) - English - Horror, Fantasy - 7.0/10
  8. Bhaagamathie (2018) - Telugu - Horror, Thriller - 6.8/10
  9. Bhool Bhulaiyaa 2 (2022) - Hindi - Horror, Comedy - 6.8/10

  Choice: 0                       (back to the main menu)

  Choice: 3                       (My list)
  Choice: 1                       (Rate a movie)
  Which movie do you want to rate: inception
  Your score for "Inception" (1-10): 9.2
  Saved: Inception = 9.2/10
  (a rated movie counts as seen from now on)

  Choice: 0                       (back)
  Choice: 2                       (Get recommendations)
  Choice: 1                       (From my ratings)
  Based on 1 of your ratings, 1 already seen movie(s) skipped:

  1. The Matrix (1999) - English - Sci-Fi, Action  8.7/10 by others
  2. Guardians of the Galaxy Vol. 3 (2023) - English - Action, Sci-Fi  7.9/10 by others
  3. Tenet (2020) - English - Sci-Fi, Thriller  7.3/10 by others
  4. No Time to Die (2021) - English - Action, Thriller  7.3/10 by others
  5. Salaar: Part 1 - Ceasefire (2023) - Telugu - Action, Thriller  7.2/10 by others
  6. Nannaku Prematho (2016) - Telugu - Action, Thriller  7.2/10 by others
  7. Jawan (2023) - Hindi - Action, Thriller  7.0/10 by others
  8. Sarrainodu (2016) - Telugu - Action, Thriller  7.0/10 by others
  9. 24 (2016) - Telugu - Sci-Fi, Thriller  7.0/10 by others
  10. Pushpa 2: The Rule (2024) - Telugu - Action, Thriller  7.0/10 by others

  Choice: 0                       (back)
  Choice: 4                       (Movie details)
  Title: interstellar

  Interstellar (2014)
  Language      : English
  Genres        : Sci-Fi, Adventure, Drama
  Tags          : space, time, father, science
  Rating        : 8.7/10 by others
  Your rating   : not rated yet
  Seen          : no
  Story         : Explorers cross a wormhole searching for a new home for humanity.

  Choice: 0
Goodbye! Happy watching.
```

## How It Works

### Data Structure

Each movie is a dictionary inside a list:

```python
movie = {
    "title": "Baahubali: The Beginning",
    "year": 2015,
    "language": "Telugu",
    "genres": ["Action", "Drama", "Adventure", "Fantasy"],
    "rating": 8.0,
    "tags": ["war", "king", "kingdom", "warrior"],
    "description": "A rebel searches for the truth about a stolen kingdom.",
}
```

The database uses one line per movie, seven fields separated by `|`:

```
Title | Year | Language | Genres | Rating | Tags | Description
Baahubali: The Beginning | 2015 | Telugu | Action,Drama,Adventure,Fantasy | 8.0 | war,king,kingdom,warrior | A rebel searches for the truth about a stolen kingdom.
```

### Menus

`show_menu()` prints any menu from a list of strings, and every submenu runs its own `while True` loop with `0. Back`. The main menu therefore never grows when a feature is added - it just becomes one more entry in a submenu.

### Key Functions

**Files**
- `load_movies()` - reads `movies.txt` with `open()` and returns a list of dictionaries
- `split_words()` - turns a field like `Action,Drama` into `["Action", "Drama"]`
- `load_lines()` / `write_lines()` - read and write any text file line by line
- `load_ratings()` / `save_rating()` - handle `my_ratings.txt`
- `watched_titles()` - merges `seen.txt` and your rated titles into one list

**Helpers**
- `show_menu()`, `read_number()` - menu printing and safe number input
- `find_movies()` / `find_exact()` / `choose_movie()` - title lookup, asking you when several titles match
- `movie_line()` / `show_movies()` - printing lists with the `[seen]` tag
- `show_details()` - the full record of one movie, including its description

**Recommendation logic**
- `similarity()` - scores two movies between 0.0 and 1.0
- `similar_movies()` - prints the top matches for the movie you chose
- `genre_scores()` - turns your ratings into a score per genre
- `recommend()` - ranks unseen movies using your profile and the public rating
- `surprise_me()` - one random unseen movie with full details

**Menu actions**
- `browse_by_genre()`, `browse_by_language()`, `browse_by_year()`, `browse_all()`
- `rate_movie()`, `mark_seen()`, `show_watchlist()`, `show_rated()`, `show_seen()`
- `movie_details()`, `add_movie()`
- `main()` plus the three submenu functions

### How a recommendation is scored

**Similarity** to a movie you like:

```
same items = 2 * common genres + common tags
all items  = 2 * genres in both movies + tags in both movies
score      = same items / all items        (+0.1 if both are the same language)
```

Genres count double because they matter more than keyword tags.

**From my ratings** combines the three signals:

1. **My ratings** - each rating adds its score to every genre of that movie, so a 9/10 makes those genres count more.
2. **Seen status** - anything you rated or marked as seen is skipped, so you are only offered new movies.
3. **Rating by others** - the public rating is added to the taste score and shown on every line, so a well liked movie wins ties.

```
taste  = (sum of your genre scores) / (number of its genres)
final  = taste + public rating
```

**Multi genre browsing** counts how many of the genres you typed each movie has, lists matches with more genres first and then by public rating.

### Data Persistence

| File | Purpose |
|---|---|
| `movies.txt` | the movie database (read at startup, appended when you add a movie) |
| `my_ratings.txt` | your scores, written after every rating, format `Title\|score` |
| `seen.txt` | movies you marked as seen, one title per line |
| `watchlist.txt` | titles you want to watch, one title per line |

All files are plain text kept in the same folder as the program. The personal files are created automatically the first time you use them, and git ignores them (see below) so only the database and the code are shared.

## Project Structure

```
movies-recommendation/
├── recommendation.py          # Main source code
├── movies.txt                 # Movie database with descriptions
├── README.md                  # Documentation
├── .gitignore                 # Rules below
├── my_ratings.txt             # Your ratings (auto-generated)
├── seen.txt                   # Movies you have watched (auto-generated)
└── watchlist.txt              # Your watchlist (auto-generated)
```

`.gitignore` keeps the repository clean - none of these are committed:

```
__pycache__/   *.pyc              Python caches
my_ratings.txt  seen.txt  watchlist.txt     your personal files
```

## Technical Details

### Modules Used

Only one extra module, from the Python standard library:

- `random` - for the surprise pick (`random.choice()`)

Everything else is core Python: `list`, `dict`, `set`, `sorted()`, `max()`, `min()`, `len()`, `range()`, string methods (`split`, `strip`, `lower`, `title`), `with open()` file handling and `try / except`. Nothing has to be installed with `pip`.

### Constants

- `DATA_FILE = "movies.txt"`, `RATINGS_FILE = "my_ratings.txt"`, `SEEN_FILE = "seen.txt"`, `WATCHLIST_FILE = "watchlist.txt"`
- 7 fields per line in `movies.txt`
- Ratings are accepted in the range 1 - 10, years in the range 1900 - 2100

### Compatibility

- Python 3.6 or newer (tested on Python 3.14)
- Works on Linux, macOS and Windows
- No third-party dependencies, so it also runs in online Python compilers
