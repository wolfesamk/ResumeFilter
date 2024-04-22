#Handy Functions
import os
from os import system, name
from time import sleep
def clear():
    """Clears Terminal"""
    if name == 'nt':
        _ = system('cls')

def wait(time=None):
    """Takes int input and sleeps x number of seconds"""
    if time is None:
        print('1. Please use integers or floats.')
        sleep(3)
        return
    try:
        sleep(time)
    except ValueError:
        print('2. Please use integers or floats.')
        sleep(3)

def findPath():
    return os.getcwd()

def CountOccurrences(str, word):
    import re
    
    str = re.sub('[^A-Za-z ]','', str)
    str = str.lower()
    word = re.sub('[^A-Za-z ]','', word)
    #word = re.sub('[.]','', word)
    word = word.lower()
    # split the string by spaces
    a = str.split(" ")

    # search for pattern in a
    count = 0
    for i in range(0, len(a)):
        # if match found increase count 
        if (word == a[i]):
           count = count + 1
            
    return count 