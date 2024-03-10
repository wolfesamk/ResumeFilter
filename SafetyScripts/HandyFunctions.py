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