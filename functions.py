from collections import defaultdict
from operator import attrgetter
from textdistance import jaro_winkler
from Match import Match

NUM_RESULTS = 10
bands = {}
# "trigrams" is a defaultdict. This simplifies the syntax when creating
# dictionaries as new keys are given a default datatype and value,
# allowing one to directly access a key as if it existed. Trigrams,
# three character groupings, are used to reduce the number of computations
# done when performing fuzzy string matching by shifting the burden into
# preprocessing. The length of this n-gram could be altered depending on
# the size of the dataset, and different databases could even be constructed
# with different length n-grams, though trigrams are fairly standard. By
# normalizing input (converting to lowercase, removing diacritics, etc.),
# the possible number of trigram combinations could result in a number
# significantly lower than 50 million. Counts for this trigram dictionary
# would be highly skewed as only certain letter combinations occur
# with high frequency (e.g., highly productive morphemes), so special
# logic would only need to be employed for a small number of cases.
trigrams = defaultdict(set)


def create_db():
    f = open("fake_band_names_mit.txt")

    for line in f:
        # Remove leading/trailing whitespace, and guard against non-alphabetic
        # input. 
        entry = str(line).strip()
        # The dictionary "bands" serves as both a cheap lookup data structure
        # for exact string matches as well as a site to store non-canonical
        # forms.
        canonical_entry = entry.lower()
        bands[canonical_entry] = entry

        length = len(canonical_entry)
        if length < 3:
            trigrams[canonical_entry].add(canonical_entry)
        else:
            for i in range(length-2):
                trigrams[canonical_entry[i:i+3]].add(canonical_entry)

def search_exact(query):
    return query in bands

def search_trigrams(query):
    subset = set()

    tri_search = [query[i:i+3] for i in range(len(query)-2)]

    # A union between all sets is constructed here but this operation
    # could be altered depending on the substring submitted or where
    # the substring was found in the string, potentially handling high-
    # frequency substrings or substrings occurringly word-initially
    # differently.  
    for item in tri_search:
        if trigrams.get(item) is not None:
            subset.update(trigrams.get(item))

    # Jaro-Winkler is a good edit distance metric choice to use with trigrams as it
    # favors those strings which match from the beginning.
    # Place matches in objects so that they can be sorted later using attrgetter.
    matches = [Match(bands[item], jaro_winkler(query, item)) for item in subset]

    return sorted(matches, key=attrgetter("score"), reverse=True)[:NUM_RESULTS]

def search_errors(query):
    next_steps = ("If the exact match and basic trigram searches fail, now would be the "+
    "time to consider even more expensive searchs, e.g., spelling errors and "+ 
    "probabilities. I didn't implement this here but I have done so before. "+
    "Basically one looks at the probability of a given spelling mistake "+ 
    "type (insertion, deletion, substitution, or transposition) for a given "+
    "letter or letter pair. This is necessary as some mistakes are obviously "+
    "more likely than others for any given letter (influenced by their "+
    "proximity on the keyboard). These probabilities then combine with "+
    "overall frequencies, potentially generated from a custom corpus.")
    return "No results found for {}. <br/><br/> {}".format(query, next_steps) 

