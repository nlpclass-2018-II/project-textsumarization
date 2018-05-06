import networkx as nx
import itertools
import editdistance
import nltk
import textdistance
import os


def buildGraph(nodes):
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    nodePairs = list(itertools.combinations(nodes, 2))

    for pair in nodePairs:
        firstString = pair[0]
        secondString = pair[1]
        distance = editdistance.eval(firstString, secondString)
        graph.add_edge(firstString, secondString, weight=distance)

    return graph


def buildGraphAlt(nodes):
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    nodePairs = list(itertools.combinations(nodes, 2))

    for pair in nodePairs:
        firstString = pair[0]
        secondString = pair[1]
        distance = textdistance.hamming.distance(firstString,
                                                 secondString)  # https://pypi.org/project/textdistance/ for other distance
        graph.add_edge(firstString, secondString, weight=distance)

    return graph


def summarize(text, sentenceCount):
    file = open(text)
    text = file.read()
    sentences = nltk.tokenize.sent_tokenize(text)
    graph = buildGraph(sentences)

    scoredSentences = nx.pagerank(graph, weight='weight')
    rankedSentences = sorted(((value, key) for (key, value) in scoredSentences.items()), reverse=True)

    summary = ''
    for i in range(0, sentenceCount):
        summary = summary + rankedSentences[i][1] + '\n\n'

    return summary


def summarizeAlt(text, sentenceCount):
    file = open(text)
    text = file.read()
    sentences = nltk.tokenize.sent_tokenize(text)
    graph = buildGraphAlt(sentences)

    scoredSentences = nx.pagerank(graph, weight='weight')
    rankedSentences = sorted(((value, key) for (key, value) in scoredSentences.items()), reverse=True)
    rankedSentences

    summary = ''
    for i in range(0, sentenceCount):
        summary = summary + rankedSentences[i][1] + '\n\n'

    return summary


def writeSummary(summary, text):
    file = open(text + ' Summary.txt', 'w+')
    file.write(summary)
    file.close()


def rogue(text, sentenceCount):
    path = "Gold/"
    file = open(path + text + ' Gold.txt')
    goldSum = file.read()
    goldSum = nltk.tokenize.word_tokenize(goldSum)

    path = "Text/"
    A = summarize(path + text + '.txt', sentenceCount)
    B = summarizeAlt(path + text + '.txt', sentenceCount)
    tokenA = nltk.tokenize.word_tokenize(A)
    tokenB = nltk.tokenize.word_tokenize(B)

    rogueCount = {}

    totalword = 0
    totalword2 = 0
    # counting unigram words
    for word in tokenA:
        if word in goldSum:
            totalword += 1

    for word in tokenB:
        if word in goldSum:
            totalword2 += 1

    rogueCount[1] = totalword / len(goldSum)
    rogueCount[2] = totalword2 / len(goldSum)

    path = "Summary/"
    if (rogueCount[1] > rogueCount[2]):
        writeSummary(A, path + text)
    else:
        writeSummary(B, path + text)

    return rogueCount


def run(pattern, count):
    i = 1
    score = ''
    for file in os.listdir('Text/'):
        filename = pattern + ' 0' + str(i)
        eval = rogue(filename, count)
        score = score + "Number " + str(i) + "   1: " + str(eval[1]) + "   2: " + str(eval[1]) + "\n"
        i += 1

    file = open('Score.txt', 'w+')
    file.write(score)
    file.close()