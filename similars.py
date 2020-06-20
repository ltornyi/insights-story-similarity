import json
from nltk.tokenize import RegexpTokenizer
import gensim

TRANSLATE_DICT = {
    '\u2014': '-',
    '\u2002': ' ',
    '\u201c': '"',
    '\u201d': '"',
    '.': None,
    ',': None,
    '!': None,
    '?': None,
    ':': None
}

_translate_tab = "".maketrans(TRANSLATE_DICT)
_tokenizer = RegexpTokenizer(r'\s+', gaps=True)


def get_story_fulltext(story):
    return (story['title'] + ' ' + story['topLine'] + ' ' + story['text']).translate(_translate_tab).lower()


def tokenize_story(story):
    return [w for w in _tokenizer.tokenize(get_story_fulltext(story))]


def read_stories(filename):
    with open(filename) as infile:
        stories = json.load(infile)
    return stories


# https://radimrehurek.com/gensim/auto_examples/core/run_similarity_queries.html#sphx-glr-auto-examples-core-run-similarity-queries-py
def generate_tools(stories):
    tokenized_stories = [ [word for word in tokenize_story(story)] for story in stories ]
    dictionary = gensim.corpora.Dictionary(tokenized_stories)
    corpus = [dictionary.doc2bow(story) for story in tokenized_stories]
    tf_idf = gensim.models.TfidfModel(corpus)
    index = gensim.similarities.MatrixSimilarity(tf_idf[corpus])
    return {
        'dictionary': dictionary,
        'tf_idf': tf_idf,
        'index': index,
        'corpus': corpus
    }


def get_similar_stories(story, dictionary, tf_idf, index):
    story_bow = dictionary.doc2bow(tokenize_story(story))
    story_tfidf = tf_idf[story_bow]
    sims = index[story_tfidf]
    return sorted(enumerate(sims), key=lambda item: -item[1])


if __name__ == "__main__":
    stories = read_stories('stories.json')
    print('Number of stories: {}'.format(len(stories)))
    tools = generate_tools(stories)

    ind = int(input('Story index, enter to quit:'))
    while True:
        print('*****************')
        print('Selected story: {}'.format(stories[ind]['title']))
        print(stories[ind]['topLine'])
        print('*****************')
        sims = get_similar_stories(stories[ind], tools['dictionary'], tools['tf_idf'], tools['index'])[:4]
        for i, s in enumerate(sims):
            # The story is similar to itself, so we skip it:
            if s[0] != ind:
                print('Index: {}, Similarity score: {}, title: {}'.format(s[0], s[1], stories[s[0]]['title']))
                print(stories[s[0]]['topLine'])
                print('---------')
        print()
        ind = int(input('Story index, enter to quit:'))
