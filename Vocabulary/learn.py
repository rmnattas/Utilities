"""
Aug 2018
learn.py

This terminal python app is made for my own use to leanr new English vocabulary.
It's an app that takes a list words and presents a translation, definition, and synynoms for it.

APIs:
- googletrans API (rip off of google translate...)
- Google spreadsheet API

Added Features:
- cache 
- grouping words (easier to learn)
- words direrctly from Google spreadsheet 
- add new words to Google spreadsheet
- show group
- chech if word in list
- select a word

"""


import random
from googletrans import Translator
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def main():
    words = getWords()
    words_dic = {}
    group = 1
    group_size = 10
    groups = setGroups(len(words), group_size)
    while True:
        action = input("Select Action or Group Number (1-{}) (g to show group) (s to select a word) (n to new word) (e to exit): ".format(len(groups)))
        done = False
        
        if isInt(action):
            group = int(action)

        elif action == "g":
            print("Group", group, "\n")
            showGroup(words, groups, group)
            done = True
            
        elif action == 'n':
            new_word = newWord(words)
            if new_word:
                addWord(new_word, words)
                groups = setGroups(len(words), group_size)
            done = True

        elif action == "s":
            print()
            while True:
                word_i = input("Enter the word number in group {}: ".format(group))
                if isInt(word_i):
                    break
            word = words[((group-1)*10)+int(word_i)]
            print("\n" + word + "\n")
            printWordInfo(word, words_dic)
            done = True

        elif action == "e":
            break

        if not done:
            print("Group", group)
            word = selectWord(words, groups, group)
            print("\n" + word)
            input()
            printWordInfo(word, words_dic)
        
        print("\n\n" + "-"*60 + "\n" + "-"*60 + "\n")
            
        

def getWords():
    print("Loading Words List.....")
    
    # https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
    # Get words list from Googel Drive Sheet
    scope = ['https://www.googleapis.com/auth/drive', 'https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secrets.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("Vocabulary").sheet1
    cells = sheet.col_values(1)
    
    #Cabitalize the first letter for each word
    for i in range(len(cells)):
        if cells[i]:
            cells[i] = cab(cells[i])
    #print(cells)
    return cells

def setGroups(words_count, gorup_size):
    groups = {}
    groups_count = ((words_count -1) // gorup_size) + 1
    for i in range(1, groups_count+1):
        frm = (i-1) * gorup_size
        to = i * gorup_size - 1
        if to >= words_count:
            to = words_count - 1
        groups[i] = [frm, to]
    return groups

def selectWord(words, groups, group):
    group_range = groups[group]
    randint = random.randint(group_range[0], group_range[1])
    return words[randint]

def getWordData(word):
    print("Loading Word Info.....")
    translator = Translator()
    data = translator.translate(word, src="en", dest="ar").extra_data
    
    word_data = {}
    
    pos_trans = []
    for translate in data["possible-translations"][0][2]:
        pos_trans.append(translate[0])
    if pos_trans: 
        word_data["possible-translations"] = pos_trans
    
    
    all_trans = []
    if data["all-translations"]:
        for partOfSpeech in data["all-translations"]:
            trans_list = []
            for translate in partOfSpeech[2]:
                trans_list.append(translate[0])
            all_trans.append([POS(partOfSpeech[0]), trans_list])
    if all_trans:
        word_data["all-translations"] = all_trans
        
        
    definitions = []
    if data["definitions"]:
        for partOfSpeech in data["definitions"]:
            POS_def_list = []  
            for definition in partOfSpeech[1]:
                defi = cab(definition[0])
                example = None
                if len(definition) == 3:
                    example = cab(definition[2])
                POS_def_list.append([defi, example])
            definitions.append([POS(partOfSpeech[0]), POS_def_list])
    if definitions:
        word_data["definitions"] = definitions
        
    
    synonyms = []
    if data["synonyms"]:
        for partOfSpeech in data["synonyms"]:
            syn_list = []
            for synonym in partOfSpeech[1]:
                syn_list.append(cab(synonym[0][0]))
            synonyms.append([POS(partOfSpeech[0]), syn_list])
    if synonyms:
        word_data["synonyms"] = synonyms        
    
    return word_data


def printWordInfo(word, words_dic=False):
    if isinstance(words_dic, dict):
        if word not in words_dic:
            words_dic[word] = getWordData(word)
        word_info = words_dic[word]
    else:
        word_info = getWordData(word)
        print("\n\n" + word)
            

            
    print("\n" + "Translate:")
    for translate in word_info["possible-translations"]:
        print("\t" + translate)
    if "all-translations" in word_info:
        for partOfSpeech in word_info["all-translations"]:
            print("\t" + partOfSpeech[0] + ":")
            print("\t\t" + "، ".join(partOfSpeech[1]))
    
    
    if "definitions" in word_info:
        print("\n" + "Definitions and Examples:")
        for partOfSpeech in word_info["definitions"]:
            print("\t" + partOfSpeech[0] + ":")
            for definition in partOfSpeech[1]:
                print("\t\t" + definition[0])
                if definition[1]:
                    print('\t\t\t"' + definition[1] + '"')
    
    
    if "synonyms" in word_info:
        print("\n" + "Synonyms:")
        for partOfSpeech in word_info["synonyms"]:
            print("\t" + partOfSpeech[0] + ":")
            print("\t\t" + ", ".join(partOfSpeech[1]))


def newWord(words):
    print()
    word = cab(input("Enter the new word: "))
    print()
    printWordInfo(word)

    if word not in words:
        action = input("\nAdd the word to the list (y/n): ")
        if action == "y":
            return word
        else:
            return False
    else:
        print("\nWord is already on the list")

def addWord(word, words):
    print("Adding the word '{}' to the list.....".format(word))
    
    # https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
    # Adding a new word to a Googel Drive Sheet
    
    try:
        scope = ['https://www.googleapis.com/auth/drive', 'https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)
        sheet = client.open("Vocabulary").sheet1    
        sheet.update_cell(len(words)+1, 1, word)
    except:
        print("Error Adding to the list")
    else:
        # update words list
        words.append(word)
        print("Done Adding to the list")
    
    
def showGroup(words, groups, group):
    group_words = words[groups[group][0] : groups[group][1]+1]
    for i in range(len(group_words)):
        print(str(i) + "-" + group_words[i])
    
    
def cab(string):
    #Cabitalize the first letter in a string
    return string[0].upper() + string[1:]

def POS(partOfSpeech):
    #Convert part of speech to english
    POS_dic = {
        "اسم" : "Noun",
        "فعل" : "Verb",
        "صفة" : "Adjective",
        "حال" : "Adverb",
        "اختصار" : "Abbreviation"
    }
    if partOfSpeech in POS_dic:
        return POS_dic[partOfSpeech]
    else:
        return partOfSpeech
    
def isInt(string):
    # Check if the string is a number
    try:
        int(string)
        return True
    except:
        return False


main()
