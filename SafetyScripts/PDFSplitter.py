#Script for pulling resumes in and splitting into unique paragraphs.
import numpy as np

def readThisApp(filename,jobID):
    from pypdf import PdfReader
    import pandas as pd

    indir = 'Files\JobApps\\'+jobID+'\Raw'
    # # creating a pdf reader object and combining all pages raw
    reader = PdfReader(f'{indir}/{filename}')
    pages = ''
    for p in range(len(reader.pages)):
        pages = pages+reader.pages[p].extract_text(extraction_mode='layout')
    segmented = pages.split('\n')

    #using Dataframe to reduce character count and format resume
    df = pd.DataFrame({'lines': segmented})
    df = df.replace(r'\s+', ' ', regex=True)
    df = df.replace(r'\A ', '', regex=True)
    df = df.replace(r'\A ', '', regex=True)
    df = df.replace(r'\A• ', '', regex=True)
    df = df.replace(r'[|]', '', regex=True)
    df = df.replace(r'\s+', ' ', regex=True)
    #df = df.replace(r'o ', '', regex=True)####

    #removing excess whitespace lines
    temp = []
    for r in df.index:
        if len(df.lines[r]) == 0:
            temp.append(r)
    offenders = []
    for x in temp:
        if (x+1) in temp:
            offenders.append(x)
    offenders.append(temp[len(temp)-1])
    df.drop(labels=offenders, axis=0,inplace=True)
    df.reset_index(inplace=True)

    #reducing paragraphs back to string and list format, cleaning up dataframe objects.
    resumeParagraphs = []
    temp = ''
    for r in df.index:
        line = df.lines[r]
        print(line)

        #checks if line exists in temp
        if line in temp and line !='':
            print(line)
            continue
        #checks for empty line
        if line == '':
            #if line is empty checks for current last character
            #else it adds a period.
            if temp[len(temp)-1] in ['.']:
                continue
            elif df.lines[r+1] == '':
                print('HERE')
                print(line)
                continue
            else:
                temp = temp +'.'
            #because we are at the end of a paragraph, adding bar for split later.
            temp = temp +'|'
        #last element check
        if r == 85:
            print('PENIS')
            print(len(df.index))
            print(r)
            print(line)
            print(df.lines[r])
        #if temp is blank, round one, temp is now set to new line.
        # else temp is now temp plus a space and a line.
        if temp == '':
            temp = line
        else:
            temp = temp + ' ' + line
    resumeParagraphs = temp.split('|')
    for p in resumeParagraphs:
        print(p)
    # for r in df.index:
        
    #     print('r='+str(r))
    #     print(df.lines[r])
    #     print('r='+str(r+1))
    #     print(df.lines[43])
        
    #     if len(df.lines[r]) == 0:
    #         print(1)
    #         if temp in resumeParagraphs:
    #             print(2)
    #             temp=''
    #             continue
    #         resumeParagraphs.append(temp)
    #         temp = ''
    #         continue
    #     print(3)
    #     temp = temp+' '+df.lines[r]
    #     if temp[len(temp)-1] in [',','.']:
    #         print(4)
    #         continue
    #     elif temp[len(temp)-1] != '.':
    #         print(5)
    #         if len(df.lines[r+1]) == 0:
    #             print(6)
    #         else:
    #             temp = temp + '.'
    # print(resumeParagraphs)
    return resumeParagraphs

def readThisJob(filename):
    from pypdf import PdfReader
    import pandas as pd

    indir = 'Files'
    # # creating a pdf reader object and combining all pages raw
    reader = PdfReader(f'{indir}/{filename}')
    pages = ''
    for p in range(len(reader.pages)):
        pages = pages+reader.pages[p].extract_text(extraction_mode='layout')
    segmented = pages.split('\n')

    #using Dataframe to reduce character count and format resume
    df = pd.DataFrame({'lines': segmented})
    df = df.replace(r'^\s+', ' ', regex=True)
    df = df.replace(r'\A ', ' ', regex=True)
    df = df.replace(r'\A ', '', regex=True)
    df = df.replace(r'\A• ', '', regex=True)
    df = df.replace(r'[|]', '', regex=True)
    df = df.replace(r'\s+', ' ', regex=True)
    df = df.replace(r'^\s+', '', regex=True)

    #removing excess whitespace lines
    temp = []
    for r in df.index:
        if len(df.lines[r]) == 0:
            temp.append(r)
    offenders = []
    for x in temp:
        if (x+1) in temp:
            offenders.append(x)
    offenders.append(temp[len(temp)-1])
    df.drop(labels=offenders, axis=0,inplace=True)

    #reducing paragraphs back to string and list format, cleaning up dataframe objects.
    resumeParagraphs = []
    temp = ''
    for r in df.index:
        x = df.lines[r]
        if len(x) == 0:
            if temp in resumeParagraphs:
                temp=''
                continue
            resumeParagraphs.append(temp)
            temp = ''
            continue
        temp = temp+' '+x
        if temp[len(temp)-1] in [',','.','/']:
            continue
    return resumeParagraphs