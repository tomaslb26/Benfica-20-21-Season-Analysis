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

fm_scada = FontManager(('https://github.com/googlefonts/scada/blob/main/fonts/ttf/'
                        'Scada-Regular.ttf?raw=true'))

def clean(x):
    return x['displayName']

def cleanQualifiers(x):
    newList = []
    for y in x:
        newList += [y['type']['displayName']]
    return newList

def plotShots(new_df,ax):
    pitch.scatter(new_df[(new_df['type'] =="MissedShots") | (new_df['type'] =="ShotOnPost") | (new_df['type'] =="Goal") | (new_df['type'] =="SavedShot")].x,
                  new_df[(new_df['type'] =="MissedShots") | (new_df['type'] =="ShotOnPost") | (new_df['type'] =="Goal") | (new_df['type'] =="SavedShot")].y,
                  marker = "*", s = 60, ax = ax, color = "white", edgecolor = "white",lw = 3, zorder = 2)
    pitch.lines(new_df[(new_df['type'] =="SavedShot")].x,
                new_df[(new_df['type'] =="SavedShot")].y,
                new_df[(new_df['type'] =="SavedShot")].blockedX,
                new_df[(new_df['type'] =="SavedShot")].blockedY,
                ax = ax, color = "red", zorder = 1, comet = True)
    pitch.lines(new_df[(new_df['type'] =="MissedShots") | (new_df['type'] =="Goal") | (new_df['type'] =="ShotOnPost")].x,
                new_df[(new_df['type'] =="MissedShots") | (new_df['type'] =="Goal") | (new_df['type'] =="ShotOnPost")].y,
                new_df[(new_df['type'] =="MissedShots") | (new_df['type'] =="Goal") | (new_df['type'] =="ShotOnPost")].endX,
                new_df[(new_df['type'] =="MissedShots") | (new_df['type'] =="Goal") | (new_df['type'] =="ShotOnPost")].goalMouthY,
                ax = ax, color = "red", zorder = 1, comet = True)
    pitch.lines(new_df[(new_df['type'] =="Goal")].x,
                new_df[(new_df['type'] =="Goal")].y,
                new_df[(new_df['type'] =="Goal")].endX,
                new_df[(new_df['type'] =="Goal")].goalMouthY,
                ax = ax, color = "#19DA44", zorder = 2, comet = True)

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

mpl.rcParams['figure.dpi'] = 300

pitch = VerticalPitch( line_zorder=2, pitch_color='#4D4D53',line_color='white',pitch_type='opta')

#For First 3
# fig, axs = pitch.grid(figheight=13, title_height=0.08, space=0.1, ncols = 3, nrows = 1,
#               # Turn off the endnote/title axis. I usually do this after
#               # I am happy with the chart layout and text placement
#               axis=False,
#               title_space=0, grid_height=0.85, endnote_height=0.02)


fig, axs = pitch.grid(figheight=13, title_height=0.08, space=0.1, ncols = 2, nrows = 1,
              # Turn off the endnote/title axis. I usually do this after
              # I am happy with the chart layout and text placement
              axis=False,
              title_space=0, grid_height=0.85, endnote_height=0.02)

fig.set_facecolor('#4D4D53')

df2 = pd.read_csv("C:/Users/tomas/Benfica-20-21-Season-Analysis/Data/allTeamsCSV/allEventsBenfica.csv")

df2['type'] = df2['type'].apply(ast.literal_eval)
df2['type'] = df2['type'].apply(clean)
df2['outcomeType'] = df2['outcomeType'].apply(ast.literal_eval)
df2['outcomeType'] = df2['outcomeType'].apply(clean)
df2['qualifiers'] = df2['qualifiers'].apply(ast.literal_eval)
df2['qualifiers'] = df2['qualifiers'].apply(cleanQualifiers)

df1 = df2.copy()

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

df_transition = df2[((df2['type']=='Tackle') & (df2['outcomeType']=='Successful') & (df2['teamId']!=299) & (df2['nextTeam1']!=299)) |
                    ((df2['type']=='BallRecovery') & (df2['outcomeType']=='Successful') & (df2['teamId']!=299)& (df2['nextTeam1']!=299)) |
                    ((df2['type']=='BlockedPass') & (df2['outcomeType']=='Successful') & (df2['teamId']!=299)& (df2['nextTeam1']!=299)) |
                    ((df2['type']=='Clearance') & (df2['outcomeType']=='Successful') & (df2['teamId']!=299)& (df2['nextTeam1']!=299)) |
                    ((df2['type']=='Interception') & (df2['outcomeType']=='Successful') & (df2['teamId']!=299)& (df2['nextTeam1']!=299)) |
                    ((df2['type']=='BallTouch') & (df2['outcomeType']=='Unsuccessful') & (df2['teamId']==299)& (df2['nextTeam1']!=299))]

df_transition['removable'] = df_transition['Type1'].apply(removeDup)
df_transition = df_transition[df_transition['removable'] == False]
df_transition['removable'] = df_transition['Type2'].apply(removeDup)
df_transition = df_transition[df_transition['removable'] == False]
df_transition['removable'] = df_transition['Type3'].apply(removeDup)
df_transition = df_transition[df_transition['removable'] == False]
df_transition['removable'] = df_transition['Type4'].apply(removeDup)
df_transition = df_transition[df_transition['removable'] == False]

df_transition_1 = df_transition[(((df_transition['Type1'] == "SavedShot") | (df_transition['Type1'] == "MissedShots") | (df_transition['Type1'] == "ShotOnPost") | (df_transition['Type1'] == "Goal")) & (df_transition['nextTeam1']!=299))]
df_transition_2 = df_transition[(((df_transition['Type2'] == "SavedShot") | (df_transition['Type2'] == "MissedShots") | (df_transition['Type2'] == "ShotOnPost") | (df_transition['Type2'] == "Goal")) & (df_transition['nextTeam1']!=299) & (df_transition['nextTeam2']!=299))]
df_transition_3 = df_transition[(((df_transition['Type3'] == "SavedShot") | (df_transition['Type3'] == "MissedShots") | (df_transition['Type3'] == "ShotOnPost") | (df_transition['Type3'] == "Goal")) & (df_transition['nextTeam1']!=299) & (df_transition['nextTeam2']!=299) & (df_transition['nextTeam3']!=299)) ]
df_transition_4 = df_transition[(((df_transition['Type4'] == "SavedShot") | (df_transition['Type4'] == "MissedShots") | (df_transition['Type4'] == "ShotOnPost") | (df_transition['Type4'] == "Goal")) & (df_transition['nextTeam1']!=299) & (df_transition['nextTeam2']!=299) & (df_transition['nextTeam3']!=299) & (df_transition['nextTeam4']!=299))]
df_transition_5 = df_transition[(((df_transition['Type5'] == "SavedShot") | (df_transition['Type5'] == "MissedShots") | (df_transition['Type5'] == "ShotOnPost") | (df_transition['Type5'] == "Goal")) & (df_transition['nextTeam1']!=299) & (df_transition['nextTeam2']!=299) & (df_transition['nextTeam3']!=299) & (df_transition['nextTeam4']!=299) & (df_transition['nextTeam5']!=299))]
df_transition_6 = df_transition[(((df_transition['Type6'] == "SavedShot") | (df_transition['Type6'] == "MissedShots") | (df_transition['Type6'] == "ShotOnPost") | (df_transition['Type6'] == "Goal")) & (df_transition['nextTeam6']!=299) & (df_transition['nextTeam1']!=299) & (df_transition['nextTeam2']!=299) & (df_transition['nextTeam3']!=299) & (df_transition['nextTeam4']!=299) & (df_transition['nextTeam5']!=299)) ]
df_transition_7 = df_transition[(((df_transition['Type7'] == "SavedShot") | (df_transition['Type7'] == "MissedShots") | (df_transition['Type7'] == "ShotOnPost") | (df_transition['Type7'] == "Goal")) & (df_transition['nextTeam7']!=299) & (df_transition['nextTeam6']!=299) & (df_transition['nextTeam1']!=299) & (df_transition['nextTeam2']!=299) & (df_transition['nextTeam3']!=299) & (df_transition['nextTeam4']!=299) & (df_transition['nextTeam5']!=299)) ]
df_transition_8 = df_transition[(((df_transition['Type8'] == "SavedShot") | (df_transition['Type8'] == "MissedShots") | (df_transition['Type8'] == "ShotOnPost") | (df_transition['Type8'] == "Goal")) & (df_transition['nextTeam8']!=299) & (df_transition['nextTeam7']!=299) & (df_transition['nextTeam6']!=299) & (df_transition['nextTeam1']!=299) & (df_transition['nextTeam2']!=299) & (df_transition['nextTeam3']!=299) & (df_transition['nextTeam4']!=299) & (df_transition['nextTeam5']!=299)) ]
df_transition_9 = df_transition[(((df_transition['Type9'] == "SavedShot") | (df_transition['Type9'] == "MissedShots") | (df_transition['Type9'] == "ShotOnPost") | (df_transition['Type9'] == "Goal")) & (df_transition['nextTeam9']!=299) & (df_transition['nextTeam8']!=299) & (df_transition['nextTeam7']!=299) & (df_transition['nextTeam6']!=299) & (df_transition['nextTeam1']!=299) & (df_transition['nextTeam2']!=299) & (df_transition['nextTeam3']!=299) & (df_transition['nextTeam4']!=299) & (df_transition['nextTeam5']!=299))]



#First 3
# for count, ax in enumerate(axs['pitch'].flat):
#     if(count==0):
#         a = np.array(df_transition_1.index.tolist())
#         b = a+1

#         new_df = df1.loc[[x for y in zip(a,b) for x in y]]
#         new_df['x'].loc[new_df['teamId']==299] = 100 - new_df['x']
#         new_df['endX'] = new_df['x'].shift(-1)
#         new_df['endY'] = new_df['y'].shift(-1)
#         new_df['endX'].loc[(new_df['type'] =="MissedShots") | (new_df['type'] =="Goal") | (new_df['type'] =="ShotOnPost")] = 100
        
#         pitch.scatter(new_df[(new_df['type'] =="Tackle") | (new_df['type'] =="BallRecovery") | (new_df['type'] =="Interception") | (new_df['type'] =="BallTouch") | (new_df['type'] =="Clearance") | (new_df['type'] =="BlockedPass")].x,
#                       new_df[(new_df['type'] =="Tackle") | (new_df['type'] =="BallRecovery") | (new_df['type'] =="Interception") | (new_df['type'] =="BallTouch") | (new_df['type'] =="Clearance") | (new_df['type'] =="BlockedPass")].y,
#         s = 50, ax = ax, color = "white", edgecolor = "white", lw = 3, zorder = 2)
#         pitch.lines(new_df[(new_df['type'] =="Tackle") | (new_df['type'] =="BallRecovery") | (new_df['type'] =="Interception") | (new_df['type'] =="BallTouch") | (new_df['type'] =="BlockedPass")].x,
#                     new_df[(new_df['type'] =="Tackle") | (new_df['type'] =="BallRecovery") | (new_df['type'] =="Interception") | (new_df['type'] =="BallTouch") | (new_df['type'] =="BlockedPass")].y,
#                     new_df[(new_df['type'] =="Tackle") | (new_df['type'] =="BallRecovery") | (new_df['type'] =="Interception") | (new_df['type'] =="BallTouch") | (new_df['type'] =="BlockedPass")].endX,
#                     new_df[(new_df['type'] =="Tackle") | (new_df['type'] =="BallRecovery") | (new_df['type'] =="Interception") | (new_df['type'] =="BallTouch") | (new_df['type'] =="BlockedPass")].endY,
#                     ax = ax, color = "#3CACD8", zorder = 1, lw=1.5)

        
#     if(count == 1):
#         a = np.array(df_transition_2.index.tolist())
#         b = a+1
#         c = a+2

#         new_df = df1.loc[[x for y in zip(a,b,c) for x in y]]
#         new_df['x'].loc[new_df['teamId']==299] = 100 - new_df['x']
#         new_df['x1'] = new_df['x'].shift(-1)
#         new_df['y1'] = new_df['y'].shift(-1)
#         new_df['endX'].loc[(new_df['type'] =="MissedShots") | (new_df['type'] =="Goal") | (new_df['type'] =="ShotOnPost")] = 100
        
#         pitch.scatter(new_df[(new_df['type'] =="Tackle") | (new_df['type'] =="BallRecovery") | (new_df['type'] =="Interception") | (new_df['type'] =="BallTouch") | (new_df['type'] =="Clearance") | (new_df['type'] =="BlockedPass")].x,
#                       new_df[(new_df['type'] =="Tackle") | (new_df['type'] =="BallRecovery") | (new_df['type'] =="Interception") | (new_df['type'] =="BallTouch") | (new_df['type'] =="Clearance") | (new_df['type'] =="BlockedPass")].y,
#                         s = 50, ax = ax, color = "white", edgecolor = "white", lw = 3, zorder = 2)
#         pitch.lines(new_df[(new_df['type'] =="Tackle") | (new_df['type'] =="BallRecovery") | (new_df['type'] =="Interception") | (new_df['type'] =="BallTouch") | (new_df['type'] =="BlockedPass")].x,
#                     new_df[(new_df['type'] =="Tackle") | (new_df['type'] =="BallRecovery") | (new_df['type'] =="Interception") | (new_df['type'] =="BallTouch") | (new_df['type'] =="BlockedPass")].y,
#                     new_df[(new_df['type'] =="Tackle") | (new_df['type'] =="BallRecovery") | (new_df['type'] =="Interception") | (new_df['type'] =="BallTouch") | (new_df['type'] =="BlockedPass")].x1,
#                     new_df[(new_df['type'] =="Tackle") | (new_df['type'] =="BallRecovery") | (new_df['type'] =="Interception") | (new_df['type'] =="BallTouch") | (new_df['type'] =="BlockedPass")].y1,
#                     ax = ax, color = "#3CACD8", zorder = 1,lw=1.5)
#         pitch.arrows(new_df[new_df['type'] == "Pass"].x,
#                     new_df[new_df['type'] == "Pass"].y,
#                     new_df[new_df['type'] == "Pass"].endX,
#                     new_df[new_df['type'] == "Pass"].endY,
#                     ax = ax, color = "yellow", zorder = 1,width = 2,headwidth=5,headlength=5)
        
#         pitch.lines(new_df[new_df['type'] == "Pass"].endX,
#                     new_df[new_df['type'] == "Pass"].endY,
#                     new_df[new_df['type'] == "Pass"].x1,
#                     new_df[new_df['type'] == "Pass"].y1,
#                     ax = ax, color = "#3CACD8", zorder = 1, lw=1.5)
        
        
#     if(count == 2):
#         a = np.array(df_transition_3.index.tolist())
#         b = a+1
#         c = a+2
#         d = a+3

#         new_df = df1.loc[[x for y in zip(a,b,c,d) for x in y]]
#         new_df['x'].loc[new_df['teamId']==299] = 100 - new_df['x']
#         new_df['x1'] = new_df['x'].shift(-1)
#         new_df['y1'] = new_df['y'].shift(-1)
#         new_df['endX'].loc[(new_df['type'] =="MissedShots") | (new_df['type'] =="Goal") | (new_df['type'] =="ShotOnPost")] = 100
        
#         pitch.scatter(new_df[(new_df['type'] =="Tackle") | (new_df['type'] =="BallRecovery") | (new_df['type'] =="Interception") | (new_df['type'] =="BallTouch") | (new_df['type'] =="Clearance") | (new_df['type'] =="BlockedPass")].x,
#                       new_df[(new_df['type'] =="Tackle") | (new_df['type'] =="BallRecovery") | (new_df['type'] =="Interception") | (new_df['type'] =="BallTouch") | (new_df['type'] =="Clearance") | (new_df['type'] =="BlockedPass")].y,
#                       s = 50, ax = ax, color = "white", edgecolor = "white", lw = 3, zorder = 2)
#         pitch.lines(new_df[(new_df['type'] =="Tackle") | (new_df['type'] =="BallRecovery") | (new_df['type'] =="Interception") | (new_df['type'] =="BallTouch") | (new_df['type'] =="BlockedPass")].x,
#                     new_df[(new_df['type'] =="Tackle") | (new_df['type'] =="BallRecovery") | (new_df['type'] =="Interception") | (new_df['type'] =="BallTouch") | (new_df['type'] =="BlockedPass")].y,
#                     new_df[(new_df['type'] =="Tackle") | (new_df['type'] =="BallRecovery") | (new_df['type'] =="Interception") | (new_df['type'] =="BallTouch") | (new_df['type'] =="BlockedPass")].x1,
#                     new_df[(new_df['type'] =="Tackle") | (new_df['type'] =="BallRecovery") | (new_df['type'] =="Interception") | (new_df['type'] =="BallTouch") | (new_df['type'] =="BlockedPass")].y1,
#                     ax = ax, color = "#3CACD8", zorder = 1, lw=1.5)
#         pitch.arrows(new_df[new_df['type'] == "Pass"].x,
#                     new_df[new_df['type'] == "Pass"].y,
#                     new_df[new_df['type'] == "Pass"].endX,
#                     new_df[new_df['type'] == "Pass"].endY,
#                     ax = ax, color = "yellow", zorder = 1,width = 2,headwidth=5,headlength=5)
#         pitch.lines(new_df[new_df['type'] == "Pass"].endX,
#                     new_df[new_df['type'] == "Pass"].endY,
#                     new_df[new_df['type'] == "Pass"].x1,
#                     new_df[new_df['type'] == "Pass"].y1,
#                     ax = ax, color = "#3CACD8", zorder = 1, lw=1.5)
#         pitch.arrows(new_df[new_df['type'] == "Ball Touch"].x,
#                     new_df[new_df['type'] == "Ball Touch"].y,
#                     new_df[new_df['type'] == "Ball Touch"].x1,
#                     new_df[new_df['type'] == "Ball Touch"].y1,
#                     ax = ax, color = "yellow", zorder = 1,width = 2,headwidth=5,headlength=5)

        
        
        

#     plotShots(new_df,ax)
    
    
    
# Last 2
for count, ax in enumerate(axs['pitch'].flat):
    if(count==0):
        a = np.array(df_transition_4.index.tolist())
        b = a+1
        c = a+2
        d = a+3
        e = a+4

        new_df = df1.loc[[x for y in zip(a,b,c,d,e) for x in y]]
        new_df['x'].loc[new_df['teamId']==299] = 100 - new_df['x']
        new_df['x1'] = new_df['x'].shift(-1)
        new_df['y1'] = new_df['y'].shift(-1)
        new_df['endX'].loc[(new_df['type'] =="MissedShots") | (new_df['type'] =="Goal") | (new_df['type'] =="ShotOnPost")] = 100
        
        pitch.scatter(new_df[(new_df['type'] =="Tackle") | (new_df['type'] =="BallRecovery") | (new_df['type'] =="Interception") | (new_df['type'] =="BallTouch") | (new_df['type'] =="Clearance") | (new_df['type'] =="BlockedPass")].x,
                      new_df[(new_df['type'] =="Tackle") | (new_df['type'] =="BallRecovery") | (new_df['type'] =="Interception") | (new_df['type'] =="BallTouch") | (new_df['type'] =="Clearance") | (new_df['type'] =="BlockedPass")].y,
                      s = 50, ax = ax, color = "white", edgecolor = "white", lw = 3, zorder = 2)
        pitch.lines(new_df[(new_df['type'] =="Tackle") | (new_df['type'] =="BallRecovery") | (new_df['type'] =="Interception") | (new_df['type'] =="BallTouch") | (new_df['type'] =="BlockedPass")].x,
                    new_df[(new_df['type'] =="Tackle") | (new_df['type'] =="BallRecovery") | (new_df['type'] =="Interception") | (new_df['type'] =="BallTouch") | (new_df['type'] =="BlockedPass")].y,
                    new_df[(new_df['type'] =="Tackle") | (new_df['type'] =="BallRecovery") | (new_df['type'] =="Interception") | (new_df['type'] =="BallTouch") | (new_df['type'] =="BlockedPass")].x1,
                    new_df[(new_df['type'] =="Tackle") | (new_df['type'] =="BallRecovery") | (new_df['type'] =="Interception") | (new_df['type'] =="BallTouch") | (new_df['type'] =="BlockedPass")].y1,
                    ax = ax, color = "#3CACD8", zorder = 1, lw=1.5)
        pitch.arrows(new_df[new_df['type'] == "Pass"].x,
                    new_df[new_df['type'] == "Pass"].y,
                    new_df[new_df['type'] == "Pass"].endX,
                    new_df[new_df['type'] == "Pass"].endY,
                    ax = ax, color = "yellow", zorder = 1,width = 2,headwidth=5,headlength=5)
        pitch.lines(new_df[new_df['type'] == "Pass"].endX,
                    new_df[new_df['type'] == "Pass"].endY,
                    new_df[new_df['type'] == "Pass"].x1,
                    new_df[new_df['type'] == "Pass"].y1,
                    ax = ax, color = "#3CACD8", zorder = 1, lw=1.5)
        pitch.arrows(new_df[new_df['type'] == "Ball Touch"].x,
                    new_df[new_df['type'] == "Ball Touch"].y,
                    new_df[new_df['type'] == "Ball Touch"].x1,
                    new_df[new_df['type'] == "Ball Touch"].y1,
                    ax = ax, color = "yellow", zorder = 1,width = 2,headwidth=5,headlength=5)
    if(count==1):
        a = np.array(df_transition_5.index.tolist())
        b = a+1
        c = a+2
        d = a+3
        e = a+4
        f = a+5

        new_df = df1.loc[[x for y in zip(a,b,c,d,e,f) for x in y]]
        new_df['x'].loc[new_df['teamId']==299] = 100 - new_df['x']
        new_df['x1'] = new_df['x'].shift(-1)
        new_df['y1'] = new_df['y'].shift(-1)
        new_df['endX'].loc[(new_df['type'] =="MissedShots") | (new_df['type'] =="Goal") | (new_df['type'] =="ShotOnPost")] = 100
        
        pitch.scatter(new_df[(new_df['type'] =="Tackle") | (new_df['type'] =="BallRecovery") | (new_df['type'] =="Interception") | (new_df['type'] =="BallTouch") | (new_df['type'] =="Clearance") | (new_df['type'] =="BlockedPass")].x,
                      new_df[(new_df['type'] =="Tackle") | (new_df['type'] =="BallRecovery") | (new_df['type'] =="Interception") | (new_df['type'] =="BallTouch") | (new_df['type'] =="Clearance") | (new_df['type'] =="BlockedPass")].y,
                      s = 50, ax = ax, color = "white", edgecolor = "white", lw = 3, zorder = 2)
        pitch.lines(new_df[(new_df['type'] =="Tackle") | (new_df['type'] =="BallRecovery") | (new_df['type'] =="Interception") | (new_df['type'] =="BallTouch") | (new_df['type'] =="BlockedPass")].x,
                    new_df[(new_df['type'] =="Tackle") | (new_df['type'] =="BallRecovery") | (new_df['type'] =="Interception") | (new_df['type'] =="BallTouch") | (new_df['type'] =="BlockedPass")].y,
                    new_df[(new_df['type'] =="Tackle") | (new_df['type'] =="BallRecovery") | (new_df['type'] =="Interception") | (new_df['type'] =="BallTouch") | (new_df['type'] =="BlockedPass")].x1,
                    new_df[(new_df['type'] =="Tackle") | (new_df['type'] =="BallRecovery") | (new_df['type'] =="Interception") | (new_df['type'] =="BallTouch") | (new_df['type'] =="BlockedPass")].y1,
                    ax = ax, color = "#3CACD8", zorder = 1, lw=1.5)
        pitch.arrows(new_df[new_df['type'] == "Pass"].x,
                    new_df[new_df['type'] == "Pass"].y,
                    new_df[new_df['type'] == "Pass"].endX,
                    new_df[new_df['type'] == "Pass"].endY,
                    ax = ax, color = "yellow", zorder = 1,width = 2,headwidth=5,headlength=5)
        pitch.lines(new_df[new_df['type'] == "Pass"].endX,
                    new_df[new_df['type'] == "Pass"].endY,
                    new_df[new_df['type'] == "Pass"].x1,
                    new_df[new_df['type'] == "Pass"].y1,
                    ax = ax, color = "#3CACD8", zorder = 1, lw=1.5)
        pitch.arrows(new_df[new_df['type'] == "Ball Touch"].x,
                    new_df[new_df['type'] == "Ball Touch"].y,
                    new_df[new_df['type'] == "Ball Touch"].x1,
                    new_df[new_df['type'] == "Ball Touch"].y1,
                    ax = ax, color = "yellow", zorder = 1,width = 2,headwidth=5,headlength=5)
        
    plotShots(new_df,ax)