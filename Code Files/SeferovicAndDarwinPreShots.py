import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from mplsoccer import Pitch, VerticalPitch, FontManager
import os
import ast

def clean(x):
    return x['displayName']

def cleanQualifiers(x):
    newList = []
    for y in x:
        newList += [y['type']['displayName']]
    return newList

def getColor(x):
    if(x == "Goal"):
        return "green"
    else:
       return "#ED2C0E"

fm_scada = FontManager(('https://github.com/googlefonts/scada/blob/main/fonts/ttf/'
                        'Scada-Regular.ttf?raw=true'))

mpl.rcParams['figure.dpi'] = 166

pitch = VerticalPitch(pitch_type='opta', pitch_color='#4D4D53', line_color='#c7d5cc',line_zorder=2)

fig, axs = pitch.grid(figheight=35, title_height=0.08, space=0.1, ncols = 2, nrows = 1,
              # Turn off the endnote/title axis. I usually do this after
              # I am happy with the chart layout and text placement
              axis=False,
              title_space=0, grid_height=0.85, endnote_height=0.02)


fig.set_facecolor('#4D4D53')

# path = os.path.join(os.path.expanduser('~'), 'Desktop', 'python', 'file.txt')
# print(path)

df2 = pd.read_csv("/home/tomas/Desktop/Benfica-20-21-Season-Analysis/Data/allTeamsCSV/allEventsBenfica.csv")




df2['type'] = df2['type'].apply(ast.literal_eval)
df2['type'] = df2['type'].apply(clean)
df2['qualifiers'] = df2['qualifiers'].apply(ast.literal_eval)
df2['qualifiers'] = df2['qualifiers'].apply(cleanQualifiers)


df2['prevTeamId'] = df2['teamId'].shift(1)
df2['prevOutcome'] = df2['outcomeType'].shift(1)
df2['prevType'] = df2['type'].shift(1)
df2['previousX'] = df2['x'].shift(1)
df2['previousY'] = df2['y'].shift(1)
df2['previousEndX'] = df2['endX'].shift(1)
df2['previousEndY'] = df2['endY'].shift(1)

df2 = df2[(df2['type']=="MissedShots") | (df2['type']=="Goal") | (df2['type']=="SavedShot") | (df2['type']=="ShotOnPost")]

df2 = df2[(df2['playerId'] == 74016) | (df2['playerId']==400828)]
df2['color'] = df2['type'].apply(getColor)

df2 = df2[df2['prevType']=="Pass"]


for count, ax in enumerate(axs['pitch'].flat):
    if(count==0):
        pitch.lines(df2[df2['playerId']==74016].previousEndX,df2[df2['playerId']==74016].previousEndY,
                    df2[df2['playerId']==74016].x,df2[df2['playerId']==74016].y,
                    color = 'white', ax=ax)
        pitch.scatter(df2[df2['playerId']==74016].x,df2[df2['playerId']==74016].y,
                      color=df2[df2['playerId']==74016].color,
                      marker = "8",ax = ax,s=300)
    if(count==1):
        pitch.lines(df2[df2['playerId']==400828].previousEndX,df2[df2['playerId']==400828].previousEndY,
                    df2[df2['playerId']==400828].x,df2[df2['playerId']==400828].y,
                    color = 'white', ax=ax)
        pitch.scatter(df2[df2['playerId']==400828].x,df2[df2['playerId']==400828].y,
                      color=df2[df2['playerId']==400828].color,
                      marker = "8",ax = ax,s=300)
