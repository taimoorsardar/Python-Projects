import os
import re
import string
import random

from graph import Graph, Vertex

def get_words_from_text(text_path):
    with open(text_path, 'r',encoding='utf-8', errors='ignore') as f:
        text = f.read()

        # this part is mainly for songs composer
        # remove the brackets and text inside it
        text = re.sub(r'\[(.+)\]', ' ', text) 

        text = ' '.join (text.split())
        text = text.lower()
        #remove all punctuations
        text = text.translate(str.maketrans('','',string.punctuation))

    words = text.split()
    words = words[:1000]
    return words

def make_graph(words):
    g = Graph()
    previous_word = None
    
    # for each word
    for word in words:
        # check if each word is in the graph, and if not then add it
        word_vertex = g.get_vertex(word)
        # if there was a previous word, then add an edge to if it does not already exist
        # in the graph, otherwise increment weights by 1
        if previous_word:
            previous_word.increment_edge(word_vertex)
        # set our words to the previous word and iterate!
        previous_word = word_vertex

    # we have to generate the probability mappings before composing
    g.generate_probability_mappings()
    return g

def compose(g, words, length=50):
    composition = []
    word = g.get_vertex(random.choice(words)) # pick a random word to start!
    for _ in range(length):
        composition.append(word.value)
        word = g.get_next_word(word)

    return composition

def main(artist):
    # step 1 get words from text
    # words = get_words_from_text('C:\\Users\\HP\\Desktop\\Projects\\MarkovChainComposer\\texts\\hp_sorcerer_stone.txt')
    words = []
    # for song lyrics 
    for song_file in os.listdir(f'songs\\{artist}'):
        # print(song_file)
        if song_file == '.DS_Store':
            continue
        words.extend(get_words_from_text('songs/{artist}/{song}'.format(artist=artist, song=song_file)))
    # step 2 make a graph using these words
    g = make_graph(words)
    # step 3 get the next words based on the number of words (defined by user)

    # step 4 show the user!
    composition = compose(g, words, 100)
    return  ' '.join(composition)

if __name__ == '__main__':
    print(main('taylor_swift'))