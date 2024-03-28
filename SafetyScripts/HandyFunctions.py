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
    print('Time: ', time)
    if time is None:
        print('1. Please use integers or floats.')
        sleep(3)
        return
    try:
        sleep(time)
    except:
        print('2. Please use integers or floats.')
        sleep(3)

def findPath():
    return os.getcwd()

def CountOccurrences(str, word):
    # split the string by spaces in a
    a = str.split(" ")
 
    # search for pattern in a
    count = 0
    for i in range(0, len(a)):
         
        # if match found increase count 
        if (word == a[i]):
           count = count + 1
            
    return count 