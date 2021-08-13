
import seaborn as sns
from mplsoccer import Pitch, VerticalPitch, FontManager
import numpy as np
from sklearn.cluster import KMeans
from modulesSoccer import offensiveTransitionClass
from scipy.spatial import distance
from matplotlib.colors import LinearSegmentedColormap
from scipy.ndimage import gaussian_filter
import matplotlib.lines as mlines
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
import ast

def searchQualifiers(x):
    for dicte in x:
        if(dicte['type']['displayName'] == "ShotAssist"):
            return True
        elif(dicte['type']['displayName'] == "IntentionalGoalAssist"):
            return True
        if(dicte['type']['displayName'] == "IntentionalAssist"):
            return True
    return False     

fm_scada = FontManager(('https://github.com/googlefonts/scada/blob/main/fonts/ttf/'
                        'Scada-Regular.ttf?raw=true'))

mpl.rcParams['figure.dpi'] = 166

pitch = VerticalPitch(pitch_type='opta', pitch_color='#4D4D53', line_color='#c7d5cc',line_zorder=2)
fig,ax = pitch.draw(figsize=(17,21))



fig.set_facecolor('#4D4D53')

df2 = pd.read_csv("C:/Users/tomas/Documents/Benfica Data Driven Analysis/allEventsBenfica.csv")

df1 = df2.copy()
df1['nextAction'] = df1['type'].shift(-1)
df1['previousX'] = df1['x'].shift(1)
df1['previousY'] = df1['y'].shift(1)
df1['previousEndX'] = df1['endX'].shift(1)
df1['previousEndY'] = df1['endY'].shift(1)
df1['previousType'] = df1['type'].shift(1)


          

df1 = df1[df1['playerId']==107252]
df1['qualifiers'] = df1['qualifiers'].apply(ast.literal_eval)
df1['isShotAssist'] = df1['qualifiers'].apply(searchQualifiers)
df1 = df1[df1['isShotAssist'] == True]

df1 = df1[df1['type']=="{'value': 1, 'displayName': 'Pass'}"]

pitch.scatter(df1[df1['previousType']=="{'value': 1, 'displayName': 'Pass'}"].previousEndX,
              df1[df1['previousType']=="{'value': 1, 'displayName': 'Pass'}"].previousEndY,
              color = 'green', edgecolor = "white", ax = ax, zorder = 2, s = 100)

pitch.lines(df1[df1['previousType']=="{'value': 1, 'displayName': 'Pass'}"].previousEndX,
            df1[df1['previousType']=="{'value': 1, 'displayName': 'Pass'}"].previousEndY,
            df1[df1['previousType']=="{'value': 1, 'displayName': 'Pass'}"].x,
            df1[df1['previousType']=="{'value': 1, 'displayName': 'Pass'}"].y,
            color = 'yellow', ax = ax, zorder = 1,lw=2)


pitch.scatter(df1.x,
              df1.y,
              color = 'yellow', edgecolor = "white", ax = ax, zorder = 2, s = 100)
pitch.lines(df1.x,
              df1.y,
              df1.endX,
              df1.endY,
              color = '#ED2C0E', ax = ax, zorder = 1, comet = True)


key = mlines.Line2D([], [], color='green', marker='o', linestyle='None',
                          markersize=20, label='', markeredgecolor = "white")
x1 = mlines.Line2D([], [], color='yellow', marker='o', linestyle='None',
                          markersize=20, label='', markeredgecolor = "white")


plt.legend(handles=[key,x1],  bbox_to_anchor = (0.4,0), 
            facecolor = '#4D4D53', edgecolor = 'none', labelcolor = 'none', 
            fontsize = 15, handletextpad = 6, ncol = 2)