import nltk
import sys

import os
from math import log
from nltk.corpus import stopwords
nltk.download('stopwords')

from timer import Timer


FILE_MATCHES = 1
SENTENCE_MATCHES = 1

def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])

    # c=Timer('tokenize')
    # c.start()
    # file_words = {
    #     filename: tokenize(files[filename])
    #     for filename in files
    # }
    # c.stop()
    # LITTLE BIT FASTER
    c=Timer('tokenize')
    c.start()
    file_words = dict()
    for filename in files:
        file_words[filename] = tokenize(files[filename])
    c.stop()

    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    e=Timer('extract')
    e.start()
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens
    e.stop()

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    dic = dict()
    for file in os.listdir(directory):
        with open(os.path.join(directory, file),'r') as f:
            dic[file] = f.read()

    return dic


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # Remove punctuation
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    tokenized = tokenizer.tokenize(document.lower())
    # Remove Enlglish stopwords
    tokens_without_sw = [word for word in tokenized if not word in stopwords.words()]

    return tokens_without_sw


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = dict()
    num_docs = len(documents)
    in_doc = dict()

    # Count if word appears in document for all words in all documents
    # for each document
    for doc in documents:
        # for each word inside the document
        for word in documents[doc]:
            # if appears set to 1
            if word not in idfs:
              idfs[word] = 1
              in_doc[word] = True
            else:
                # only increase sum if its the first appearance on the doc
                if word not in in_doc:
                  idfs[word] += 1
                  in_doc[word] = True
        # refresh words found for the new doc
        in_doc = dict()

    # use formula for each word
    for word in idfs:
        idfs[word] = log(num_docs / idfs[word])

    return idfs

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    top = dict()
    # for each list of words in files
    for file in files:
        sum = 0
        # for each word in query
        for word in query:
            # avoid problems when a word in query doesnt exist in file
            if word not in idfs:
                continue
            else:
                idf = idfs[word]
                tf = files[file].count(word)
                sum += tf*idf
        top[file] = sum
    sorted_files = sorted(top, key=lambda x: top[x], reverse=True)[:n]
    # return the n top files
    return sorted_files

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    match_word_measure = dict()
    for sent in sentences:
        mw = 0
        qt = 0
        words = sentences[sent]
        numWords = len(words)
        for q_word in query:
            if q_word in words:
                mw += idfs[q_word]
                qt += words.count(q_word)
        qtd = qt / numWords
        match_word_measure[sent] = (mw, qtd)

    sorted_sent = sorted( match_word_measure.keys(), key=lambda x: match_word_measure[x], reverse=True)

    return sorted_sent[:n]

if __name__ == "__main__":
    main()
