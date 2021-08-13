
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
    listActions = [{'type': {'value': 6, 'displayName': 'CornerTaken'}},
                                        {'type': {'value': 107, 'displayName': 'ThrowIn'}},
                                        {'type': {'value': 5, 'displayName': 'FreekickTaken'}}]
    for dicte in x:
        for dict_action in listActions:
            if(dicte == dict_action):
                return True
    return False


fm_scada = FontManager(('https://github.com/googlefonts/scada/blob/main/fonts/ttf/'
                        'Scada-Regular.ttf?raw=true'))

mpl.rcParams['figure.dpi'] = 166

pitch = VerticalPitch(pitch_type='opta', pitch_color='#4D4D53', line_color='#c7d5cc',line_zorder=2)
fig, axs = pitch.grid(figheight=40, title_height=0, space=0.15, ncols = 3, nrows = 3,
              # Turn off the endnote/title axis. I usually do this after
              # I am happy with the chart layout and text placement
              axis=False,
              title_space=0, grid_height=0.85, endnote_height=0)

# fig, axs = pitch.grid(figheight=35, title_height=0.08, space=0.1, ncols = 3, nrows = 2,
#               # Turn off the endnote/title axis. I usually do this after
#               # I am happy with the chart layout and text placement
#               axis=False,
#               title_space=0, grid_height=0.85, endnote_height=0.02)


fig.set_facecolor('#4D4D53')

df2 = pd.read_csv("C:/Users/tomas/Documents/Benfica Data Driven Analysis/allEventsBenfica.csv")

df1 = df2.copy()


df2 = df2[df2['type']=="{'value': 1, 'displayName': 'Pass'}"]
df2 = df2[df2['outcomeType']=="{'value': 1, 'displayName': 'Successful'}"]

df_diogo_pre = df2[df2['playerId']==343029]
df_grimi_pre = df2[df2['playerId']==107252]
df_gilberto_pre = df2[df2['playerId']==119542]


df2 = df2[(df2['endX'] > 83.2) & (df2['endX'] < 100) & (df2['endY'] > 21) & (df2['endY'] < 79)]
df2 = df2[df2['teamId']==299]
df2['qualifiers'] = df2['qualifiers'].apply(ast.literal_eval)
df2['isRemovable'] = df2['qualifiers'].apply(searchQualifiers)
df2 = df2[df2['isRemovable']==False]


df_diogo = df2[df2['playerId']==343029]
df_grimi = df2[df2['playerId']==107252]
df_gilberto = df2[df2['playerId']==119542]

pearl_earring_cmap = LinearSegmentedColormap.from_list("Pearl Earring - 10 colors",
                                                       ['#4D4D53','#ED2C0E'], N=100)

df1['Recipient'] = df1['playerId'].shift(-1)
df1 = df1[df1['type']=="{'value': 1, 'displayName': 'Pass'}"]
df1 = df1[df1['outcomeType']=="{'value': 1, 'displayName': 'Successful'}"]
df_diogo_rc = df1[df1['Recipient']==343029]
df_grimi_rc = df1[df1['Recipient']==107252]
df_gilberto_rc = df1[df1['Recipient']==119542]

for count, ax in enumerate(axs['pitch'].flat):
    if(count == 0):
        pitch.arrows(df_diogo.x,df_diogo.y,df_diogo.endX,df_diogo.endY,ax=ax,color ="#ED2C0E", width = 1.4,headwidth=10,headlength=10)
    if(count == 1):
        pitch.arrows(df_gilberto.x,df_gilberto.y,df_gilberto.endX,df_gilberto.endY,ax=ax,color ="#ED2C0E", width = 1.4,headwidth=10,headlength=10) 
    if(count == 2):
        pitch.arrows(df_grimi.x,df_grimi.y,df_grimi.endX,df_grimi.endY,ax=ax,color ="#ED2C0E", width = 1.6,headwidth=10,headlength=10) 
    if(count == 3):
        kdeplot = pitch.kdeplot(df_diogo_pre.x,df_diogo_pre.y, ax=ax, cmap=pearl_earring_cmap, shade=True, levels=10,zorder = 1)
    if(count == 4):
        kdeplot = pitch.kdeplot(df_gilberto_pre.x,df_gilberto_pre.y, ax=ax, cmap=pearl_earring_cmap, shade=True, levels=10,zorder = 1)
    if(count == 5):
        kdeplot = pitch.kdeplot(df_grimi_pre.x,df_grimi_pre.y, ax=ax, cmap=pearl_earring_cmap, shade=True, levels=10,zorder = 1)
    if(count == 6):
        kdeplot = pitch.kdeplot(df_diogo_rc.x,df_diogo_rc.y, ax=ax, cmap=pearl_earring_cmap, shade=True, levels=10,zorder = 1)
    if(count == 7):
        kdeplot = pitch.kdeplot(df_gilberto_rc.x,df_gilberto_rc.y, ax=ax, cmap=pearl_earring_cmap, shade=True, levels=10,zorder = 1)
    if(count == 8):
        kdeplot = pitch.kdeplot(df_grimi_rc.x,df_grimi_rc.y, ax=ax, cmap=pearl_earring_cmap, shade=True, levels=10,zorder = 1)