import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from mplsoccer import Pitch, VerticalPitch, FontManager
import numpy as np
from sklearn.cluster import KMeans
from modulesSoccer import offensiveTransitionClass
from scipy.spatial import distance
from matplotlib.colors import LinearSegmentedColormap
from scipy.ndimage import gaussian_filter
import ast

def clean(x):
    return x['displayName']

def cleanQualifiers(x):
    newList = []
    for y in x:
        newList += [y['type']['displayName']]
    return newList

def searchQualifiers(x,req):
    for dicte in x:
        if(dicte == req):
            return True
    return False     

fm_scada = FontManager(('https://github.com/googlefonts/scada/blob/main/fonts/ttf/'
                        'Scada-Regular.ttf?raw=true'))

mpl.rcParams['figure.dpi'] = 166

pitch = VerticalPitch(pitch_type='opta', pitch_color='#4D4D53', line_color='#c7d5cc',line_zorder=2, half=True)
fig, axs = pitch.grid(figheight=10, title_height=0.08, space=0.1, ncols = 3, nrows = 1,
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

df2['nextType1'] = df2['type'].shift(-1)
df2['nextTeam1'] = df2['teamId'].shift(-1)
df2['nextType2'] = df2['type'].shift(-2)
df2['nextTeam2'] = df2['teamId'].shift(-2)
df2['nextType3'] = df2['type'].shift(-3)
df2['nextTeam3'] = df2['teamId'].shift(-3)
df2['nextType4'] = df2['type'].shift(-4)
df2['nextTeam4'] = df2['teamId'].shift(-4)
df2['nextType5'] = df2['type'].shift(-5)

df2['Corner'] = df2.apply(lambda row: searchQualifiers(row.qualifiers,"CornerTaken"),axis=1)
df2['DirectFreeKick'] = df2.apply(lambda row: searchQualifiers(row.qualifiers,"DirectFreekick"),axis=1)
df2['FreeKick'] = df2.apply(lambda row: searchQualifiers(row.qualifiers,"FreekickTaken"),axis=1)
df_corner = df2[(df2['Corner'] == True) & (df2['teamId'] == 299)]
df_d_fk = df2[(df2['DirectFreeKick'] == True) & (df2['teamId'] == 299)]
df_fk = df2[(df2['FreeKick'] == True) & (df2['teamId'] == 299) & (df2['x']>50) & (df2['endX']>70)]

df_corner_goals = df_corner[((df_corner['nextType1']=="Goal")) 
                            | ((df_corner['nextType2']=="Goal") & (df_corner['nextType1']!="Foul")) 
                            | ((df_corner['nextType3']=="Goal") & (df_corner['nextType1']!="Foul") & (df_corner['nextType2']!="Foul"))
                            | ((df_corner['nextType4']=="Goal") & (df_corner['nextType1']!="Foul") & (df_corner['nextType2']!="Foul") & (df_corner['nextType3']!="Foul"))
                            | ((df_corner['nextType5']=="Goal") & (df_corner['nextType4']!="Foul") & (df_corner['nextType1']!="Foul") & (df_corner['nextType2']!="Foul") & (df_corner['nextType3']!="Foul"))]

df_fk_goals = df_fk[((df_fk['nextType1']=="Goal")) 
                            | ((df_fk['nextType2']=="Goal") & (df_fk['nextType1']!="Foul")) 
                            | ((df_fk['nextType3']=="Goal") & (df_fk['nextType1']!="Foul") & (df_fk['nextType2']!="Foul"))
                            | ((df_fk['nextType4']=="Goal") & (df_fk['nextType1']!="Foul") & (df_fk['nextType2']!="Foul") & (df_fk['nextType3']!="Foul"))
                            | ((df_fk['nextType5']=="Goal") & (df_fk['nextType4']!="Foul") & (df_fk['nextType1']!="Foul") & (df_fk['nextType2']!="Foul") & (df_fk['nextType3']!="Foul"))]


df_d_fk['endX'] = 100
for count, ax in enumerate(axs['pitch'].flat):
    if(count==0):
        arrows = pitch.scatter(df_corner.endX,df_corner.endY,ax=ax,
                      color = 'red', edgecolor = "#ED2C0E", zorder = 2, marker = "o", s = 300, alpha = 0.3)
        arrows = pitch.scatter(df_corner_goals.endX,df_corner_goals.endY,ax=ax,
                      color = '#14F63F', edgecolor = "#14F63F", zorder = 3, marker = "*", s = 400, lw = 3)
    if(count==1):
        # arrows = pitch.scatter(df_fk.endX,df_fk.endY,ax=ax,
        #               color = '#98A29A', edgecolor = "#ED2C0E", zorder = 2, marker = "8", s = 300)
        # arrows = pitch.scatter(df_fk_goals.endX,df_fk_goals.endY,ax=ax,
        #               color = '#14F63F', edgecolor = "green", zorder = 3, marker = "8", s = 400, lw = 3)
        arrows = pitch.lines(df_fk.x,df_fk.y,df_fk.endX,df_fk.endY,ax=ax,
                       color = '#ED2C0E', zorder = 2, comet=True)
        arrows = pitch.lines(df_fk_goals.x,df_fk_goals.y,df_fk_goals.endX,df_fk_goals.endY,ax=ax,
                       color = '#14F63F', edgecolor = "#14F63F", zorder = 3, comet=True)
    if(count==2):
        arrows = pitch.lines(df_d_fk[df_d_fk['type']=="SavedShot"].x,
                             df_d_fk[df_d_fk['type']=="SavedShot"].y,
                             df_d_fk[df_d_fk['type']=="SavedShot"].blockedX,
                             df_d_fk[df_d_fk['type']=="SavedShot"].blockedY,
                             ax=ax,
                             color = '#ED2C0E', zorder = 2, comet=True)
        arrows = pitch.lines(df_d_fk[df_d_fk['type']=="Goal"].x,
                             df_d_fk[df_d_fk['type']=="Goal"].y,
                             df_d_fk[df_d_fk['type']=="Goal"].endX,
                             df_d_fk[df_d_fk['type']=="Goal"].goalMouthY,
                             ax=ax,
                             color = '#14F63F', edgecolor = "#14F63F", zorder = 2, comet=True)
        arrows = pitch.lines(df_d_fk[df_d_fk['type']=="MissedShots"].x,
                             df_d_fk[df_d_fk['type']=="MissedShots"].y,
                             df_d_fk[df_d_fk['type']=="MissedShots"].endX,
                             df_d_fk[df_d_fk['type']=="MissedShots"].goalMouthY,
                             ax=ax,
                             color = '#98A29A', edgecolor = "#ED2C0E", zorder = 2, comet=True)

