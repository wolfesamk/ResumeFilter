## This is a script to get all required libraries. Use when setting up new system to run with the program.
## Requires use of Python 3.12.0 Currently, may change as libs are updated or added.
## TODO: Create function to load list of supplied libraries at desired version number. pip install --force-reinstall -v "MySQL_python==1.2.2" is the syntax I am looking for.

## list of non standard libraries required.
extra_packages = ['numpy','pandas','tqdm','google-cloud-language','google-cloud-api-keys','scikit-learn','google-cloud-storage','trueskill','mpmath']
## NOTE: scikit-surprise == Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/

#### DO NOT EDIT BELOW THIS LINE ####

import sys
import subprocess
import os
from os import system, name
from time import sleep
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
    outdir = 'SafetyScripts\WolfGlyphEnvironmentSetup\Saves'
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    path = os.getcwd()
    files = os.listdir(path+'\\'+outdir)
    lib_files = []
    for f in files:
        if 'lib' in f:
            lib_files.append(f)
    if len(lib_files) < 1:
        return False
    lib_files.sort(reverse=True)
    hist_libs = lib_files[0]
    try:
        temp_df = pd.read_csv(f"{outdir}/{hist_libs}")
    except:
        install(['pandas'])
        temp_df = pd.read_csv(f"{outdir}/{hist_libs}")
    return temp_df.library.to_list()

def import_libs():
    #Loads exported library from local file, must be in same location as EnvironmentSetup.py
    print('Importing Saved Library List')
    try:
        temp_df = pd.read_csv('WGES_export.csv',header=0,index_col=False)
    except:
        install(['pandas'])
        temp_df = pd.read_csv('WGES_export.csv',header=0,index_col=False)
    installed_libs = []
    for pack in temp_df.index:
        temp_lib = []
        temp_lib.append(temp_df.library[pack])
        temp_lib.append(temp_df.version[pack])
        installed_libs.append(temp_lib)
    force_update(installed_libs)

def force_update(imported_libs):
    print('Force updating installed libraries to match import.')
    for package in imported_libs:
        print('Force Updating: '+ package[0])
        package_ver = package[0]+'=='+package[1]
        print(package_ver)
        subprocess.check_call([sys.executable, '-m', 'pip', 'install','--force-reinstall', '-v', package_ver])

def save_cleanup():
    #keeps save clutter down to a maximum of 5
    path = os.getcwd()
    outdir = 'SafetyScripts\WolfGlyphEnvironmentSetup\Saves'
    files = os.listdir(path+'\\'+outdir)
    lib_files = []
    for f in files:
        if 'lib' in f:
            lib_files.append(f)
    if len(lib_files) < 1:
        return False
    if len(lib_files) > 5:
        lib_files.sort()
        for safety in range(len(lib_files)-5):
            os.remove(f"{outdir}/{lib_files[safety]}")
            if safety > 5:
                print('To many saved lib files to safely cleanup, manual cleanup recommended.')
                break
        return False
    return True

def check():
    #basic check for outdated libraries
    print('Checking for outdated Libraries')
    reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'list','--outdated'])
    outdated_packages = [r.decode() for r in reqs.split()]
    if len(outdated_packages) <= 0:
        return
    for risk in range(8):
        outdated_packages.pop(0)
    temp_list = []
    x=0
    for risk in range(len(outdated_packages)):
        if risk != x:
            continue
        temp_list.append(outdated_packages[x])
        x=x+4
    outdated_packages = temp_list
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
    path = os.getcwd()
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
    outdir = 'SafetyScripts\WolfGlyphEnvironmentSetup\Saves'
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    lib_df.to_csv(f"{outdir}/{save_name}",index=False)
    print(save_name + ' has been saved to '+ path + '\\'+outdir)

def export_libs():
    #exports current libraries for sharing
    print('Exporting Libaries and Versions as CSV')
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
    outdir = 'SafetyScripts\WolfGlyphEnvironmentSetup'
    save_name = 'WGES_export.csv'
    lib_df.to_csv(outdir+"\\"+save_name,index=False)
    path = os.getcwd()
    print(save_name + ' has been saved to '+ path +'\\'+outdir)

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
                raw_packages.append(d)
    return raw_packages

def exists(prep_packages):
    #checks to see if requested packages are already installed, then installs any that are not installed.
    print('Installing Missing Libraries')
    pre_installed_packages = installed()
    pre_installed_packages.sort()
    packages=[]
    for package in prep_packages:
        if package not in pre_installed_packages:
            packages.append(package)
    if len(packages) > 0:
        install(packages)

def case1(raw_packages):
    #1. First time environment setup, library list only, no updates.
    clear()
    print('Starting Library Install')
    prep_packages = historical(raw_packages)
    exists(prep_packages)
    save_libs()
    truth = save_cleanup()
    if truth == False:
        print('Save Files were cleaned up')
        print()
    elif truth == True:
        print()

def case2(raw_packages):
    #2. First time environment setup, library list only, with updates. *DANGEROUS*
    clear()
    print('Starting Library Install')
    prep_packages = historical(raw_packages)
    exists(prep_packages)
    check()
    save_libs()
    truth = save_cleanup()
    if truth == False:
        print('Save Files were cleaned up')
        print()
    elif truth == True:
        print()

def case3():
    export_libs()
   
def case4():
    import_libs()

def case5():
    check()

def clear():
    if name == 'nt':
        _ = system('cls')

def startup():
    clear()
    print(menu_options[0])
    loading = ['Loading...','...','...','...','...Loaded']
    for m in loading:
        print(m)
        sleep(1)
    sleep(2)
    clear()
    print(menu_options[0])
    clear()

def input_checker1():
    raw_input = input('>')
    try:
        raw_input = int(raw_input)
    except:
        clear()
        print('Please enter whole numbers between 1 and 6 only')
        sleep(3)
        clear()
        return 0
    if (isinstance(raw_input,int)) == True and raw_input > 0 and raw_input < 7:
        return raw_input
    else:
        clear()
        print('Please enter whole numbers between 1 and 6 only')
        sleep(3)
        clear()
        return 0
    
def input_checker2():
    raw_input = input('Are you certain? y/n: ')
    accepted_inputs = ['y','Y','yes','YES','Yes']
    if raw_input in accepted_inputs:
        return True
    else:
        clear()
        return False

def menu_case(inp):
    match inp:
        case 1:
            case1(extra_packages)
        case 2:
            truth = input_checker2()
            if truth == True:
                case2(extra_packages)
            elif truth == False:
                return
        case 3:
            case3()
        case 4:
            truth = input_checker2()
            if truth == True:
                case4()
            elif truth == False:
                return
        case 5:
            truth = input_checker2()
            if truth == True:
                case5()
            elif truth == False:
                return
        case 6:
            clear()
            print('System Control Offline')
            sleep(2)
            print('Goodbye')
            sleep(2)           
            return

def main_menu(menu):
    menu_input = 0
    first_time = 0
    while menu_input != 6:
        if first_time == 1:
            for m in menu:
                print(m)
        elif first_time == 0:
            for m in menu:
                print(m)
                sleep(.5)
            first_time = 1
        menu_input = input_checker1()
        menu_case(menu_input)

menu_options = ['---WolfGlyph Environment Setup---',
            'Please select from the following operations',
            '1. First time environment setup, library list only, no updates.',
            '2. First time environment setup, library list only, with updates. *DANGEROUS*',
            '3. Export current library.',
            '4. Import and override current library. *DANGEROUS*',
            '5. Update all libraries. *DANGEROUS*',
            '6. Exit WolfGlyph Environment Setup']
startup()
main_menu(menu_options)
clear()