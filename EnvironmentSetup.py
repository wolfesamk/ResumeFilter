## This is a script to get all required libraries. Use when setting up new system to run with the program.
## Requires use of Python 3.12.0 Currently, may change as libs are updated or added.
## TODO: Create function to load list of supplied libraries at desired version number. pip install --force-reinstall -v "MySQL_python==1.2.2" is the syntax I am looking for.
## I can turn this into a great little script for automatically updating other peoples libraries too.
## Give it a menu and options. 1. BAU, runs current script. 2. Export users current library save only. 3. Import other users library save and force install that on your system. 4. Exit Program.
## TODO: Remove automatic update, will cause problems. Change to 1. BAU checks and installs libraries. 2. BAU+ Updates libraries 3. Export users current library save only. 4. Import other users library save and force install that on your system. 5. Exit Program.


## list of non standard libraries required.
extra_packages = ['numpy','pandas','pdfquery','tqdm','PyPDF2']

#### DO NOT EDIT BELOW THIS LINE ####

import sys
import subprocess
import os
from datetime import datetime
import pandas as pd

def install(packages):
    #basic library installer
    for package in packages:
        print('Installing: '+package)
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def saved_libs():
    #Loads the saved library from local file, must be in same location as EnvironmentSetup.py
    print('Loading Saved Library List')
    path = os.getcwd()
    files = os.listdir(path)
    lib_files = []
    for f in files:
        if 'lib' in f:
            lib_files.append(f)
    if len(lib_files) < 1:
        return False
    lib_files.sort(reverse=True)
    hist_libs = lib_files[0]
    try:
        temp_df = pd.read_csv(hist_libs)
    except:
        install(['pandas'])
        temp_df = pd.read_csv(hist_libs)
    return temp_df.library.to_list()
def save_cleanup():
    #keeps save clutter down to a maximum of 5
    path = os.getcwd()
    files = os.listdir(path)
    lib_files = []
    for f in files:
        if 'lib' in f:
            lib_files.append(f)
    if len(lib_files) < 1:
        return False
    if len(lib_files) > 5:
        lib_files.sort()
        for safety in range(len(lib_files)-5):
            os.remove(lib_files[safety])
            if safety > 5:
                print('To many saved lib files to safely cleanup, manual cleanup recommended.')
                break
        return False
    return True
def check():
    #basic check for outdated libraries
    print('Checking for outdated Libraries')
    reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'list','--outdated'])
    outdated_packages = [r.decode().split('==')[0] for r in reqs.split()]
    if len(outdated_packages) > 0:
        update(outdated_packages)
def update(packages):
    #basic update outdated libaries
    print('Updating outdated Libraries')
    for package in packages:
        print('Updating: '+package)
        subprocess.check_call([sys.executable, '-m', 'pip', 'install','--upgrade', package])
def installed():
    #basic list of installed libraries
    print('Checking for installed Libraries')
    reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
    return installed_packages
def installed_ver():
    #basic list of installed libraries and version
    print('Checking for installed Libraries and Version Number')
    reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    installed_packages = [r.decode().split('\r')[0] for r in reqs.split()]
    return installed_packages
def save_libs():
    #Saves current libraries for reference later
    print('Saving Libaries and Versions as CSV')
    lib_str = []
    lib_ver = []
    installed_vers = installed_ver()
    for lib in installed_vers:
        lstr,lver = lib.split('==',1)
        lib_str.append(lstr)
        lib_ver.append(lver)
    lib_dict = {'library': lib_str, 'version':lib_ver}
    import pandas as pd
    lib_df = pd.DataFrame(lib_dict)
    raw_time = datetime.now()
    current_date = raw_time.strftime('%b_%d_%Y')
    current_time = raw_time.strftime('%H_%M_%S')
    save_name = 'libs_'+current_date+'_'+current_time+'.csv'
    lib_df.to_csv(save_name,index=False)
    path = os.getcwd()
    print(save_name + ' has been saved to '+ path)
def historical(raw_packages):
    # checking for historical libraries and adding any missing from install to install list if not on list.
    print('Checking currently installed Libraries versus historically installed Libraries')
    pre_installed_packages = installed()
    pre_installed_packages.sort()
    hist_installed_packages = saved_libs()
    if hist_installed_packages == False:
        return raw_packages
    hist_installed_packages.sort()
    if pre_installed_packages == hist_installed_packages:
        print('Historical Libraries match Installed Libraries')
        diffs = []
    elif pre_installed_packages != hist_installed_packages:
        print('Historical Libraries DO NOT match Installed Libraries')
        diffs = list(set(hist_installed_packages) - set(pre_installed_packages))
    if len(diffs) > 0:
        for d in diffs:
            if d not in raw_packages:
                raw_packages.append()
    return raw_packages
def exists(prep_packages):
    #checks to see if requested packages are already installed, then installs anyt that are not installed.
    print('Installing Missing Libraries')
    pre_installed_packages = installed()
    pre_installed_packages.sort()
    packages=[]
    for package in prep_packages:
        if package not in pre_installed_packages:
            packages.append(package)
    if len(packages) > 0:
        install(packages)

def primary(raw_packages):
    #main function
    
    print('Starting Library Install')
    prep_packages = historical(raw_packages)
    exists(prep_packages)
    check()
    save_libs()
    truth = save_cleanup()
    if truth == False:
        print('Save Files were cleaned up')
        print('Goodbye')
    elif truth == True:
        print('Goodbye')

primary(extra_packages)