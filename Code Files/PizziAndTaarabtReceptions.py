
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

def cleanDF(playerId,df):
    dfpreclean = df[df['Recipient']==playerId]
    dfclean = dfpreclean[['endX','endY','nextX','nextY','nextEndX','nextEndY','Recipient','nextType','nextOutcome']]
    return dfclean

def plotActions(df,ax):
    df_test = df[(df['nextType'] == "{'value': 3, 'displayName': 'TakeOn'}") & (df['nextOutcome']=="{'value': 0, 'displayName': 'Unsuccessful'}")]
    pitch.scatter(df[(df['nextType'] == "{'value': 3, 'displayName': 'TakeOn'}") & (df['nextOutcome']=="{'value': 1, 'displayName': 'Successful'}")].nextX,df[(df['nextType'] == "{'value': 3, 'displayName': 'TakeOn'}") & (df['nextOutcome']=="{'value': 1, 'displayName': 'Successful'}")].nextY,color = "green",edgecolors= 'white',ax = ax,s=550, zorder = 2, marker = 'x')
    pitch.scatter(df.endX,df.endY,color = "green",edgecolors= 'white',ax = ax,s=150, zorder = 2)
    pitch.scatter(df[(df['nextType'] == "{'value': 1, 'displayName': 'Pass'}")].nextX,df[(df['nextType'] == "{'value': 1, 'displayName': 'Pass'}")].nextY,color = "red",edgecolors= 'white',ax = ax,s=150,zorder = 1)
    arrows = pitch.lines(df.endX,df.endY,df.nextX,df.nextY,ax=ax,
              color = "black", zorder = 4, lw = 1)
    arrows = pitch.arrows(df[(df['nextOutcome']=="{'value': 0, 'displayName': 'Unsuccessful'}") & (df['nextType'] == "{'value': 1, 'displayName': 'Pass'}")].nextX,
                          df[(df['nextOutcome']=="{'value': 0, 'displayName': 'Unsuccessful'}") & (df['nextType'] == "{'value': 1, 'displayName': 'Pass'}")].nextY,
                          df[(df['nextOutcome']=="{'value': 0, 'displayName': 'Unsuccessful'}") & (df['nextType'] == "{'value': 1, 'displayName': 'Pass'}")].nextEndX,
                          df[(df['nextOutcome']=="{'value': 0, 'displayName': 'Unsuccessful'}") & (df['nextType'] == "{'value': 1, 'displayName': 'Pass'}")].nextEndY,ax=ax,
                  color = "red" , edgecolor = "white", zorder = 1, width = 1.4,headwidth=10,headlength=10)
    arrows = pitch.arrows(df[(df['nextOutcome']=="{'value': 1, 'displayName': 'Successful'}") & (df['nextType'] == "{'value': 1, 'displayName': 'Pass'}")].nextX,
                          df[(df['nextOutcome']=="{'value': 1, 'displayName': 'Successful'}") & (df['nextType'] == "{'value': 1, 'displayName': 'Pass'}")].nextY,
                          df[(df['nextOutcome']=="{'value': 1, 'displayName': 'Successful'}") & (df['nextType'] == "{'value': 1, 'displayName': 'Pass'}")].nextEndX,
                          df[(df['nextOutcome']=="{'value': 1, 'displayName': 'Successful'}") & (df['nextType'] == "{'value': 1, 'displayName': 'Pass'}")].nextEndY,ax=ax,
                  color = "green" , edgecolor = "white", zorder = 1, width = 1.4,headwidth=10,headlength=10)
    pitch.scatter(df_test.nextX,df_test.nextY,
                  color = "red",edgecolors= 'white',ax = ax,s=550,zorder = 5,marker='x')
    pitch.scatter(df[(df['nextOutcome']=="{'value': 0, 'displayName': 'Unsuccessful'}") & (df['nextType'] == "{'value': 61, 'displayName': 'BallTouch'}")].nextX,df[(df['nextOutcome']=="{'value': 0, 'displayName': 'Unsuccessful'}") & (df['nextType'] == "{'value': 61, 'displayName': 'BallTouch'}")].nextY,color = "red",edgecolors= 'white',ax = ax,s=150, zorder = 2, marker = 's')
    pitch.scatter(df[(df['nextOutcome']=="{'value': 1, 'displayName': 'Successful'}") & (df['nextType'] == "{'value': 61, 'displayName': 'BallTouch'}")].nextX,df[(df['nextOutcome']=="{'value': 1, 'displayName': 'Successful'}") & (df['nextType'] == "{'value': 61, 'displayName': 'BallTouch'}")].nextY,color = "green",edgecolors= 'white',ax = ax,s=150, zorder = 2, marker = 's')
    pitch.scatter(df[(df['nextType'] == "{'value': 4, 'displayName': 'Foul'}")].nextX,df[(df['nextType'] == "{'value': 4, 'displayName': 'Foul'}")].nextY,color = "green",edgecolors= 'white',ax = ax,s=150, zorder = 2, marker = '^')

def isBallRecovery(prevEventType,prevTeamId,outcome,teamId,eventType,outcomeCurrent,qualifiers):
    defensiveEvents = ["{'value': 49, 'displayName': 'BallRecovery'}",
                    "{'value': 8, 'displayName': 'Interception'}",
                  "{'value': 12, 'displayName': 'Clearance'}",
                    "{'value': 7, 'displayName': 'Tackle'}",
                    "{'value': 74, 'displayName': 'BlockedPass'}"]
    if(prevEventType in defensiveEvents and
        prevTeamId == 299 and teamId == 299 and 
        outcome == "{'value': 1, 'displayName': 'Successful'}" and
        eventType == "{'value': 1, 'displayName': 'Pass'}"):
        return True
    if(searchQualifiers(qualifiers) and eventType == "{'value': 1, 'displayName': 'Pass'}"
         and teamId == 299):
        return True
    elif("{'type': {'value': 107, 'displayName': 'ThrowIn'}}" in qualifiers and eventType == "{'value': 1, 'displayName': 'Pass'}"
         and teamId == 299):
        return "ThrowIn"
    else:
        return False
    
def searchQualifiers(x):
    listActions = ["{'type': {'value': 5, 'displayName': 'FreekickTaken'}}",
                                        "{'type': {'value': 124, 'displayName': 'GoalKick'}}"]
    for dict_action in listActions:
        if(dict_action in x):
            return True

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

df2 = pd.read_csv("C:/Users/tomas/Documents/Benfica Data Driven Analysis/allEventsBenfica.csv")

df2['previousOutcome'] = df2["outcomeType"].shift(1)
df2['previousType'] = df2['type'].shift(1)
df2['previousTeamId'] = df2["teamId"].shift(1)

df2['Possession_Start'] = df2.apply(lambda row: isBallRecovery(row['previousType'],row['previousTeamId'],row['previousOutcome'],row['teamId'],row['type'],row['outcomeType'],row['qualifiers']),axis = 1)

df2['Prev_Possession_Start'] = df2['Possession_Start'].shift(1)
df2['Possession_Start'].loc[(df2['Prev_Possession_Start']=='ThrowIn') & (df2['type']=="{'value': 1, 'displayName': 'Pass'}")  ] = 1
df2 = df2.drop(columns = ['Prev_Possession_Start'])


df2['Possession_Sequence'] = False
df2['Possession_Sequence'].loc[(df2['x'] < 33.3) &  (df2['Possession_Start'] == True) & (df2['outcomeType'] == "{'value': 1, 'displayName': 'Successful'}")] = 1


df2['Recipient'] = df2['playerId'].shift(-1)
df2['nextOutcome'] = df2['outcomeType'].shift(-1)
df2['nextType'] = df2['type'].shift(-1)
df2['nextX'] = df2['x'].shift(-1)
df2['nextY'] = df2['y'].shift(-1)
df2['nextEndY'] = df2['endY'].shift(-1)
df2['nextEndX'] = df2['endX'].shift(-1)

df_seq_1 = df2[df2['Possession_Sequence']==1]

df2['prev_sequence'] = df2['Possession_Sequence'].shift(1)

df2['Possession_Sequence'].loc[(df2['type'] == "{'value': 1, 'displayName': 'Pass'}") &  (df2['prev_sequence'] == 1) 
                               & (df2['outcomeType'] == "{'value': 1, 'displayName': 'Successful'}")
                               & (df2['teamId'] == 299) & (df2['previousOutcome'] == "{'value': 1, 'displayName': 'Successful'}")] = 2

df_seq_2 = df2[df2['Possession_Sequence']==2]

df2['prev_sequence'] = df2['Possession_Sequence'].shift(1)

df2['Possession_Sequence'].loc[(df2['type'] == "{'value': 1, 'displayName': 'Pass'}") &  (df2['prev_sequence'] == 2) 
                               & (df2['outcomeType'] == "{'value': 1, 'displayName': 'Successful'}")
                               & (df2['teamId'] == 299) & (df2['previousOutcome'] == "{'value': 1, 'displayName': 'Successful'}")] = 3
df2 = df2.drop(columns = ['previousOutcome','previousType','previousTeamId', 'Possession_Start'])
df_seq_3 = df2[df2['Possession_Sequence']==3]


# df_pizzi = df_seq_1[df_seq_1['Recipient']==81928]
# df_taarabt = df_seq_1[df_seq_1['Recipient']==24642]
# df_pizzi_clean = df_pizzi[['endX','endY','nextX','nextY','nextEndX','nextEndY','Recipient','nextType','nextOutcome']]
# df_taarabt_clean = df_taarabt[['endX','endY','nextX','nextY','nextEndX','nextEndY','Recipient','nextType','nextOutcome']]

# df_pizzi_test = df_seq_2[df_seq_2['Recipient']==81928]
# df_pizzi_clean_test = df_pizzi_test[['endX','endY','nextX','nextY','nextEndX','nextEndY','Recipient','nextType','nextOutcome']]

    
seqs = [df_seq_1,df_seq_2,df_seq_3]
for count, ax in enumerate(axs['pitch'].flat):
    if(count==0):
        for df in seqs:
            plotActions(cleanDF(81928,df), ax)
    else:
        for df in seqs:
            plotActions(cleanDF(24642,df), ax)
        
big = mlines.Line2D([], [], color='green', marker='o', linestyle='None',
                          markersize=45, label='Reception', markeredgecolor = "white")
key = mlines.Line2D([], [], color='red', marker='o', linestyle='None',
                          markersize=45, label='Pass Location', markeredgecolor = "white")
x1 = mlines.Line2D([], [], color='none', marker='s', linestyle='None',
                          markersize=45, label='Ball Touch', markeredgecolor = "white")
x3 = mlines.Line2D([], [], color='red', marker='x', linestyle='None',
                          markersize=45, label='Take-On', markeredgecolor = "white")
x2 = mlines.Line2D([], [], color='none', marker='^', linestyle='None',
                          markersize=45, label='Foul', markeredgecolor = "white")

x4 = mlines.Line2D([], [], color='#4D4D53', marker='^', linestyle='None',
                          markersize=1, label='Green = Successful', markeredgecolor = "#4D4D53")
x5 = mlines.Line2D([], [], color='#4D4D53', marker='^', linestyle='None',
                          markersize=1, label='Red = Unuccessful', markeredgecolor = "#4D4D53")

plt.legend(handles=[big,key,x1,x3,x2], loc="lower right", 
            facecolor = '#4D4D53', edgecolor = '#565051', labelcolor = 'white', 
            fontsize = 40, handletextpad = 0.2, ncol = 5 )

plt.savefig(dpi=166,fname='C:/Users/tomas/Documents/Benfica Data Driven Analysis/receptions.png')


        