import json
import random as r
from termcolor import colored as c
import re

def get_term_open_file():
    """
    Choose term and open correct file
    """
    while True:
        print(c("Enter term, or enter 'x' to exit","dark_grey"), end = "")
        term = input(c(": ","dark_grey")).replace(" ","").title()

        # exit if user enters 'x'
        if term == 'X':
            break

        




# https://www.geeksforgeeks.org/read-json-file-using-python/
# Open and read the JSON file
with open('Spring2025flashCards.json') as file:
    flashCards = json.load(file)

def main():
    # https://www.geeksforgeeks.org/python-do-while/
    while True:
        # choose a random flash card
        course = flashCards['CSCE 3550']
        module = r.randint(1,1)
        section = 'Module ' + str(module)
        cardNo = r.randint(0,len(course[section])-1)
        
        # show the question
        print("\n" + course[section][cardNo]['Q'])
        print(c("\nPress [ENTER] to show answer","dark_grey"), end = "")

        # check question for hint
        hasHint = course[section][cardNo]['Hint']
        if not hasHint == "X":
            print(c(", or enter 'h' for a hint","dark_grey"), end = "")
        
        needHint = input(c(": ","dark_grey")).lower()

        # check if user needs the hint
        if needHint == 'h':
            print("\nHINT: " + hasHint, end = " ")
            input()
        else:
            print()
        
        # show the answer
        for answer in course[section][cardNo]['A']:
            print(answer, end = "")
            if not answer == course[section][cardNo]['A'][-1]:
                input()
            else:
                print()
            
        # prompt for show next card or exit
        print(c("\nPress [ENTER] to go to the next","dark_grey"), end = " ")
        print(c("flash card, or enter 'x' to exit:","dark_grey"), end = " ")
        choice = input().lower()
        while not (choice == "" or choice == "x"):
            print(c("Make a valid selection:","dark_grey"), end = " ")
            print(c("[ENTER] to move on, or 'x' to exit:","dark_grey"), end = " ")
            choice = input().lower()

        if choice == 'x':
            print(c("\nGoodbye!\n","blue"))
            break

# get_term_open_file()