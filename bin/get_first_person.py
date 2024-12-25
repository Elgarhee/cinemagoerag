#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
get_first_movie.py

Usage: get_first_movie "movie title"
Search for the given title and print the exact match if available.
"""

import sys

# Import the Cinemagoer package.
try:
    import imdb
except ImportError:
    print('You need to install the Cinemagoer package!')
    sys.exit(1)

if len(sys.argv) != 2:
    print('Only one argument is required:')
    print('  %s "movie title"' % sys.argv[0])
    sys.exit(2)

title = sys.argv[1].strip()

# Initialize IMDb object
i = imdb.IMDb()

try:
    # Perform the search and get the results (a list of Movie objects).
    results = i.search_movie(title)
except imdb.IMDbError as e:
    print("Probably you're not connected to the Internet. Complete error report:")
    print(e)
    sys.exit(3)

if not results:
    print(f'No matches for "{title}", sorry.')
    sys.exit(0)

# Attempt to find an exact match
exact_match = None
title_lower = title.lower()
for movie in results:
    movie_title = movie.get('title', '').lower()
    movie_original_title = movie.get('original title', '').lower()
    movie_year = movie.get('year', '')

    # Check for exact match (with or without year in the title)
    if title_lower == f"{movie_title} {movie_year}".lower() or title_lower == movie_title.lower():
        exact_match = movie
        break
    if title_lower == f"{movie_original_title} {movie_year}".lower() or title_lower == movie_original_title.lower():
        exact_match = movie
        break

if exact_match:
    # Update and print exact match details
    i.update(exact_match)
    print(f'Exact match found for "{title}":')
    print(exact_match.summary())
else:
    # Print the first result as the best match
    print(f'No exact match found for "{title}". Showing the best matches instead:')
    for idx, movie in enumerate(results[:5], start=1):  # Show the first 5 matches
        print(f"{idx}. {movie.get('title', 'Unknown')} ({movie.get('year', 'Unknown')})")
