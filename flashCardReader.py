# Python flash card reader, by MoTWilliams
import json
import random as r
from termcolor import colored as c

def load_last_used_file():
    TandC = None

    try:
        with open('lastUsed.json') as file:
            TandC = json.load(file)
    except FileNotFoundError:
        print(c("\nERROR","red"), end = "")
        print(": Could not retrieve term and course information.", end = " ")
        print("Please try again.")
        return None
    else:
        return TandC
    

def load_term_file(TandC):
    
    cards = None
    try:
        with open(TandC['term'] + 'flashCards.json') as file:
            cards = json.load(file)
    except FileNotFoundError:
        print(c("\nERROR","red"), end = "")
        print(": " + TandC['term'] + "flashCards.json not found.")
    else:
        return cards


def load_course(term):
    TandC = load_last_used_file()

    while term:
        course = None
        try:
            course = term[TandC['course']]
        except:
            print(c("\nERROR","red"), end = "")
            print(": " + TandC['course'] + " does not exist.", end = " ")
            print("Please try again.")
        else:
            return course


def load_different_term_file(TandC):
    
    while TandC:
        print(c("\nEnter term, or enter 'x' to exit","dark_grey"), end = "")
        term = input(c(": ","dark_grey")).title().replace(" ","")

        # exit if user enters 'x'
        if term == 'X':
            return None

        cards = None
        try:
            with open(term + 'flashCards.json') as file:
                cards = json.load(file)
        except FileNotFoundError:
            print(c("\nERROR","red"), end = "")
            print(": " + term + "flashCards.json not found.", end = " ")
            print("Please try again.")
        else:
            TandC.update({"term":term})
            with open('lastUsed.json', 'w') as file:
                json.dump(TandC, file, indent=2)
            return cards

def load_different_course(term):
    TandC = load_last_used_file()

    while term:
        print(c("\nEnter course, or enter 'x' to exit","dark_grey"), end = "")
        courseNo = input(c(": ","dark_grey")).upper().replace(" ","")

        if courseNo == 'X':
            print(c("\nGoodbye!\n","blue"))
            return None

        course = None
        try:
            course = term[courseNo]
        except:
            print(c("\nERROR","red"), end = "")
            print(": " + courseNo + " does not exist.", end = " ")
            print("Please try again.")
        else:
            TandC.update({'course':courseNo})
            with open('lastUsed.json', 'w') as file: 
                json.dump(TandC, file, indent=2)
            return course


def show_cards(course):
    # https://www.geeksforgeeks.org/python-do-while/
    while course:
        # choose a random flash card
        module = r.randint(1,2) # working on allowing user to enter a range here
        section = 'Module ' + str(module)
        cardNo = r.randint(0,len(course[section])-1) 
        
        # show the question
        print("\n" + course[section][cardNo]['Q'])
        
        # hint feature
        hasHint = None
        while True:
            print(c("\nPress [ENTER] to show answer","dark_grey"), end = "")

            # check if question has a hint
            try:
                hasHint = course[section][cardNo]['Hint']
            except:
                print(c(":","dark_grey"), end = " ")
            else:
                print(c(", or enter 'h' for a hint:","dark_grey"), end = " ")

            # check if user needs the hint
            needHint = input().lower()
            if needHint == 'h':
                print("\nHINT: " + hasHint, end = " ")
                input()
                break
            elif needHint == '':
                print()
                break
            else:
                print(c("\nERROR","red") + ": Invalid entry.", end = " ")
                print("Did you mean 'h'?", c("Please try again.", "dark_grey"))
        
        # show the answer
        answers = course[section][cardNo]['A']

        if type(answers) == list:
            for answer in answers:
                if type(answer) == list:
                    for point in answer:
                        print("  " + point, end = "")
                        input()
                else:
                    print(answer, end = "")
                    input()
        else:
            print(answers)

        # prompt for show next card or exit
        print(c("\nPress [ENTER] to go to the next","dark_grey"), end = " ")
        print(c("flash card, or enter 'x' to exit:","dark_grey"), end = " ")
        choice = input().lower()
        while not (choice == "" or choice == "x"):
            print(c("Make a valid selection:","dark_grey"), end = " ")
            print(c("[ENTER] to move on, or 'x'","dark_grey"), end = " ")
            choice = input(c("to exit:","dark_grey")).lower()

        if choice == 'x':
            break


def main():
    last_used = load_last_used_file()
    print("\nLast card set viewed:", end = " ")
    print(last_used['term'] + " - " + last_used['course'] + ".") # this line

    term = None
    course = None
    while True:
        print(c("Press [ENTER] to view this set","dark_grey"), end = " ")
        print(c("again, enter 'new' to choose a","dark_grey"), end = " ")
        print(c("different card set, or enter 'x'","dark_grey"), end = " ")
        choice = input(c("to exit: ","dark_grey")).lower()

        # exit if user enters 'x'
        if choice == 'x':
            break

        if choice == "new":
            term = load_different_term_file(last_used)
            course = load_different_course(term)
            break
        
        if choice == "":
            term = load_term_file(last_used)
            course = load_course(term)
            break

        print(c("ERROR","red") + (": Invalid entry. Please try again.\n"))
    
    show_cards(course)
    print(c("\nGoodbye!\n","blue"))        

main()