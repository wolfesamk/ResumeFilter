# this file is for the menus.
import os
import pandas as pd
from time import sleep
from SafetyScripts.HandyFunctions import clear
from SafetyScripts.FileSystemActions import BaseCheckForCreate,CreateJobPost
from SafetyScripts.Analytics import PrepImport, ScoreKeeper, KeywordCounter, NERScoring, GoogleJob, SubScoring
from SafetyScripts.Match import Game

def input_checker1(exit_num):
    # this function checks to ensure user input is valid.

    # requesting user input based on menu provided
    raw_input = input('>')

    # checking if user input can be converted to in format
    # if yes, it moves forward. If no, it returns 0 which restarts main menu
    try:
        raw_input = int(raw_input)

    # the exception that can happen is ValueError, telling user to only input
    # values between 1 and the highest menu number.
    except ValueError:
        clear()
        print('Please enter whole numbers between 1 and ',exit_num ,' only')
        sleep(3)
        clear()
        return 0

    # if the users input is a valid int, checks if value is between 0 and max +1
    # if true, returns in. otherwise restarts main menu.
    if (isinstance(raw_input,int)) == True and raw_input > 0 and raw_input < (exit_num+1):
        return raw_input

    # if input is valid in and not between 0 and max+1, telling user to only input
    # values between 1 and the highest menu number.
    else:
        clear()
        print('Please enter whole numbers between 1 and ',exit_num ,' only')
        sleep(3)
        clear()
        return 0

def input_checker2(text):
    # this function is a simple yes/no input verification.
    # because my program can rack up costs this is important.
    print('Are you certain you want to', text,'?')
    raw_input = input('y/n: ')
    accepted_inputs = ['y','Y','yes','YES','Yes']
    if raw_input in accepted_inputs:
        return True
    else:
        clear()
        return False
    
def input_checker3(jobID):
    # this function checks if jobID is valid
    path = os.getcwd()
    # # creates jobID directory location
    rawDir = path + '\\Files\\JobApps'
    jobList = os.listdir(rawDir)
    if jobID in jobList:
        truth = True
    else:
        print('Invalid jobID, please try again.')
        truth = False
    return truth

def case1():
    # this function processes candidates
    # defaulting truth and count
    truth = False
    count = 0
    # asking for user input on Job ID
    while truth is not True:
        jobID = input('Please enter Job Post ID: ')

        # checking if jobID is valid
        truth = input_checker3(jobID)
        count = count+1
        if count >= 3:
            print('To many incorrect jobID, returning to main Menu.')
            sleep(3)
            return

    # checking if certain files already exist.
    path = os.getcwd()

    # creates jobID directory location
    rawDir = path + '\\Files\\JobApps\\' + jobID

    # gathers all files in root dir for jobID
    fileList = os.listdir(rawDir)
    
    # calculating these elements every time is low cpu tax
    dfJobpost,dfKeywords,dfApplicants = PrepImport(jobID)

    # this checks if NER data is available to save on API Calls
    # if classification is not present, highly likely jobPost needs to be run
    if 'df_classification_'+jobID+'.csv' not in fileList:
        GoogleJob(dfJobpost)

    # if dfScoreKeeper is not present as a save file, process NERScoring.
    if 'dfScoreKeeper_'+jobID+'.csv' not in fileList:
        # creates new dfScoreKeeper to check for new applicants
        dfScoreKeeper = ScoreKeeper(dfApplicants,jobID)

        # runs them through first round of scoring
        dfScoreKeeper = KeywordCounter(dfApplicants, dfKeywords,dfScoreKeeper)
        dfScoreKeeper = NERScoring(jobID, dfApplicants, dfScoreKeeper)

    # else, import saved Keeper file. This overwrites previous dfScoreKeeper
    else:
        # imports existing dfScoreKeeper
        dfImport = pd.read_csv(rawDir+'\\'+'dfScoreKeeper_'+jobID+'.csv')

        # if the length of the existing dfScoreKeeper is less than dfApplicants,
        # we need to run the applicants through again.
        if len(dfImport.index) < len(dfApplicants.index):
            # creates new dfScoreKeeper to check for new applicants
            dfScoreKeeper = ScoreKeeper(dfApplicants,jobID)

            # runs them through first round of scoring
            dfScoreKeeper = KeywordCounter(dfApplicants, dfKeywords,dfScoreKeeper)
            dfScoreKeeper = NERScoring(jobID, dfApplicants, dfScoreKeeper)

        # opposite to catch everything else
        if len(dfImport.index) >= len(dfApplicants.index):
            dfScoreKeeper = dfImport

    clear()
    # processing dfScoreKeeper through subscoring, returning Scaled and non Scaled versions
    dfScoreKeeper, dfScoreKeeper_Scaled = SubScoring(jobID, dfJobpost, dfApplicants, dfScoreKeeper)
    clear()

    # pushing dfScoreKeeper_Scaled through the match system to rank candidates
    dfScoreKeeper_Scaled = Game(dfScoreKeeper_Scaled)

    # saving files
    dfScoreKeeper.to_csv(rawDir+'\\dfScoreKeeper_'+jobID+'.csv',index =False)
    dfScoreKeeper_Scaled.to_csv(rawDir+'\\dfScoreKeeper_Scaled_'+jobID+'.csv',index =False)

    # end of case1
    print('All files have been saved to:',rawDir,'\n')



def menu_case(inp,menu):
    # this function is a simple match case system to process the menu input
    menu_item = menu[int(inp)-1]
    match inp:
        case 1:
            # Processing Candidates through specified job post id
            truth = input_checker2(menu_item)
            if truth is True:
                case1()
            elif truth is False:
                return

        case 2:
            truth = input_checker2(menu_item)
            if truth is True:
                BaseCheckForCreate()
                CreateJobPost()
            elif truth is False:
                return
        case 3:
            truth = input_checker2(menu_item)
            if truth is True:
                BaseCheckForCreate()
            elif truth is False:
                return
        case 4:
            clear()
            print('Goodbye')
            sleep(2)
            clear()
            return

def main_menu(menu):
    # this is the main menu system function

    # setting the maximum menu length for exit value
    exit_num = len(menu)

    # defaulting menu input to 0
    menu_input = 0

    # for presentation purposes only, slows down the output first time program runs.
    first_time = 0

    # header text
    header = ['---WolfGlyph Resume Scoring System---','Please select from the following operations']
    # while loop to simulate program running. exits upon having the menu length entered.
    while menu_input != exit_num:

        # if first time has been flagged, prints menu as fast as possible.
        if first_time == 1:
            for h in header:
                print(h)
            for m in menu:
                number = str(menu.index(m)+1) +':'
                print(number,m)

        # if first time is not flagged, prints menu slowly for effect.
        elif first_time == 0:
            for h in header:
                print(h)
                sleep(.5)
            for m in menu:
                number = str(menu.index(m)+1) +':'
                print(number,m)
                sleep(.5)
            first_time = 1
        # checks for user input and verifies it is legitimate.
        menu_input = input_checker1(exit_num)
        #takes user input and runs in through the case system to perform menu action.
        menu_case(menu_input,menu)
