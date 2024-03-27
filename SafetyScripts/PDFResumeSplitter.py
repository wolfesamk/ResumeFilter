#Script for pulling resumes in and splitting into unique paragraphs.


def readThisApp(filename):
    from pypdf import PdfReader
    import pandas as pd

    indir = 'Files/JobApps'
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
    df = df.replace(r'o ', '', regex=True)####

    #removing excess whitespace lines
    truth = False
    temp = []
    offset = 1
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
        if len(df.lines[r]) == 0:
            if temp in resumeParagraphs:
                temp=''
                continue
            resumeParagraphs.append(temp)
            temp = ''
            continue
        temp = temp+' '+df.lines[r]
        if temp[len(temp)-1] in [',','.']:
            continue
        elif temp[len(temp)-1] != '. ':
            temp = temp + '.'
    del pages,segmented,df,truth,temp,offset,offenders
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
    truth = False
    temp = []
    offset = 1
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
    del pages,segmented,df,truth,temp,offset,offenders
    return resumeParagraphs