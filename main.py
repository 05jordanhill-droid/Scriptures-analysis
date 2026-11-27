import pandas as pd
from Python_Support import Python_Support

"""
Question 1: How many occurences of a given word appears in a given selection of Scripture 
  and how does that word count compare to other selections?

Question 2: What is the density of a given word within a given selection of Scripture 
  and how does that density compare to other selections?

Question 3: What are the most used words within a given selection of Scripture?
"""

# Future implementation allows percentage_match to match with varied versions of a word.
# Depending on the percentage, "hate" could be matched with "hating"
def search_word(df, search_word:str, percentage_match=1, search=None, exact=False):
    search_word = search_word.lower()
    verse_list = []
    word_count = 0
    selection = get_selection(df, search)

    for index, row in selection.iterrows():
        verse = row["scripture_text"]

        clean_verse = Python_Support.remove_punctuation(verse)

        for word in clean_verse.split():
            word_count += 1

            if exact:
                if word == search_word:
                    verse_list.append({
                        "verse" : verse,
                        "address" : row["verse_title"]
                    })
            else:
                if Python_Support.are_similar(search_word, word, percentage_match):
                    verse_list.append({
                        "verse" : verse,
                        "address" : row["verse_title"]
                    })

    return {
        "words" : word_count,
        "searched" : verse_list
    }


# Rather than iterating through every word and running them all through search_word(), 
#   having a dedicated function for cataloging every word is FAR more efficient.
def search_all(df, search=None):
    words = {}

    word_count = 0
    selection = get_selection(df, search)

    for index, row in selection.iterrows():
        verse = row["scripture_text"]

        clean_verse = Python_Support.remove_punctuation(verse)

        for word in clean_verse.split():
            word_count += 1

            if word.title() not in words.keys():
                words[word.title()] = {
                    "count" : 1
                }
            else:
                words[word.title()]["count"] += 1

    for key in words:
        words[key]["density"] = words[key]["count"] / word_count

    return words, word_count


# search is applied to the data like a whitelist filter, starting with the largest identifiers 
# and wittling out what wasn't specified in the search
def get_selection(df, search=None):
    if search is None:
        search = {
            "volume_titles" : [
                "Old Testament",
                "New Testament",
                "Book of Mormon",
                "Doctrine and Covenants",
                "Pearl of Great Price"
            ],
            "book_titles" : [],
            "chapter_numbers" : [],
            "verse_numbers" : []
        }

    selection = df
    
    if search["volume_titles"] != []:
        selection = selection[
            selection["volume_title"].isin(search["volume_titles"])
        ]

    if search["book_titles"] != []:
        selection = selection[
            selection["book_title"].isin(search["book_titles"])
        ]
        
    if search["chapter_numbers"] != []:
        selection = selection[
            selection["chapter_number"].isin(search["chapter_numbers"])
        ]
        
    if search["verse_numbers"] != []:
        selection = selection[
            selection["verse_number"].isin(search["verse_numbers"])
        ]

    return selection


# A word count between different sized selections can be mute, 
# since more of a specific word in one selection may be the result of a larger text 
# rather than a greater emphasis
def get_search_density(search_results):
    return len(search_results["searched"]) / search_results["words"]


def analyze(df, search):
    selection = get_selection(df, search)

    dictionary = {
        "word count" : 0,
        "words" : {}
    }

    dictionary = analyze_verse(dictionary, selection)


def analyze_verse(dictionary, selection, index=0):
    row = selection.iloc[index]
    verse = row["scripture_text"]
    clean_verse = Python_Support.remove_punctuation(verse).split()

    dictionary = analyze_word(dictionary, clean_verse)

    if index != len(selection) - 1:
        dictionary = analyze_verse(dictionary, selection, index + 1)
    else:
        return dictionary


def analyze_word(dictionary, verse, index=0):
    word = verse[index]

    if word not in dictionary.keys():
        dictionary["words"][word] = 1
    else:
        dictionary["words"][word] += 1

    dictionary["word count"] += 1

    if index != len(verse) - 1:
        dictionary = analyze_word(dictionary, verse, index + 1)
    else:
        return dictionary


# Generalizing the process of selecting either a Volume, Book, etc... into one functions saves space
# rather than just repeating the code in the different functions with minimal differences between them 
def select_something(df, search, something, something_key):
    run = True
    
    Python_Support.clear_terminal()

    while run:
        choice = input(f"Add {something.title()} to Search (leave empty to finish {something.lower()} additions) \n>")

        fail = False

        if choice != "":
            try:
                check = df[
                    df[something_key] == choice
                ]
            except:
                fail = True

            Python_Support.clear_terminal()

            if fail or check.size == 0:
                print("Invalid Input. Try Again.\n")
            
            else:
                search[something_key + "s"].append(choice)

        else:
            run = False

    return search

def select_volume(df, search):
    return select_something(df, search, "volume", "volume_title")

def select_book(df, search):
    return select_something(df, search, "book", "book_title")

def select_chapter(df, search):
    return select_something(df, search, "chapter", "chapter_number")

def select_verse(df, search):
    return select_something(df, search, "verse", "verse_number")


def select_search(df):
    # These act as white listed filters to the data when applied using get_selection()
    search = {
        "volume_titles" : [],
        "book_titles" : [],
        "chapter_numbers" : [],
        "verse_numbers" : []
    }
    
    while True:
        Python_Support.clear_terminal()
        choice = Python_Support.input("""1. Add Volume to Search
2. Add Book to Search
3. Add Chapter to Search
4. Add Verse to Search
5. Continue
>""", [
    "add volume to search", "1",
    "add book to search", "2",
    "add chapter to search", "3",
    "add verse to search", "4",
    "continue", "5"
]).lower()

        if choice in ["add volume to search", "1"]:
            search = select_volume(df, search)
            
        elif choice in ["add book to search", "2"]:
            search = select_book(df, search)

        elif choice in ["add chapter to search", "3"]:
            search = select_chapter(df, search)

        elif choice in ["add verse to search", "4"]:
            search = select_verse(df, search)

        elif choice in ["continue", "5"]:
            return search


# Each individual search is a single analysis that will be compared with other analyses
# A single search can have several different filters on it
# Putting 5 in verse_numbers would get every 5th verse of a chapter in the entire database
# Reccomended usage for multiple additions to a search is applying multiple books if you want to search that section
# and compare it to a different section
def select_searches(df):
    searches = []

    while True:
        Python_Support.clear_terminal()

        choice = Python_Support.input("""1. Configure Search to Add
2. Continue
>""", [
    "1", "configure search to add",
    "2", "continue"
])
        if choice in ["1", "configure search to add"]:
            search = select_search(df)

            Python_Support.clear_terminal()
            name = input("Choose name for configured search \n>")

            search["name"] = name
            searches.append(search)

        else:
            if len(searches) > 1:
                return searches

            Python_Support.clear_terminal()
            print("At least 2 searches required.")


def main():
    df = pd.read_csv("combinationscriptures.csv")

    run = True

    while run:
        Python_Support.clear_terminal()

        choice = Python_Support.input("""1. Compare chosen word counts in chosen selections 
2. Compare chosen word densities in chosen selections
3. Measure most occurent words in chosen selection
>""", [
    "1", "compare chosen word counts in chosen selections",
    "2", "compare chosen word densities in chosen selections",
    "3", "measure most occurent words in chosen selection"
])
        
        if choice.lower() in ["1", "compare chosen word counts in chosen selections"]:
            Python_Support.clear_terminal()

            word = input("Choose your word \n>")
            searches = select_searches(df)

            Python_Support.clear_terminal()
            print("Loading...")

            results = []
            for search in searches:
                results.append(search_word(df, word, search=search, exact=True))

            for i, result in enumerate(results):
                word_count = len(result["searched"])
                print(f"{searches[i]["name"]} has \"{word}\" {word_count} times")

            print()

            for i, result in enumerate(results):
                name = searches[i]["name"]
                word_count = len(result["searched"])

                for j, compare_result in enumerate(results):
                    if result != compare_result:
                        name_compare = searches[j]["name"]
                        word_count_compare = len(compare_result["searched"])

                        comparison = word_count / word_count_compare
                        term = "the same as"

                        if comparison < 1:
                            term = f"{comparison} times less than"
                        elif comparison > 1:
                            term = f"{comparison} times more than"

                        print(f"\"{word}\" appears in {name} {term} {name_compare}")

            input("\nPress ENTER to move on \n>")


        elif choice.lower() in ["2", "compare chosen word densities in chosen selections"]:
            Python_Support.clear_terminal()

            word = input("Choose your word \n>")
            searches = select_searches(df)

            Python_Support.clear_terminal()
            print("Loading...")

            results = []
            for search in searches:
                results.append(search_word(df, word, search=search, exact=True))

            for i, result in enumerate(results):
                word_density = get_search_density(result)
                print(f"{searches[i]["name"]} has \"{word}\" at a density of %{word_density * 100}")

            print()

            for i, result in enumerate(results):
                name = searches[i]["name"]
                word_density = get_search_density(result)

                for j, compare_result in enumerate(results):
                    if result != compare_result:
                        name_compare = searches[j]["name"]
                        word_density_compare = get_search_density(compare_result)

                        comparison = word_density / word_density_compare
                        term = "the same as"

                        if comparison < 1:
                            term = f"{comparison} times less than"
                        elif comparison > 1:
                            term = f"{comparison} times more than"

                        print(f"{name} \"{word}\" density is {term} {name_compare} \"{word}\" density")

            input("\nPress ENTER to move on \n>")

        else:
            Python_Support.clear_terminal()
            
            search = select_search(df)

            Python_Support.clear_terminal()
            print("Loading...")

            words, word_count = search_all(df, search)

            keys = sorted(
                words,
                key=lambda k: words[k]["count"],
                reverse=True
            )

            Python_Support.clear_terminal()

            # Allows full data to be shown in VSCode
            Python_Support.adjust_terminal_history_capacity(len(words))

            print(f"Total Word Count: {word_count}")
            print(f"Word            | Count    | Density")
            print(f"-----------------------------------------------------------")

            for i, key in enumerate(keys):
                print(f"{key.title():<15} | {words[key]["count"]:<8} | %{words[key]["density"] * 100}")

            input("\nPress ENTER to move on \n>")

            # Puts terminal history scroll back back to default
            Python_Support.adjust_terminal_history_capacity(1000)



main()