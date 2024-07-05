import pandas as pd
import copy
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns


# STRUCTURE:
# 1. DEFINITIONS
# 2. FUNCTIONS
#   - load_data
#   - winrate
#   - total_games
#   - total_games_all
#   - total_tournaments
#   - fenster_winrate
#   - nemesis
#   - ultimate_nemesis
#   - ranks (barplot)
# 3. TESTS
#   - WL
#   - cups
#   - testAll

# DEFINITIONS
# -------------------------------------------------------------------------

spiele = None
plätze = None
players = None

# define player columns for spiele file
player_cols_spiele  = None
# define player columns for plätze file
player_cols_plätze = None

# -------------------------------------------------------------------------

# INITIALIZE
def load_data(df_spiele, df_plätze):
    global spiele, plätze, players, player_cols_plätze, player_cols_spiele
    spiele = df_spiele
    plätze = df_plätze
    spiele.fillna(value="", inplace = True)
    plätze.fillna(value="", inplace = True)

    # rename columns
    spiele = spiele.rename(columns = {'Player 1': 'p1', 'Player 2': 'p2', 'Player 3': 'p3', 'Player 4': 'p4', 
                                    'Player 5': 'p5', 'Player 6': 'p6', 'Teamname 1': 'tname1', 'Teamname 2': 'tname2',
                                    'Datum': 'datum', 'W/L Team 1': 'WLt1', 'W/L Team 2': 'WLt2', 'Becher übrig': 'becher',
                                    'Trickshot': 'trickshot', 'Fenster Team': 'fenster', 'Verlängerung': 'verl',
                                    'Becher P1': 'p1Becher', 'Becher P2': 'p2Becher', 'Becher P3': 'p3Becher', 
                                    'Becher T1': 't1Becher', 'Becher P4': 'p4Becher', 'Becher P5': 'p5Becher',
                                    'Becher P6': 'p6Becher', 'Becher T2': 't2Becher', '1v1': '1v1', 
                                    'X_Runden Regel': '5called', 'Eigentore': 'Eigentore'})

    # Apply str.strip() to remove trailing spaces from each cell
    spiele = spiele.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    
    # define player columns for spiele file
    player_cols_spiele  = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6']
    # define player columns for plätze file
    player_cols_plätze = ['Player 1', 'Player 2', 'Player 3']


    # define all player(names)
    players = pd.unique(spiele[player_cols_spiele].values.flatten())
    players = players.tolist()
    # remove empty name
    players = [value for value in players if value]
    # sort alphabetically
    players.sort()
    return spiele, plätze, players, player_cols_plätze, player_cols_spiele
# -------------------------------------------------------------------------

# WINRATE FUNCTION

# *args adds as many optional arguments as desired
def winrate(player, *args):
    if args:
        # output should not be printed
        output = 0
    else:
        # output should be printed
        output = 1
    df = spiele.copy(deep=True)
    pattern = rf'\b{player}\b'
    df = df[df[player_cols_spiele].apply(lambda row: row.str.contains(pattern).any(), axis=1)].reset_index(drop=True)
    
    team = -1
    games = 0
    wins = 0
    partner = {elem: [0, 0] for elem in players}
    # opponents: 2nd value = wins AGAINST opponent, 3rd value = winrate AGAINST opponent
    opponents = {elem: [0, 0] for elem in players}
    player_number = 'p0'
    cup_hit_rate = []
    cup_hit_rate_output = -1
    
    for i in range(len(df)):
        partner1, partner2 = '', ''
        
        if df.loc[i, 'p1'] == player:
            player_number = 'p1'
            team = 1
            partner1, partner2 = df.loc[i, 'p2'], df.loc[i, 'p3']
            opponent1, opponent2, opponent3, = df.loc[i, 'p4'], df.loc[i, 'p5'], df.loc[i, 'p6']
        elif df.loc[i, 'p2'] == player:
            player_number = 'p2'
            team = 1
            partner1, partner2 = df.loc[i, 'p1'], df.loc[i, 'p3']
            opponent1, opponent2, opponent3, = df.loc[i, 'p4'], df.loc[i, 'p5'], df.loc[i, 'p6']
        elif df.loc[i, 'p3'] == player:
            player_number = 'p3'
            team = 1
            partner1, partner2 = df.loc[i, 'p1'], df.loc[i, 'p2']
            opponent1, opponent2, opponent3, = df.loc[i, 'p4'], df.loc[i, 'p5'], df.loc[i, 'p6']
        elif df.loc[i, 'p4'] == player:
            player_number = 'p4'
            team = 2
            partner1, partner2 = df.loc[i, 'p5'], df.loc[i, 'p6']
            opponent1, opponent2, opponent3, = df.loc[i, 'p1'], df.loc[i, 'p2'], df.loc[i, 'p3']
        elif df.loc[i, 'p5'] == player:
            player_number = 'p5'
            team = 2
            partner1, partner2 = df.loc[i, 'p4'], df.loc[i, 'p6']
            opponent1, opponent2, opponent3, = df.loc[i, 'p1'], df.loc[i, 'p2'], df.loc[i, 'p3']
        elif df.loc[i, 'p6'] == player:
            player_number = 'p6'
            team = 2
            partner1, partner2 = df.loc[i, 'p4'], df.loc[i, 'p5']
            opponent1, opponent2, opponent3, = df.loc[i, 'p1'], df.loc[i, 'p2'], df.loc[i, 'p3']
        else:
            print(f"Player {player} not found in row {i}")
            continue
        
        # handle PARTNERS
        if partner1:
            partner[partner1][0] += 1
        if partner2:
            partner[partner2][0] += 1
        # add 3 player teams (don't know how yet)
        #if partner1 & partner2:
        #    partner[partner1 + "&"+ partner2][0] = 1
        
        # handle OPPONENTS
        if opponent1:
            opponents[opponent1][0] += 1
        if opponent2:
            opponents[opponent2][0] += 1
        if opponent3:
            opponents[opponent3][0] += 1
        
        # handle NUMBER OF GAMES
        games += 1
        if team == 1:
            current_win = df.loc[i, 'WLt1']
        else:
            current_win = df.loc[i, 'WLt2']
        
        # handle WINS
        if current_win:
            wins += 1
            if partner1:
                partner[partner1][1] += 1
            if partner2:
                partner[partner2][1] += 1
            if opponent1:
                opponents[opponent1][1] += 1
            if opponent2:
                opponents[opponent2][1] += 1
            if opponent3:
                opponents[opponent3][1] += 1
        
        # handle CUP_HIT_RATE
        player_cups_col = f'{player_number}Becher'
        team_cups_col = f't{team}Becher'
        num_players = -1
        if df.loc[i, player_cups_col] and [i, team_cups_col]:
            if partner1 and partner2:
                num_players = 3
            elif partner1:
                num_players = 2
            elif partner2:
                print("something wrong with cup_hit_rate and partners")
            else:
                num_players = 1
            hit_rate = df.loc[i, player_cups_col] / df.loc[i, team_cups_col] * max((num_players /2), 1)
            cup_hit_rate.append(hit_rate)
       
    
    winrate = wins / games * 100
    
    if cup_hit_rate:
        cup_hit_rate_output = np.mean(cup_hit_rate)*100
    
    for elem in partner:
        games_tmp = partner[elem][0]
        wins_tmp = partner[elem][1]
        if games_tmp != 0:
            winrate_tmp = wins_tmp / games_tmp
        else:
            winrate_tmp = 0
        partner[elem].append(winrate_tmp)
        
    for elem in opponents:
        games_tmp = opponents[elem][0]
        wins_tmp = opponents[elem][1]
        if games_tmp != 0:
            winrate_tmp = wins_tmp / games_tmp
        else:
            winrate_tmp = 0
        opponents[elem].append(winrate_tmp)
    
    # turn partner into df
    df_partner = pd.DataFrame.from_dict(partner, orient = 'index')
    df_partner.columns = ['Games', 'Wins', 'Winrate']
    df_partner.reset_index(inplace = True)
    df_partner.rename(columns={'index': 'Name'}, inplace = True)
    df_partner.sort_values('Winrate', ascending=False, inplace = True)
    # turn opp into df
    df_opponents = pd.DataFrame.from_dict(opponents, orient = 'index')
    df_opponents.columns = ['Games', 'Wins', 'Winrate']
    df_opponents.reset_index(inplace = True)
    df_opponents.rename(columns={'index': 'Name'}, inplace = True)
    df_opponents.sort_values('Winrate', ascending=True, inplace = True)
    
    # only print stuff if no optional args are given
    if output == 1:
        # print output
        print(f'{player}')
        print(f'Total games: {games}')
        print(f'Winrate: {winrate:.2f}%')
        # cup_hit_rate can only be printed when data exists (no data = -1)
        if cup_hit_rate_output > -1:
            print(f'Cup-hit-rate: {cup_hit_rate_output:.2f}%')
        print('----------------------------------------')
    returns = [df_partner, df_opponents, winrate, cup_hit_rate] 
    return returns

# -------------------------------------------------------------------------

# TOTAL GAMES FUNCTION

def total_games(player):
    df = spiele.copy(deep=True)
    pattern = rf'\b{player}\b'
    df = df[df[player_cols_spiele].apply(lambda row: row.str.contains(pattern).any(), axis=1)].reset_index(drop=True)
    
    return len(df)

# -------------------------------------------------------------------------

# TOTAL GAMES ALL FUNCTION
def total_games_all():
    print("total games of all players:")
    for elem in players: 
        print(f'{elem}: ', total_games(elem))
    return

# -------------------------------------------------------------------------

# TOTAL TOURNAMENTS FUNCTION

def total_tournaments(player):
    df = plätze.copy(deep=True)
    pattern = rf'\b{player}\b'
    df = df[df[player_cols_plätze].apply(lambda row: row.str.contains(pattern).any(), axis=1)].reset_index(drop=True)
    
    return len(df)

# -------------------------------------------------------------------------

# TOTAL TOURNAMENTS ALL FUNCTION

def total_tournaments_all():
    print("total tournaments of all players:")
    for elem in players: 
        print(f'{elem}: ', total_tournaments(elem))
    return

# -------------------------------------------------------------------------

# FENSTER_WINRATE FUNCTION

def fenster_winrate():
    df = spiele.copy(deep=True)
    df = df[df['fenster'] == 1]
    # since we made sure that team 1 is always fenster, we can just sum up the wins of team1 and divide by the total number of games which have a value in fenster
    print(sum(df['WLt1'])/len(df))
    return

# -------------------------------------------------------------------------

# NEMESIS FUNCTION

# min_games refers to the minimuim number of games AGAINST a specific opponent
# *args adds as many optional arguments as desired
def nemesis(player, min_games, *args):
    if args:
        # output should not be printed
        output = 0
    else:
        # output should be printed
        output = 1
    _, opp = winrate(player, 'no_output')
    if opp['Games'].max() < min_games:
        print(f'{player} does not have sufficient games.')
        return
    else:
        try:
            opp.drop(opp[opp.Games < min_games].index, inplace = True)
            opp.reset_index(drop=True, inplace = True)
            opp.sort_values('Winrate', ascending=True, inplace = True)
            name = opp.loc[0, 'Name']
            winrate_opp = opp.loc[0, 'Winrate']
            games = opp.loc[0, 'Games']
            if output == 1:
                print(f'{player}\'s Nemesis: {name} with a winrate of {winrate_opp} over {games} Games.')
        except KeyError as e:
            raise Exception(f'Player {player} has too few games (min_games: {min_games}) probably? {opp}') from e
        
    return opp

# -------------------------------------------------------------------------

# ULTIMATE NEMESIS FUNCTION

def ultimate_nemesis(min_games):
    min_games = min_games
    count = {elem: 0 for elem in players}
    for elem in players:
        opp = nemesis(elem, min_games, 'no_output')
        if isinstance(opp, pd.DataFrame):
            ult = opp.loc[0, 'Name']
            count[ult] += 1
        else:
            print(f'Opp was not a df, instead it is ', type(opp), opp)
    return count 

# -------------------------------------------------------------------------

# RANKS FUNCTION (BARPLOT)

def ranks(player):
    df = plätze.copy(deep=True)
    pattern = rf'\b{player}\b'
    df = df[df[player_cols_plätze].apply(lambda row: row.str.contains(pattern).any(), axis=1)].reset_index(drop=True)
    # transform platzierungen into relative ranks
    df['rel_rank'] = (df['Platzierung']-1)/df['Anzahl Teams']
    
    # Create a custom x-axis with equal spacing
    df['custom_x'] = df.index
    
    # not needed right now
    # create a col that has 'yes' in it if there were multiple tournaments on the same day, else 'no'
    # df['same_date'] = df.groupby('Datum')['Datum'].transform(lambda x: 'yes' if len(x) > 1 else 'no')
    
    # create col shift
    df['shift'] = (df['rel_rank'].diff().abs() <= 0.1).astype(int)
    
    # adjust figure size (to make it bigger go up in steps of 2 (eg 14,10))
    plt.figure(figsize=(12, 10))
    # adjust transparency with alpha
    sns.lineplot(data=df, x='custom_x', y='rel_rank', marker='o', alpha = 0.35)

    # Annotation
    for x, rel_rank, team, shift, rank, num_teams in zip(df['custom_x'], df['rel_rank'], df['Teamname'], df['shift'], df['Platzierung'], df['Anzahl Teams']):
        color = 'black'
        if rank == 1:
            color = '#fcc200' 
        # define initial offsets (-20, below the point) and (-10, below the point)
        offset_team = 21
        offset_rank = 11
        # which is to be adjusted based on the column shift
        if shift:
             offset_team  = -21
             offset_rank = -11
        else: 
            offset_team  = 21
            offset_rank = 11
        plt.annotate(f'{rank}/{num_teams}', (x, rel_rank), textcoords="offset points", xytext=(0,offset_rank), ha='center', fontsize=8, color = color)
        plt.gca().annotate(team, (x, rel_rank), textcoords="offset points", xytext=(0,offset_team), ha='center', fontsize=8, color='black', rotation=0)

    plt.ylim(1.0, -0.1)  # Invert y-axis
    plt.xlabel('Date')
    plt.ylabel('Relative Rank: rel_rank = (platzierung -1)/anzahl_teams')
    plt.title(f'Rankings Over Time for {player}')
    
    # Set the original dates as x-axis ticks
    date_mapping = dict(zip(df['custom_x'], df['Datum']))
    plt.xticks(df['custom_x'], [date_mapping[x].strftime('%Y-%m-%d') for x in df['custom_x']], rotation=45)
    
    # not exactly sure what this does
    plt.tight_layout()
    plt.show()
    
    return # df['rel_rank']

# -------------------------------------------------------------------------

# TESTS SECTION

# -------------------------------------------------------------------------

# W/L columns

def WLTest():
    # make sure either both teams lost (X Runden gecalled) or exactly one team lost and excatly one team won
    rule = spiele.apply(lambda row: (row['WLt1'], row['WLt2']) in [(0, 1), (1, 0), (0, 0)], axis=1)

    if rule.all():
        WLtestres = 1
    else:
        WLtestres = 0
    return WLtestres 

# -------------------------------------------------------------------------

# Cup hit columns 

def cupTest():
    check_df = spiele.copy(deep=True)
    # insert 0 if verl is empty
    check_df['verl'] = check_df['verl'].apply(lambda x: 0 if x == '' else x)
    check_df['max_cups'] = 6 + 3*check_df['verl']
    check_df.tail(20)

    cuptestres = 0
    # todo: check if max_cups == t1Becher if WLt1 == 1 and max_cups - Becher übrig = t2Becher 
    # und umgekehrt
    return cuptestres

# -------------------------------------------------------------------------

# -------------------------------------------------------------------------

# All test functions combined in one

def testAll():
    WL = WLTest()
    cups = cupTest()
    if WL and cups:
        print("alle Tests bestanden :)")
    elif not WL:
        print("Fehler in WLTest :(")
    elif not cups:
        print("Fehler in cupTest :(, muss noch fertig geschrieben werden.")
    else:
        print("Fehler in TestALL :(")
    
    return