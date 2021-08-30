import numpy as np
from matplotlib import rcParams
from matplotlib.colors import to_rgba
from mplsoccer import Pitch, VerticalPitch, FontManager
from highlight_text import ax_text
from mplsoccer.statsbomb import read_event, EVENT_SLUG
import glob, os
import pandas as pd
import json
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import matplotlib as mpl
from modulesSoccer import offensiveTransitionClass
import ast

def clean(x):
    return x['displayName']

def cleanQualifiers(x):
    newList = []
    for y in x:
        newList += [y['type']['displayName']]
    return newList

def searchQualifiers(x):
    for dicte in x:
        if(dicte == "BigChanceCreated"):
            return True
    return False     

def searchForSetPieces(x):
    listActions = ['CornerTaken','ThrowIn','FreekickTaken','GoalKick']
    for dicte in x:
        for dict_action in listActions:
            if(dicte == dict_action):
                return True
    return False

def getSuccessfulDefensiveActions(df1,teamId,against=None):
    defensiveEvents = ['BallRecovery',
                       'Interception',
                       'Clearance',
                       'Tackle',
                       'BlockedPass']
    df2 = pd.DataFrame()
    if(against == True):
        df2 = df2.append(df1.loc[(df1["type"] == 'BallTouch') & (df1['teamId'] == teamId) & (df1['outcomeType'] == 'Unsuccessful')])
    else:
        df2 = df2.append(df1.loc[(df1["type"] == 'BallTouch') & (df1['teamId'] != teamId) & (df1['outcomeType'] == 'Unsuccessful')])
    for dicte in defensiveEvents:
        if(against == True):
            df2 = df2.append(df1.loc[(df1["type"] == dicte) & (df1["teamId"] != teamId)])
        else:
            df2 = df2.append(df1.loc[(df1["type"] == dicte) & (df1["teamId"] == teamId)])
    df2 = df2[df2['nextOutcome'] == 'Successful']
    if(against == True):
        df2 = df2[df2['nextTeamId'] != teamId]
    else:
        df2 = df2[df2['nextTeamId'] == teamId]
    df2['isRemovable'] = df2['nextQualifiers'].apply(searchForSetPieces)
    df2 = df2[df2['isRemovable'] == False]
    for dicte in defensiveEvents:
        df2 = df2.loc[(df2['nextType'] != 'BallRecovery') & 
                      (df2['nextType'] != 'Interception') & 
                      (df2['nextType'] != 'Clearance')    &
                      (df2['nextType'] != 'Tackle') &
                      (df2['nextType'] != 'BlockedPass')]
    return df2

def shiftTypes(df2):
    df2['nextType'] = df2['type'].shift(-1)
    df2['nextX'] = df2['x'].shift(-1)
    df2['nextY'] = df2['y'].shift(-1)
    df2['nextEndY'] = df2['endY'].shift(-1)
    df2['nextPlayerId'] = df2['playerId'].shift(-1)
    df2['nextEndX'] = df2['endX'].shift(-1)
    df2['nextOutcome'] = df2["outcomeType"].shift(-1)
    df2['nextQualifiers'] = df2['qualifiers'].shift(-1)
    df2['nextTeamId'] = df2['teamId'].shift(-1)
    return df2

def isProgressivePass(x,y,endX,endY):
    distanceInitial = np.sqrt(np.square(120 - x) + np.square(40 - y))
    distanceFinal = np.sqrt(np.square(120 - endX) + np.square(40 - endY))
    if(x <= 60 and endX <= 60):
        if(distanceInitial - distanceFinal > 30):
            return True
    elif(x <= 60 and endX > 60):
        if(distanceInitial - distanceFinal > 15):
            return True
    elif(x > 60 and endX > 60):
        if(distanceInitial - distanceFinal > 10):
            return True
    return False


mpl.rcParams['figure.dpi'] = 300

fm_scada = FontManager(('https://github.com/googlefonts/scada/blob/main/fonts/ttf/'
                        'Scada-Regular.ttf?raw=true'))

pitch = VerticalPitch( line_zorder=2, pitch_color='#4D4D53',line_color='white',pitch_type='opta')
fig, axs = pitch.grid(figheight=23, title_height=0.08, space=0.1, ncols = 3, nrows = 1,
              # Turn off the endnote/title axis. I usually do this after
              # I am happy with the chart layout and text placement
              axis=False,
              title_space=0, grid_height=0.85, endnote_height=0.02)

fig.set_facecolor('#4D4D53')

df2 = pd.read_csv("C:/Users/tomas/Documents/Benfica Data Driven Analysis/allEventsBenfica.csv")

df2['type'] = df2['type'].apply(ast.literal_eval)
df2['type'] = df2['type'].apply(clean)
df2['outcomeType'] = df2['outcomeType'].apply(ast.literal_eval)
df2['outcomeType'] = df2['outcomeType'].apply(clean)
df2['qualifiers'] = df2['qualifiers'].apply(ast.literal_eval)
df2['qualifiers'] = df2['qualifiers'].apply(cleanQualifiers)

df2 = shiftTypes(df2)

df2 = getSuccessfulDefensiveActions(df2,teamId = 299,against=True)

df2 = df2[(df2['nextType'] == 'Pass') & (df2['nextOutcome'] == "Successful")]

df2['progressive'] = df2.apply(lambda row: isProgressivePass(row['nextX'],row['nextY'],row['nextEndX'],row['nextEndY']), axis=1)

df2['nextX'] = 100 - df2['nextX']
df2['nextY'] = 100 - df2['nextY']
df2['nextEndX'] = 100 - df2['nextEndX']
df2['nextEndY'] = 100 - df2['nextEndY']

for count, ax in enumerate(axs['pitch'].flat):
    if(count == 0):
        pitch.arrows(df2[(df2['progressive'] == False) & (df2['nextX']>=66.6)].nextX,
            df2[(df2['progressive'] == False) & (df2['nextX']>=66.6)].nextY,
            df2[(df2['progressive'] == False) & (df2['nextX']>=66.6)].nextEndX,
            df2[(df2['progressive'] == False) & (df2['nextX']>=66.6)].nextEndY, color = "green", ax = ax,zorder = 1,width = 2,headwidth=10,headlength=10)
        pitch.lines(df2[(df2['progressive'] ==True) & (df2['nextX']>=66.6)].nextX,
                df2[(df2['progressive'] ==True) & (df2['nextX']>=66.6)].nextY,
                df2[(df2['progressive'] ==True) & (df2['nextX']>=66.6)].nextEndX,
                df2[(df2['progressive'] ==True) & (df2['nextX']>=66.6)].nextEndY,comet = True, color = "yellow", ax = ax, zorder = 2)
        pitch.scatter( df2[(df2['progressive'] ==True) & (df2['nextX']>=66.6)].nextEndX,
                       df2[(df2['progressive'] ==True) & (df2['nextX']>=66.6)].nextEndY, color = "#4D4D53",edgecolor = 'yellow', ax = ax, s = 600, zorder = 3, linewidth = 5)
    if(count == 1):
        pitch.arrows(df2[(df2['progressive'] == False) & (df2['nextX']<66.6) & (df2['nextX'] >= 33.3)].nextX,
            df2[(df2['progressive'] == False) & (df2['nextX']<66.6) & (df2['nextX'] >= 33.3)].nextY,
            df2[(df2['progressive'] == False) & (df2['nextX']<66.6) & (df2['nextX'] >= 33.3)].nextEndX,
            df2[(df2['progressive'] == False) & (df2['nextX']<66.6) & (df2['nextX'] >= 33.3)].nextEndY, color = "green", ax = ax,width = 2,headwidth=10,headlength=10)
        pitch.lines(df2[(df2['progressive'] ==True) & (df2['nextX']<66.6) & (df2['nextX'] >= 33.3)].nextX,
            df2[(df2['progressive'] ==True) & (df2['nextX']<66.6) & (df2['nextX'] >= 33.3)].nextY,
            df2[(df2['progressive'] ==True) & (df2['nextX']<66.6) & (df2['nextX'] >= 33.3)].nextEndX,
            df2[(df2['progressive'] ==True) & (df2['nextX']<66.6) & (df2['nextX'] >= 33.3)].nextEndY,comet = True, color = "yellow", ax = ax)
        pitch.scatter( df2[(df2['progressive'] ==True) & (df2['nextX']<66.6) & (df2['nextX'] >= 33.3)].nextEndX,
                       df2[(df2['progressive'] ==True) & (df2['nextX']<66.6) & (df2['nextX'] >= 33.3)].nextEndY, color = "#4D4D53",edgecolor = 'yellow', ax = ax, s = 600, zorder = 3, linewidth = 5)
    if(count == 2):
        pitch.arrows(df2[(df2['progressive'] == False) & (df2['nextX']<33.3)].nextX,
            df2[(df2['progressive'] == False) & (df2['nextX']<33.3)].nextY,
            df2[(df2['progressive'] == False) & (df2['nextX']<33.3)].nextEndX,
            df2[(df2['progressive'] == False) & (df2['nextX']<33.3)].nextEndY, color = "green", ax = ax, width = 2,headwidth=10,headlength=10)
        pitch.lines(df2[(df2['progressive'] ==True) & (df2['nextX']<33.3)].nextX,
                df2[(df2['progressive'] ==True) & (df2['nextX']<33.3)].nextY,
                df2[(df2['progressive'] ==True) & (df2['nextX']<33.3)].nextEndX,
                df2[(df2['progressive'] ==True) & (df2['nextX']<33.3)].nextEndY,comet = True, color = "yellow", ax = ax)
        pitch.scatter( df2[(df2['progressive'] ==True) & (df2['nextX']<33.3)].nextEndX,
                       df2[(df2['progressive'] ==True) & (df2['nextX']<33.3)].nextEndY, color = "#4D4D53",edgecolor = 'yellow', ax = ax, s = 600, zorder = 3, linewidth = 5)