from music import music_db
from match import match
from typing import List, Tuple, Callable, Any

# The projection functions, that give us access to certain parts of a "music" (a tuple)
def get_title(music: Tuple[str, str, int, List[str]]) -> str:
    return music[0]


def get_artist(music: Tuple[str, str, int, List[str]]) -> str:
    return music[1]


def get_year(music: Tuple[str, str, int, List[str]]) -> int:
    return music[2]


def get_genres(music: Tuple[str, str, int, List[str]]) -> List[str]:
    return music[3]


# --- Actions ---


def songs_by_year(matches: List[str]) -> List[str]:
    year = int(matches[0])
    result = []
    for music in music_db:
        if get_year(music) == year:
            result.append(get_title(music))
    return result

def songs_by_year_range(matches: List[str]) -> List[str]:
    start, end = int(matches[0]), int(matches[1])
    result = []
    for music in music_db:
        if start <= get_year(music) <= end:
            result.append(get_title(music))
    return result


def songs_before_year(matches: List[str]) -> List[str]:
    year = int(matches[0])
    result = []
    for music in music_db:
        if get_year(music) < year:
            result.append(get_title(music))
    return result


def songs_after_year(matches: List[str]) -> List[str]:
    year = int(matches[0])
    result = []
    for music in music_db:
        if get_year(music) > year:
            result.append(get_title(music))
    return result

def artist_by_song(matches: List[str]) -> List[str]:
    title = matches[0]
    result = []
    for music in music_db:
        if get_title(music).lower() == title.lower():
            result.append(get_artist(music))
    return result


def songs_by_artist(matches: List[str]) -> List[str]:
    artist = matches[0]
    result = []
    for music in music_db:
        if get_artist(music) == artist:
            result.append(get_title(music))
    return result


def year_by_song(matches: List[str]) -> List[str]:
    title = matches[0]
    result = []
    for music in music_db:
        if get_title(music) == title:
            result.append(get_year(music))
    return result

def songs_by_genre(matches: List[str]) -> List[str]:
    genre = matches[0].lower()
    return [get_title(s) for s in music_db if any(g.lower() == genre for g in get_genres(s))]

def earliest_song(matches: List[str]) -> List[str]:
    if not music_db:
        return []
    min_year = min(get_year(m) for m in music_db)
    return [get_title(m) for m in music_db if get_year(m) == min_year]

# dummy argument is ignored and doesn't matter
def bye_action(dummy: List[str]) -> None:
    raise KeyboardInterrupt

# --- PATTERN–ACTION LIST ---

pa_list: List[Tuple[List[str], Callable[[List[str]], List[Any]]]] = [
    (str.split("what songs were made in _"), songs_by_year),
    (str.split("what songs were made between _ and _"), songs_by_year_range),
    (str.split("what songs were made before _"), songs_before_year),
    (str.split("what songs were made after _"), songs_after_year),
    (str.split("who sang %"), artist_by_song),
    (str.split("what songs were sung by %"), songs_by_artist),
    (str.split("when was % released"), year_by_song),
    (str.split("what songs are in the % genre"), songs_by_genre),
    (str.split("what was the earliest song"), earliest_song),
    (["bye"], bye_action),
]

# --- CORE SEARCH ---

def search_pa_list(src: List[str]) -> List[str]:
    for pattern, action in pa_list:
        matched = match(pattern, src)
        if matched is not None:
            result = action(matched)
            if not result:
                return ["No answers"]
            return result
    return ["I don't understand"]

# --- QUERY LOOP ---

def query_loop() -> None:
    print("Welcome to the music database!\n")
    while True:
        try:
            print()
            query = input("Your query? ").replace("?", "").lower().split()
            answers = search_pa_list(query)
            for ans in answers:
                print(ans)
        except (KeyboardInterrupt, EOFError):
            break
    print("\nGoodbye!\n")


if __name__ == "__main__":
    query_loop()
"""
# --- TESTS ---
if __name__ == "__main__":
    # --- Songs by year ---
    assert sorted(songs_by_year(["1975"])) == ["Bohemian Rhapsody"]
    assert sorted(songs_by_year(["1991"])) == ["Lithium", "Smells Like Teen Spirit"]
    assert sorted(songs_by_year(["2017"])) == ["Shape of You"]

    # --- Songs by artist ---
    assert sorted(songs_by_artist(["Queen"])) == ["Bohemian Rhapsody"]
    assert sorted(songs_by_artist(["Nirvana"])) == ["Come As You Are", "Heart-Shaped Box", "Lithium", "Smells Like Teen Spirit"]
    assert sorted(songs_by_artist(["Mac Miller"])) == ["Good News", "Ladders", "Nikes on My Feet", "Self Care", "The Spins"]
    assert sorted(songs_by_artist(["A$AP Rocky"])) == ["Goldie", "L$D", "Peso", "Praise The Lord (Da Shine)"]

    # --- Artist by song ---
    assert sorted(artist_by_song(["Imagine"])) == ["John Lennon"]
    assert sorted(artist_by_song(["Shape of You"])) == ["Ed Sheeran"]
    assert sorted(artist_by_song(["Bohemian Rhapsody"])) == ["Queen"]
    assert sorted(artist_by_song(["Smells Like Teen Spirit"])) == ["Nirvana"]

    # --- Songs before year ---
    assert sorted(songs_before_year(["1980"])) == sorted([
        "Imagine",
        "Superstition",
        "Like a Rolling Stone",
        "Hey Jude",
        "Bohemian Rhapsody",
        "Hotel California",
        "Stayin' Alive",
        "Dreams",
        "Go Your Own Way",
        "September"
    ])

    # --- Songs after year ---
    assert sorted(songs_after_year(["2015"])) == sorted([
        "Shape of You",
        "Self Care",
        "Ladders",
        "Good News",
        "Praise The Lord (Da Shine)"
    ])

    # --- Year by song ---
    assert sorted(year_by_song(["Billie Jean"])) == [1983]
    assert sorted(year_by_song(["Smells Like Teen Spirit"])) == [1991]
    assert sorted(year_by_song(["Shape of You"])) == [2017]

    # --- Songs by genre ---
    assert sorted(songs_by_genre(["Pop"])) == sorted([
        "Beat It",
        "Billie Jean",
        "Clocks",
        "Empire State of Mind",
        "Purple Rain",
        "Rolling in the Deep",
        "Shape of You",
        "Stayin' Alive",
        "Thriller",
        "Uptown Funk",
        "Viva La Vida"
    ])
    assert sorted(songs_by_genre(["Grunge"])) == sorted([
        "Smells Like Teen Spirit",
        "Come As You Are",
        "Lithium",
        "Heart-Shaped Box"
    ])
    assert sorted(songs_by_genre(["Hip Hop"])) == sorted([
        "Lose Yourself",
        "Nikes on My Feet",
        "Self Care",
        "The Spins",
        "Good News",
        "Ladders",
        "Praise The Lord (Da Shine)",
        "L$D",
        "Peso",
        "Goldie",
        "Empire State of Mind"
    ])

    assert sorted(songs_by_genre(["Rock"])) == sorted([
        'Africa',
        'Beat It',
        'Bohemian Rhapsody',
        'Clocks',
        'Come As You Are',
        "Don't Stop Believin'",
        'Dreams',
        'Every Breath You Take',
        'Go Your Own Way',
        'Heart-Shaped Box',
        'Hey Jude',
        'Hotel California',
        'Lithium',
        'Mr. Brightside',
        'Purple Rain',
        'Radioactive',
        'Smells Like Teen Spirit',
        'Thriller',
        'Viva La Vida',
        'Wonderwall'
    ])

    # --- Pattern-action search ---
    assert sorted(search_pa_list(["who", "sang", "imagine"])) == ["John Lennon"]
    assert sorted(search_pa_list(["what", "was", "the", "earliest", "song"])) == ["Like a Rolling Stone"]

    print("All tests passed!")
"""
