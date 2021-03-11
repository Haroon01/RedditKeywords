from bot import reddit
import time

r = reddit.Reddit()
if __name__ == "__main__":

    print("Keyword Trends")
    print("*"*30)
    time.sleep(1)
    print("Choose an option:\n"
          "1) Search for all words\n"
          "2) Search for specified words only\n\n"
          "Hint: You can specify your own words in custom_words.txt")
    time.sleep(0.5)
    option = input(">> ")

    if option == "1":
        custom_words = False
        cmn_words_inp = input("Would you like to exclude common words? (Yes/No) ").lower()
        if cmn_words_inp == "yes":
            cmn_words = True
        elif cmn_words_inp == "no":
            cmn_words = False
        else:
            cmn_words = False
    elif option == "2":
        cmn_words = False

        custom_words = True
        print("Using words specified in custom_words.txt\n")
    else:
        print("Error: Invalid Input")
        quit()

    sub = input("Which subreddit would you like to scan? ")
    amnt = int(input("How many comments should I read? "))

    r.scan(sub, amnt, cmn_words, custom_words)