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

def clean(x):
    return x['displayName']

def cleanQualifiers(x):
    newList = []
    for y in x:
        newList += [y['type']['displayName']]
    return newList

def plot_and_cluster(df,pitch,ax):
    X = np.array(df[['x','y','endX','endY']])
    kmeans = KMeans(n_clusters = 12, random_state = 100)
    kmeans.fit(X)
    df['cluster'] = kmeans.predict(X)
    i = df['cluster'].value_counts()
    arrows = pitch.arrows(df[df['cluster']==i.index[0]].x,df[df['cluster']==i.index[0]].y,
                             df[df['cluster']==i.index[0]].endX,df[df['cluster']==i.index[0]].endY,ax=ax,
                      color = "red", zorder = 5, lw = 1, width = 0.7,headwidth=5,headlength=5)
    arrows = pitch.arrows(df[df['cluster']==i.index[1]].x,df[df['cluster']==i.index[1]].y,
                         df[df['cluster']==i.index[1]].endX,df[df['cluster']==i.index[1]].endY,ax=ax,
                  color = "blue", zorder = 4, lw = 1, width = 0.7,headwidth=5,headlength=5)
    arrows = pitch.arrows(df[df['cluster']==i.index[2]].x,df[df['cluster']==i.index[2]].y,
                         df[df['cluster']==i.index[2]].endX,df[df['cluster']==i.index[2]].endY,ax=ax,
                  color = "pink", zorder = 3, lw = 1, width = 0.7,headwidth=5,headlength=5)
    arrows = pitch.arrows(df[df['cluster']==i.index[3]].x,df[df['cluster']==i.index[3]].y,
                         df[df['cluster']==i.index[3]].endX,df[df['cluster']==i.index[3]].endY,ax=ax,
                  color = "yellow", zorder = 2, lw = 1, width = 0.7,headwidth=5,headlength=5)
    arrows = pitch.arrows(df[df['cluster']==i.index[4]].x,df[df['cluster']==i.index[4]].y,
                         df[df['cluster']==i.index[4]].endX,df[df['cluster']==i.index[4]].endY,ax=ax,
                  color = "purple", zorder = 1, lw = 1, width = 0.7,headwidth=5,headlength=5)

mpl.rcParams['figure.dpi'] = 166

pitch = VerticalPitch(pitch_type='opta', pitch_color='#4D4D53', line_color='#c7d5cc',line_zorder=1)

fig, axs = pitch.grid(figheight=12, title_height=0.08, space=0.1, ncols = 3, nrows = 2,
              # Turn off the endnote/title axis. I usually do this after
              # I am happy with the chart layout and text placement
              axis=False,
              title_space=0, grid_height=0.85, endnote_height=0.02)


fig.set_facecolor('#4D4D53')




df2 = pd.read_csv("C:/Users/tomas/Benfica-20-21-Season-Analysis/Data/allTeamsCSV/allEventsBenfica.csv")

df2['type'] = df2['type'].apply(ast.literal_eval)
df2['type'] = df2['type'].apply(clean)
df2['qualifiers'] = df2['qualifiers'].apply(ast.literal_eval)
df2['qualifiers'] = df2['qualifiers'].apply(cleanQualifiers)

df2 = df2[df2['type'] == "Pass"]

weigl_df = df2[(df2['playerId']==142318)]
pizzi_df = df2[(df2['playerId']==81928)]
taarabt_df = df2[(df2['playerId']==24642)]


df_list = [weigl_df[(weigl_df['x']<=50) & (weigl_df['x']>=25)],
           pizzi_df[(pizzi_df['x']<=50) & (pizzi_df['x']>=25)],
           taarabt_df[(taarabt_df['x']<=50) & (taarabt_df['x']>=25)],
           weigl_df[(weigl_df['x']<=75) & (weigl_df['x']>=50)],
           pizzi_df[(pizzi_df['x']<=75) & (pizzi_df['x']>=50)],
           taarabt_df[(taarabt_df['x']<=75) & (taarabt_df['x']>=50)]]


for count, ax in enumerate(axs['pitch'].flat):
    plot_and_cluster(df_list[count],pitch,ax)
    if(count == 0):
        rect = patches.Rectangle((0,25),100,25,linewidth=1,edgecolor="red",facecolor='none',zorder=2)
    if(count == 1):
        rect = patches.Rectangle((0,25),100,25,linewidth=1,edgecolor="red",facecolor='none',zorder=2)
    if(count == 2):
        rect = patches.Rectangle((0,25),100,25,linewidth=1,edgecolor="red",facecolor='none',zorder=2)
    if(count == 3):
        rect = patches.Rectangle((0,50),100,25,linewidth=1,edgecolor="red",facecolor='none',zorder=2)
    if(count == 4):
        rect = patches.Rectangle((0,50),100,25,linewidth=1,edgecolor="red",facecolor='none',zorder=2)
    if(count == 5):
        rect = patches.Rectangle((0,50),100,25,linewidth=1,edgecolor="red",facecolor='none',zorder=2)
    ax.add_patch(rect)



