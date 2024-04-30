# This python object functions as Main for this program.
from SafetyScripts.HandyFunctions import clear
from SafetyScripts import Menu
clear()

menu_options = ['Process Candidates',
                'New Job Post',
                'First Time Setup',
                'Exit WolfGlyph Resume Recommendation System']

Menu.main_menu(menu_options)
