# this script will focus on the "match system"
# https://trueskill.org/
import trueskill as ts
import mpmath
mpmath.mp.dps = 25
# import Rating, rate

def Game(df):
    # establishing default score columns    
    matches = ['score_relocation', 'score_pay','score_months', 'score_sentiment', 'score_education', 'score_classification', 'score_entity', 'score_keyword']

    # creating a numbers to satisfy ranges.
    r = len(df)

    # setting up trueskill
    ts.setup(backend='mpmath', draw_probability=(1/r))

    # creating the base player scores
    players = [ts.Rating() for x in range(r)]

    #initializing each player as their own team
    teams = [(players[i],) for i in range(r)]

    # creating new column for rank.
    temp = []
    for t in teams:
        temp.append(t[0].mu)
    df['rank'] = temp

    for m in matches:
        # ranks will be the index of the dataframe after sorting +1, so sort_values -> i+1 to get me a value between n and n+1
        ranks = []
        
        # sorting by the value of the column (m) to generate rank.
        df_sorted = df.sort_values(by=m, ascending=False)
        
        # score pay needs to be flipped
        if m == 'score_pay':
            df_sorted = df.sort_values(by=m, ascending=True)

        # checking to see if column is score_relocation. Because the values are either 0 or 1
        # I have to instead group by the columns value, 0 or 1, and then sort by mu.
        if m == 'score_relocation':
            
            # sorting by column 'score_relocation to separate 0 and 1, then sub sorting by rank.
            df_sorted = df.sort_values([m,'rank'], ascending=False)

        for i in df_sorted.index:
            ranks.append(i+1)
            
        # this runs the players on their teams through a match and recalculates their scores.
        # rate() outputs the same values as teams, just updated with the new content. So you can
        # reuse it over and over throughout the loop.
        teams = ts.rate(teams, ranks=ranks)
        temp1 = []
        temp2 = []
        for t in teams:
            temp1.append(t[0].mu)
            temp2.append(t[0].sigma)
        df['rank'] = temp1
        df['uncertainty'] = temp2
    
    # sorting by final ranks.
    df = df.sort_values('rank', ascending=False)
    return df
