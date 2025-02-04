# Python flash card reader, by MoTWilliams
import json
import random as r
from termcolor import colored as c


def load_last_used_file():
    """
    Loads file to retrieve term, course, and module range of the last viewed
    card set; returns it as a dictionary.
    """
    TandC = None
    try:
        with open('lastUsed.json') as file:
            TandC = json.load(file)
    except FileNotFoundError:
        print(c("\nERROR:","red"), end=" ")
        print("Could not retrieve term and course information.", end=" ")
        print("Please try again.")
        return None
    else:
        return TandC
    

def print_last_used_set(TandC):
    """
    Print the term, course, and range of modules for the last viewed card set
    """
    # print term and course
    print("\nLast card set viewed:", end=" ")
    print(TandC['term'] + ":", end=" ")
    print(TandC['course'] + " - ", end="")
    
    # get modules range
    first = str(TandC['modules']['from'])
    last = str(TandC['modules']['to'])

    # last set viewed only included one module
    if first == last:
        print("Module " + first)
        return
    
    # print the modules range
    print("Modules " + first + "-" + last)


def load_term_file(TandC):
    """
    Opens the last viewed card data file
    """
    cards = None
    try:
        with open(TandC['term'] + 'flashCards.json') as file:
            cards = json.load(file)
    except FileNotFoundError:
        print(c("\nERROR:","red"), end=" ")
        print(TandC['term'] + "flashCards.json not found.")
    else:
        return cards


def get_course(TandC,term):
    """
    Retrieves the last viewed course from the open card data file
    """
    while term:
        course = None
        try:
            course = term[TandC['course']]
        except:
            print(c("\nERROR:","red"), end =" ")
            print(TandC['course'] + " does not exist.", end=" ")
            print("Please try again.")
        else:
            return course


def get_modules(TandC,course):
    """
    Retrieves module numbers from the last opened file
    """
    while course:
        return {
            "from":TandC['modules']['from'],
            "to":TandC['modules']['to']
        }


def load_different_term_file(TandC):
    """
    Opens user-specified card data file and updates last used file with new term
    """
    while TandC:
        print(c("\nEnter term, or enter 'x' to exit","dark_grey"), end="")
        term = input(c(": ","dark_grey")).title().replace(" ","")

        # exit if user enters 'x'
        if term == 'X':
            return None

        # open card data file and update last opened
        cards = None
        try:
            with open(term + 'flashCards.json') as file:
                cards = json.load(file)
        except FileNotFoundError:
            print(c("\nERROR","red"), end="")
            print(": " + term + "flashCards.json not found.", end=" ")
            print("Please try again.")
        else:
            TandC.update({"term":term})
            with open('lastUsed.json', 'w') as file:
                json.dump(TandC, file, indent=2)
            return cards


def get_different_course(TandC,term):
    """
    Opens user-specified course and updates last used file with new course
    """
    while term:
        print(c("\nEnter course, or enter 'x' to exit:","dark_grey"), end=" ")
        courseNo = input().upper().replace(" ","")

        # exit if user enters 'x'
        if courseNo == 'X':
            return None

        # retrieve course and update last opened file
        course = None
        try:
            course = term[courseNo]
        except:
            print(c("\nERROR:","red"), end=" ")
            print(courseNo + " does not exist.", end=" ")
            print("Please try again.")
        else:
            TandC.update({'course':courseNo})
            with open('lastUsed.json', 'w') as file: 
                json.dump(TandC, file, indent=2)
            return course


def get_different_modules(TandC,course):
    """
    Opens user-specified module(s) and updates last used file with new module(s)
    """
    while course:
        print(c("\nEnter the first module (Ex:'1'),","dark_grey"), end=" ")
        print(c("or enter 'x' to exit:","dark_grey"), end=" ")
        firstNo = int(input())

        # exit if user enters 'x'
        if str(firstNo) == 'x':
            return None

        print(c("\nEnter the last module","dark_grey"), end=" ")
        print(c("(Ex:3) or enter 'x' to exit:","dark_grey"), end=" ")
        lastNo = int(input())

        # exit if user enters 'x'
        if str(lastNo) == 'x':
            return None
        
        last = None
        if firstNo > lastNo:
            print(c("ERROR:","red"), end=" ")
            print("Invalid range. Please try again.")
        else:
            try:
                last = course['Module ' + str(lastNo)]
            except:
                print(c("ERROR:","red"), end=" ")
                print("Module " + str(lastNo) + " does not exist.", end=" ")
                print("Please try again.")
            else:
                TandC.update({"modules":{"from":firstNo,"to":lastNo}})
                with open('lastUsed.json', 'w') as file: 
                    json.dump(TandC, file, indent=2)
                return get_modules(TandC,course)
        
        
def hint_feature(course):
    pass


def show_cards(TandC,course,modules):
    # https://www.geeksforgeeks.org/python-do-while/
    while course:
        # choose a random flash card
        moduleNo = r.randint(modules['from'],modules['to']) 
        module = 'Module ' + str(moduleNo)
        cardNo = r.randint(0,len(course[module])-1) 
        
        # show the question
        print("\n" + course[module][cardNo]['Q'])
        
        # hint feature
        hasHint = None
        while True:
            print(c("\nPress [ENTER] to show answer","dark_grey"), end="")

            # check if question has a hint
            try:
                hasHint = course[module][cardNo]['Hint']
            except:
                print(c(":","dark_grey"), end=" ")
            else:
                print(c(", or enter 'h' for a hint:","dark_grey"), end=" ")

            # check if user needs the hint
            needHint = input().lower()
            if needHint == 'h':
                print("\nHINT: " + hasHint, end=" ")
                input()
                break
            elif needHint == '':
                print()
                break
            else:
                print(c("\nERROR","red") + ": Invalid entry.", end=" ")
                print("Did you mean 'h'?", c("Please try again.", "dark_grey"))
        
        # show the answer
        answers = course[module][cardNo]['A']

        if type(answers) == list:
            for answer in answers:
                if type(answer) == list:
                    for point in answer:
                        print("  " + point, end="")
                        input()
                else:
                    print(answer, end="")
                    input()
        else:
            print(answers)

        # prompt for show next card or exit
        print(c("\nPress [ENTER] to go to the next","dark_grey"), end=" ")
        print(c("flash card, or enter 'x' to exit:","dark_grey"), end=" ")
        choice = input().lower()
        while not (choice == "" or choice == "x"):
            print(c("Make a valid selection:","dark_grey"), end=" ")
            print(c("[ENTER] to move on, or 'x'","dark_grey"), end=" ")
            choice = input(c("to exit:","dark_grey")).lower()

        if choice == 'x':
            break


def main():
    last_used = load_last_used_file()
    print_last_used_set(last_used)

    term = None
    course = None
    modules = None
    while True:
        print(c("Press [ENTER] to view this set","dark_grey"), end=" ")
        print(c("again, enter 'new' to choose a","dark_grey"), end=" ")
        print(c("different card set, or enter 'x'","dark_grey"), end=" ")
        choice = input(c("to exit: ","dark_grey")).lower()

        # exit if user enters 'x'
        if choice == 'x':
            break

        if choice == "new":
            term = load_different_term_file(last_used)
            course = get_different_course(last_used,term)
            modules = get_different_modules(last_used,course)
            break
        
        if choice == "":
            term = load_term_file(last_used)
            course = get_course(last_used,term)
            modules = get_modules(last_used,course)
            break

        print(c("ERROR","red") + (": Invalid entry. Please try again.\n"))
    
    show_cards(last_used,course,modules)
    print(c("\nGoodbye!\n","blue"))        

main()