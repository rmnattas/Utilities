"""
Jan 2019
quickWord.py

This app takes a word from std input and given def, synonyms, and examples for it.
Made as a quick way to look up a word while reading novels 

APIs:
- Wordnik API.

"""


from wordnik import *


def main():
    # e to exit
    while 1:
        print("="*80)
        word = input("\nEnter a word: ")
        if not word: continue
        if word == "e": break
        printWordInfo(word)
        print()



def printWordInfo(word):
    word_info = getWordData(word)
    print("\n\n" + word)
            
    if "definitions" in word_info:
        print("\n" + "*Definitions:")
        for defin in word_info["definitions"]:
            print("\t-" + defin )
    
    if "examples" in word_info:
        print("\n" + "*Examples:")
        for examp in word_info["examples"]:
            print("\t-\"" + examp + "\"")
    
    if "synonyms" in word_info:
        print("\n" + "*Synonyms:")
        print("\t" + ", ".join(word_info["synonyms"]))




def getWordData(word):
    print("Loading Word Info.....")
    word = word.lower()
    word_data = {}

    # set api
    f = open("key.txt", "r")
    apiKey = f.readline().strip()
    apiUrl = 'http://api.wordnik.com/v4'
    client = swagger.ApiClient(apiKey, apiUrl) 
    wordApi = WordApi.WordApi(client)
    
    # get definitions
    defs = wordApi.getDefinitions(word)
    if defs:
        word_defs = []
        for definition in defs:
            word_defs.append(definition.text)
        word_data["definitions"] = word_defs

    # get examples
    exs = wordApi.getExamples(word)
    if exs:
        word_exs = []
        for examp in exs.examples:
            word_exs.append(examp.text)
        word_data["examples"] = word_exs

    # get synonyms
    syns = wordApi.getRelatedWords(word)
    if syns:
        word_syns = []
        for relation in syns:
            if (relation.relationshipType == "equivalent" or relation.relationshipType == "synonym"):
                word_syns.extend(relation.words)
        word_data["synonyms"] = word_syns

    return word_data




main()
