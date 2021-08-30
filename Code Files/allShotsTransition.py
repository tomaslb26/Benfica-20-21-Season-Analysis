import glob, os
import pandas as pd
import json
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from matplotlib import rcParams
from matplotlib.colors import to_rgba
from mplsoccer import Pitch, VerticalPitch, FontManager
from highlight_text import ax_text
from mplsoccer.statsbomb import read_event, EVENT_SLUG
import ast
import csv

def clean(x):
    return x['displayName']

def cleanQualifiers(x):
    newList = []
    for y in x:
        newList += [y['type']['displayName']]
    return newList

def cleanDF(df2):
    df2['type'] = df2['type'].apply(ast.literal_eval)
    df2['type'] = df2['type'].apply(clean)
    df2['outcomeType'] = df2['outcomeType'].apply(ast.literal_eval)
    df2['outcomeType'] = df2['outcomeType'].apply(clean)
    df2['qualifiers'] = df2['qualifiers'].apply(ast.literal_eval)
    df2['qualifiers'] = df2['qualifiers'].apply(cleanQualifiers)
    return df2

def shiftStuff(df2):
    df2['nextTeam1'] = df2['teamId'].shift(-1)
    df2['nextTeam2'] = df2['teamId'].shift(-2)
    df2['nextTeam3'] = df2['teamId'].shift(-3)
    df2['nextTeam4'] = df2['teamId'].shift(-4)
    df2['nextTeam5'] = df2['teamId'].shift(-5)
    df2['nextTeam6'] = df2['teamId'].shift(-6)
    df2['nextTeam7'] = df2['teamId'].shift(-7)
    df2['nextTeam8'] = df2['teamId'].shift(-8)
    df2['nextTeam9'] = df2['teamId'].shift(-9)
    df2['Type1'] = df2['type'].shift(-1)
    df2['Type2'] = df2['type'].shift(-2)
    df2['Type3'] = df2['type'].shift(-3)
    df2['Type4'] = df2['type'].shift(-4)
    df2['Type5'] = df2['type'].shift(-5)
    df2['Type6'] = df2['type'].shift(-6)
    df2['Type7'] = df2['type'].shift(-7)
    df2['Type8'] = df2['type'].shift(-8)
    df2['Type9'] = df2['type'].shift(-9)
    return df2

def removeDup(x):
    defensiveEvents = ['BallRecovery',
                       'Interception',
                       'Clearance',
                       'Tackle',
                       'BlockedPass']
    if(x in defensiveEvents):
        return True
    else:
        return False

def fix_transition(df_transition):
    df_transition['removable'] = df_transition['Type1'].apply(removeDup)
    df_transition = df_transition[df_transition['removable'] == False]
    df_transition['removable'] = df_transition['Type2'].apply(removeDup)
    df_transition = df_transition[df_transition['removable'] == False]
    df_transition['removable'] = df_transition['Type3'].apply(removeDup)
    df_transition = df_transition[df_transition['removable'] == False]
    df_transition['removable'] = df_transition['Type4'].apply(removeDup)
    df_transition = df_transition[df_transition['removable'] == False]
    df_transition['removable'] = df_transition['Type5'].apply(removeDup)
    df_transition = df_transition[df_transition['removable'] == False]
    return df_transition

def plotShots(new_df,ax):
    pitch.scatter(new_df[(new_df['type'] =="MissedShots") | (new_df['type'] =="ShotOnPost") | (new_df['type'] =="SavedShot")].x,
                  new_df[(new_df['type'] =="MissedShots") | (new_df['type'] =="ShotOnPost") | (new_df['type'] =="SavedShot")].y,
                  s = 60, ax = ax, color = "#E13835", zorder = 1)
    pitch.scatter(new_df[(new_df['type'] =="Goal")].x,
                new_df[(new_df['type'] =="Goal")].y,
                ax = ax, color = "#19DA44", zorder = 2, s = 60,edgecolors="white")


mpl.rcParams['figure.dpi'] = 300

# a fontmanager object for using a google font
fm_scada = FontManager(('https://github.com/googlefonts/scada/blob/main/fonts/ttf/'
                        'Scada-Regular.ttf?raw=true'))

fileList = []

os.chdir("C:/Users/tomas/Documents/Benfica Data Driven Analysis/Game Data/allTeamsCSV")
for file in glob.glob("*.csv"):
   fileList += ["C:/Users/tomas/Documents/Benfica Data Driven Analysis/Game Data/allTeamsCSV/" + file]
   
pitch = VerticalPitch(pitch_type='opta', pitch_color='#4D4D53', line_color='#c7d5cc',half=True)
fig, axs = pitch.grid(figheight=10, title_height=0, endnote_space=0, ncols = 6, nrows = 3,
              # Turn off the endnote/title axis. I usually do this after
              # I am happy with the chart layout and text placement
              axis=False,
              title_space=0, grid_height=0.85, endnote_height=0, space = 0.2)

fig.set_facecolor('#4D4D53')

teamDict = {'Benfica': [299], 'Famalicao': [935], 'Moreirense' : [108], 'Farense': [263],
            'RioAve': [121], 'Belenenses': [292], 'Boavista': [122], 'Braga': [288],
            'Maritimo': [264], 'Paços': [786], 'Vitoria': [107], 'GilVicente': [290],
            'Porto': [297], 'Portimonense': [1463], 'SantaClara': [251], 'Tondela': [8071],
            'Nacional': [936], 'Sporting': [296]}

for count, ax in enumerate(axs['pitch'].flat):
    # if(count == 6):
    #     break
    team_name = fileList[count].split("C:/Users/tomas/Documents/Benfica Data Driven Analysis/Game Data/allTeamsCSV/allEvents")
    team_name = team_name[1].split(".csv")
    team_name = team_name[0]
    team_id = teamDict[team_name][0]
    print(team_id)
    
    ax_text(100,40, team_name, ha='left', va='center', fontsize=30,
                fontproperties=fm_scada.prop, ax=ax, color = 'white',zorder=3)
    
    df2 = pd.read_csv(fileList[count])
    df2 = cleanDF(df2)
    df1 = df2.copy()
    
    df2 = shiftStuff(df2)
    
    df_transition = df2[((df2['type']=='Tackle') & (df2['outcomeType']=='Successful') & (df2['teamId']!=team_id) & (df2['nextTeam1']!=team_id)) |
                    ((df2['type']=='BallRecovery') & (df2['outcomeType']=='Successful') & (df2['teamId']!=team_id)& (df2['nextTeam1']!=team_id)) |
                    ((df2['type']=='BlockedPass') & (df2['outcomeType']=='Successful') & (df2['teamId']!=team_id)& (df2['nextTeam1']!=team_id)) |
                    ((df2['type']=='Clearance') & (df2['outcomeType']=='Successful') & (df2['teamId']!=team_id)& (df2['nextTeam1']!=team_id)) |
                    ((df2['type']=='Interception') & (df2['outcomeType']=='Successful') & (df2['teamId']!=team_id)& (df2['nextTeam1']!=team_id)) |
                    ((df2['type']=='BallTouch') & (df2['outcomeType']=='Unsuccessful') & (df2['teamId']==team_id)& (df2['nextTeam1']!=team_id))]

    df_transition = fix_transition(df_transition)
    
    df_transition_1 = df_transition[(((df_transition['Type1'] == "SavedShot") | (df_transition['Type1'] == "MissedShots") | (df_transition['Type1'] == "ShotOnPost") | (df_transition['Type1'] == "Goal")) & (df_transition['nextTeam1']!=team_id))]
    df_transition_2 = df_transition[(((df_transition['Type2'] == "SavedShot") | (df_transition['Type2'] == "MissedShots") | (df_transition['Type2'] == "ShotOnPost") | (df_transition['Type2'] == "Goal")) & (df_transition['nextTeam1']!=team_id) & (df_transition['nextTeam2']!=team_id))]
    df_transition_3 = df_transition[(((df_transition['Type3'] == "SavedShot") | (df_transition['Type3'] == "MissedShots") | (df_transition['Type3'] == "ShotOnPost") | (df_transition['Type3'] == "Goal")) & (df_transition['nextTeam1']!=team_id) & (df_transition['nextTeam2']!=team_id) & (df_transition['nextTeam3']!=team_id)) ]
    df_transition_4 = df_transition[(((df_transition['Type4'] == "SavedShot") | (df_transition['Type4'] == "MissedShots") | (df_transition['Type4'] == "ShotOnPost") | (df_transition['Type4'] == "Goal")) & (df_transition['nextTeam1']!=team_id) & (df_transition['nextTeam2']!=team_id) & (df_transition['nextTeam3']!=team_id) & (df_transition['nextTeam4']!=team_id))]
    df_transition_5 = df_transition[(((df_transition['Type5'] == "SavedShot") | (df_transition['Type5'] == "MissedShots") | (df_transition['Type5'] == "ShotOnPost") | (df_transition['Type5'] == "Goal")) & (df_transition['nextTeam1']!=team_id) & (df_transition['nextTeam2']!=team_id) & (df_transition['nextTeam3']!=team_id) & (df_transition['nextTeam4']!=team_id) & (df_transition['nextTeam5']!=team_id))]
    df_transition_6 = df_transition[(((df_transition['Type6'] == "SavedShot") | (df_transition['Type6'] == "MissedShots") | (df_transition['Type6'] == "ShotOnPost") | (df_transition['Type6'] == "Goal")) & (df_transition['nextTeam6']!=team_id) & (df_transition['nextTeam1']!=team_id) & (df_transition['nextTeam2']!=team_id) & (df_transition['nextTeam3']!=team_id) & (df_transition['nextTeam4']!=team_id) & (df_transition['nextTeam5']!=team_id)) ]
    
    list_transition = [df_transition_1,df_transition_2,df_transition_3,df_transition_4,df_transition_5,df_transition_6]
    
    numShots = 0
    count_rows=0
    for df in list_transition:
        a = np.array(df.index.tolist())
        b = a + count_rows + 1
        new_df = df1.loc[[x for y in zip(a,b) for x in y]]
        plotShots(new_df,ax)
        numShots += new_df[(new_df['type'] =="MissedShots") | (new_df['type'] =="ShotOnPost") | (new_df['type'] =="SavedShot") | (new_df['type'] =="Goal")].shape[0]
        count_rows += 1
    
    teamDict[team_name] += [numShots/34]
    

with open('C:/Users/tomas/Documents/Benfica Data Driven Analysis/Game Data/numShotsTransition.csv', 'w') as csv_file:  
    writer = csv.writer(csv_file)
    for key, value in teamDict.items():
       writer.writerow([key, value])
        
        