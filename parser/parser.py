import nltk
import sys

from timer import Timer

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP | VP | NP VP | S Conj S | NP V AdjP | N V PP | N AdvP | VP P AdjP | NP AdjP PP | VP AdjP
NP -> N | Det N | N PP | N PP AdjP | Det N PP 
VP -> V | V NP | V PP Adv | V Adv
AdvP -> Adv VP | 
AdjP -> Adj NP | Det AdjP | Adj AdjP
PP -> P NP | V P
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    tokens = nltk.tokenize.word_tokenize(sentence.lower())
    # Dealing with non alphabetical words. 
    tokens = [word for word in tokens if word.isalpha()]

    return tokens

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """ 
    #obtaining subtrees with NP label
    pending_queue = list(tree.subtrees(filter=lambda t: t.label()=='NP'))

    chunks = []
    while pending_queue != []:
        # get tree root
        current = pending_queue.pop(0)
        # obtain subtrees labeled NP
        sub = list(current.subtrees(filter=lambda t:t.label()=='NP'))
        # remove itself
        sub.pop(0)
        # if we found 0 subtrees with NP label, we found an NP chunk
        if len(sub) == 0:
            chunks.append(current)
        # otherwise it contains another NP chunk, so lets find it
        else:
            continue

    return chunks

if __name__ == "__main__":
    main()
