import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from mplsoccer import Pitch, VerticalPitch, FontManager
import numpy as np
from sklearn.cluster import KMeans

fm_scada = FontManager(('https://github.com/googlefonts/scada/blob/main/fonts/ttf/'
                        'Scada-Regular.ttf?raw=true'))

mpl.rcParams['figure.dpi'] = 166

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
    

df2 = pd.read_csv("C:/Users/tomas/Documents/Benfica Data Driven Analysis/allEventsBenfica.csv")

df2['previousOutcome'] = df2["outcomeType"].shift(1)
df2['previousType'] = df2['type'].shift(1)
df2['previousTeamId'] = df2["teamId"].shift(1)

df2['Possession_Start'] = df2.apply(lambda row: isBallRecovery(row['previousType'],row['previousTeamId'],row['previousOutcome'],row['teamId'],row['type'],row['outcomeType'],row['qualifiers']),axis = 1)

df2['Prev_Possession_Start'] = df2['Possession_Start'].shift(1)
df2['Possession_Start'].loc[(df2['Prev_Possession_Start']=='ThrowIn') & (df2['type']=="{'value': 1, 'displayName': 'Pass'}")  ] = 1
df2 = df2.drop(columns = ['Prev_Possession_Start'])


df2['Possession_Sequence'] = False
df2['Possession_Sequence'].loc[(df2['x'] < 33.3) &  (df2['Possession_Start'] == True)] = 1

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

df_seq_3 = df2[df2['Possession_Sequence']==3]

df2['prev_sequence'] = df2['Possession_Sequence'].shift(1)

df2['Possession_Sequence'].loc[(df2['type'] == "{'value': 1, 'displayName': 'Pass'}") &  (df2['prev_sequence'] == 3) 
                               & (df2['outcomeType'] == "{'value': 1, 'displayName': 'Successful'}")
                               & (df2['teamId'] == 299) & (df2['previousOutcome'] == "{'value': 1, 'displayName': 'Successful'}")] = 4

df_seq_4 = df2[df2['Possession_Sequence']==4]

df2['prev_sequence'] = df2['Possession_Sequence'].shift(1)

df2['Possession_Sequence'].loc[(df2['type'] == "{'value': 1, 'displayName': 'Pass'}") &  (df2['prev_sequence'] == 4) 
                               & (df2['outcomeType'] == "{'value': 1, 'displayName': 'Successful'}")
                               & (df2['teamId'] == 299) & (df2['previousOutcome'] == "{'value': 1, 'displayName': 'Successful'}")] = 5

df_seq_5 = df2[df2['Possession_Sequence']==5]

df2['prev_sequence'] = df2['Possession_Sequence'].shift(1)

df2['Possession_Sequence'].loc[(df2['type'] == "{'value': 1, 'displayName': 'Pass'}") &  (df2['prev_sequence'] == 5) 
                               & (df2['outcomeType'] == "{'value': 1, 'displayName': 'Successful'}")
                               & (df2['teamId'] == 299) & (df2['previousOutcome'] == "{'value': 1, 'displayName': 'Successful'}")] = 6

df_seq_6 = df2[df2['Possession_Sequence']==6]

df2 = df2.drop(columns = ['previousOutcome','previousType','previousTeamId', 'Possession_Start','prev_sequence'])

pitch = VerticalPitch(pitch_type='opta', pitch_color='#4D4D53', line_color='#c7d5cc')

fig, axs = pitch.grid(figheight=30, title_height=0.08, space=0.1, ncols = 3, nrows = 2,
              # Turn off the endnote/title axis. I usually do this after
              # I am happy with the chart layout and text placement
              axis=False,
              title_space=0, grid_height=0.85, endnote_height=0.02)

fig.set_facecolor('#4D4D53')

# X = np.array(df_seq_1[['x','y','endX','endY']])
# kmeans = KMeans(n_clusters = 6, random_state = 100)
# kmeans.fit(X)
# df_seq_1['cluster'] = kmeans.predict(X)
# df_seq_2['cluster'] = kmeans.predict(X)
# df_seq_3['cluster'] = kmeans.predict(X)
# df_seq_4['cluster'] = kmeans.predict(X)
# df_seq_5['cluster'] = kmeans.predict(X)
# df_seq_6['cluster'] = kmeans.predict(X)


def showArrows(df):
    X = np.array(df[['x','y','endX','endY']])
    kmeans = KMeans(n_clusters = 5, random_state = 100)
    kmeans.fit(X)
    df['cluster'] = kmeans.predict(X)
    df.groupby('cluster')
    i = df['cluster'].value_counts()
    arrows = pitch.arrows(df[df['cluster']==i.index[0]].x,df[df['cluster']==i.index[0]].y,
                             df[df['cluster']==i.index[0]].endX,df[df['cluster']==i.index[0]].endY,ax=ax,
                      color = "red", zorder = 4, lw = 1, width = 1.4,headwidth=10,headlength=10)
    arrows = pitch.arrows(df[df['cluster']==i.index[1]].x,df[df['cluster']==i.index[1]].y,
                         df[df['cluster']==i.index[1]].endX,df[df['cluster']==i.index[1]].endY,ax=ax,
                  color = "blue", zorder = 4, lw = 1, width = 1.4,headwidth=10,headlength=10)
    arrows = pitch.arrows(df[df['cluster']==i.index[2]].x,df[df['cluster']==i.index[2]].y,
                         df[df['cluster']==i.index[2]].endX,df[df['cluster']==i.index[2]].endY,ax=ax,
                  color = "pink", zorder = 4, lw = 1, width = 1.4,headwidth=10,headlength=10)
    arrows = pitch.arrows(df[df['cluster']==i.index[3]].x,df[df['cluster']==i.index[3]].y,
                         df[df['cluster']==i.index[3]].endX,df[df['cluster']==i.index[3]].endY,ax=ax,
                  color = "yellow", zorder = 4, lw = 1, width = 1.4,headwidth=10,headlength=10)
    arrows = pitch.arrows(df[df['cluster']==i.index[4]].x,df[df['cluster']==i.index[4]].y,
                         df[df['cluster']==i.index[4]].endX,df[df['cluster']==i.index[4]].endY,ax=ax,
                  color = "purple", zorder = 4, lw = 1, width = 1.4,headwidth=10,headlength=10)
    # arrows = pitch.arrows(df[df['cluster']==i.index[5]].x,df[df['cluster']==i.index[5]].y,
    #                      df[df['cluster']==i.index[5]].endX,df[df['cluster']==i.index[5]].endY,ax=ax,
    #               color = "black", zorder = 4, lw = 1, width = 1.4,headwidth=10,headlength=10)

df_list = [df_seq_1,df_seq_2,df_seq_3,df_seq_4,df_seq_5,df_seq_6]    
        
for count, ax in enumerate(axs['pitch'].flat):
    showArrows(df_list[count])
    
axs['title'].text(-0.03, 1.2, "Where do Benfica direct their passes in buildup?", fontsize=65,fontproperties=fm_scada.prop,
                   color = "white",weight='bold')
axs['title'].text(-0.03, 0.9, "Liga Nos 20/21, first six passes of possessions starting in own third", fontsize=45,fontproperties=fm_scada.prop,
                   color = "white")

axs['title'].text(-0.05, 1.5, "W", fontsize=70,fontproperties=fm_scada.prop,
                   color = "#4D4D53")
axs['title'].text(1.05, 1.5, "W", fontsize=70,fontproperties=fm_scada.prop,
                   color = "#4D4D53")

plt.savefig(dpi=166,fname='C:/Users/tomas/Documents/Benfica Data Driven Analysis/Buildup.png')

