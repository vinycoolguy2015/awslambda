import random

WORDLIST_FILENAME = "words.txt"

def loadWords():
    inFile = open(WORDLIST_FILENAME, 'r')
    line = inFile.readline()
    wordlist = line.split()
    return wordlist

def chooseWord(wordlist):
    return random.choice(wordlist)

def isWordGuessed(secretWord, lettersGuessed):
    for letter in secretWord:
        if not letter in lettersGuessed:
            return False
    return True

def getGuessedWord(secretWord, lettersGuessed):
    string=('_ '*len(secretWord)).strip()
    list=string.split()
    for letter in secretWord:
        if letter in lettersGuessed:
            for i in range(len(secretWord)):
                if secretWord[i]==letter:
                    list[i]=letter
    return ''.join(list)

def getAvailableLetters(lettersGuessed):
    import string
    global letters
    letters=string.ascii_lowercase
    for letter in lettersGuessed:
        if letter in letters:
            letters=letters.replace(letter,'')
    return letters
   
def hangman(secretWord):
    allowed_attempts=8
    incorrect_guesses=0
    lettersGuessed=[]
    wordGuessed=False
    print("Welcome to the game, Hangman!\nI am thinking of a word that is "+str(len(secretWord))+" letters long.\n-------------")
    while (incorrect_guesses < 8) and (wordGuessed==False):
        print("You have "+str((allowed_attempts-incorrect_guesses))+" guesses left.")
        print("Available letters: "+getAvailableLetters(lettersGuessed))
        letter=raw_input("Please guess a letter: ")[0]
        lettersGuessed.append(letter)
        if lettersGuessed.count(letter) > 1:
                print("Oops! You've already guessed that letter "+getGuessedWord(secretWord, lettersGuessed))
                print('-----------')
        elif letter in secretWord:
            print("Good guess: "+getGuessedWord(secretWord, lettersGuessed))
            print('-----------')
            getAvailableLetters(lettersGuessed)
        else:
            print("Oops! That letter is not in my word: "+getGuessedWord(secretWord, lettersGuessed))
            print('-----------')
            incorrect_guesses=incorrect_guesses+1
        if isWordGuessed(secretWord, lettersGuessed):
            wordGuessed=True
            print("Congratulations, you won!")
            return
    print("Sorry, you ran out of guesses. The word was "+secretWord)

wordlist = loadWords()
hangman(chooseWord(wordlist))
