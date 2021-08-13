
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

pitch = VerticalPitch(pitch_type='opta', pitch_color='#4D4D53', line_color='none',line_zorder=2, half = True)
fig, axs = pitch.draw(figsize=(17,21))

# fig, axs = pitch.grid(figheight=35, title_height=0.08, space=0.1, ncols = 3, nrows = 2,
#               # Turn off the endnote/title axis. I usually do this after
#               # I am happy with the chart layout and text placement
#               axis=False,
#               title_space=0, grid_height=0.85, endnote_height=0.02)


fig.set_facecolor('#4D4D53')

df2 = pd.read_csv("C:/Users/tomas/Documents/Benfica Data Driven Analysis/allEventsBenfica.csv")

df2 = df2[df2['type']=="{'value': 1, 'displayName': 'Pass'}"]
df2 = df2[df2['outcomeType']=="{'value': 1, 'displayName': 'Successful'}"]
df2 = df2[(df2['endX'] > 83.2) & (df2['endX'] < 100) & (df2['endY'] > 21) & (df2['endY'] < 79)]
df2 = df2[df2['teamId']==299]
df2['qualifiers'] = df2['qualifiers'].apply(ast.literal_eval)
df2['isRemovable'] = df2['qualifiers'].apply(searchQualifiers)
df2 = df2[df2['isRemovable']==False]

total = 497

df_right_half_space = df2[(df2['x'] > 50) & (df2['x'] < 83) & (df2['y'] > 21) & (df2['y'] < 36.8)]
df_right_area_space = df2[(df2['x'] > 83) & (df2['x'] < 100) & (df2['y'] > 21) & (df2['y'] < 36.8)]
df_middle_space = df2[(df2['x'] > 50) & (df2['x'] < 83) & (df2['y'] > 36.8) & (df2['y'] < 63.2)]
df_left_half_space = df2[(df2['x'] > 50) & (df2['x'] < 83) & (df2['y'] > 63.2) & (df2['y'] < 79)]
df_left_area_space = df2[(df2['x'] > 83) & (df2['x'] < 100) & (df2['y'] > 63.2) & (df2['y'] < 79)]
df_right_wing_back = df2[(df2['x'] > 50) & (df2['x'] < 83) & (df2['y'] > 0) & (df2['y'] < 21)]
df_right_corner = df2[(df2['x'] > 83) & (df2['x'] < 100) & (df2['y'] > 0) & (df2['y'] < 21)]
df_left_wing_back = df2[(df2['x'] > 50) & (df2['x'] < 83) & (df2['y'] > 79) & (df2['y'] < 100)]
df_left_corner = df2[(df2['x'] > 83) & (df2['x'] < 100) & (df2['y'] > 79) & (df2['y'] < 100)]

pearl_earring_cmap = LinearSegmentedColormap.from_list("brrgheehgtr4",
                                                       ['#504847','#ED2C0E'], N=100)

maxValue = df_right_half_space.shape[0]/total

# vhjfniw = pitch.scatter(df_right_corner.x,df_right_corner.y,color = "black",edgecolors= 'white',ax = axs, zorder = 3, marker = 'o')
# vhjfniw = pitch.scatter(df_left_corner.x,df_left_corner.y,color = "black",edgecolors= 'white',ax = axs, zorder = 3, marker = 'o')
# vhjfniw = pitch.scatter(df_right_half_space.x,df_right_half_space.y,color = "black",edgecolors= 'white',ax = axs, zorder = 3, marker = 'o')
# vhjfniw = pitch.scatter(df_left_half_space.x,df_left_half_space.y,color = "black",edgecolors= 'white',ax = axs, zorder = 3, marker = 'o')
#Right Wing Back
rect = patches.Rectangle((0.1,50),21,33,linewidth=2,edgecolor="none",facecolor=pearl_earring_cmap((df_right_wing_back.shape[0]/total)*0.8/maxValue),zorder=1)
axs.add_patch(rect)
#Left Wing Back
rect = patches.Rectangle((79.1,50),21,33,linewidth=2,edgecolor="none",facecolor=pearl_earring_cmap((df_left_wing_back.shape[0]/total)*0.8/maxValue),zorder=1)
axs.add_patch(rect)
#Right Half Space
rect = patches.Rectangle((21,50),15.8,33,linewidth=2,edgecolor="none",facecolor=pearl_earring_cmap((df_right_half_space.shape[0]/total)*0.8/maxValue),zorder=1)
axs.add_patch(rect)
#Left Half Space
rect = patches.Rectangle((63.2,50),16,33,linewidth=2,edgecolor="none",facecolor=pearl_earring_cmap((df_right_half_space.shape[0]/total)*0.8/maxValue),zorder=1)
axs.add_patch(rect)
#Right Space Inside Area
rect = patches.Rectangle((21,83),15.8,17,linewidth=2,edgecolor="none",facecolor=pearl_earring_cmap((df_right_area_space.shape[0]/total)*0.8/maxValue),zorder=1)
axs.add_patch(rect)
#Left Space Inside Area
rect = patches.Rectangle((63.2,83),16,17,linewidth=2,edgecolor="none",facecolor=pearl_earring_cmap((df_left_area_space.shape[0]/total)*0.8/maxValue),zorder=2)
axs.add_patch(rect)
#Left Corner
rect = patches.Rectangle((79.1,83),21,17,linewidth=2,edgecolor="none",facecolor=pearl_earring_cmap((df_left_corner.shape[0]/total)*0.8/maxValue),zorder=1)
axs.add_patch(rect)
#Right Corner
rect = patches.Rectangle((0,83),21,17,linewidth=2,edgecolor="none",facecolor=pearl_earring_cmap((df_right_corner.shape[0]/total)*0.8/maxValue),zorder=1)
axs.add_patch(rect)
#Middle Half Space
rect = patches.Rectangle((36.8,50),26.4,33,linewidth=2,edgecolor="none",facecolor=pearl_earring_cmap((df_middle_space.shape[0]/total)*0.8/maxValue),zorder=1)
axs.add_patch(rect)

rect = patches.Rectangle((0,50),100,50,linewidth=2,edgecolor="#c7d5cc",facecolor='none',zorder=4,linestyle='dashed')
axs.add_patch(rect)

plt.plot([21,21], [50,100], '--', lw=2,zorder=2,color='#c7d5cc')
plt.plot([36.8,36.8], [50,100], '--', lw=2,zorder=2,color='#c7d5cc')
plt.plot([63.2,63.2], [50,100], '--', lw=2,zorder=2,color='#c7d5cc')
plt.plot([79.1,79.1], [50,100], '--', lw=2,zorder=2,color='#c7d5cc')
plt.plot([0,100], [83,83], '--', lw=2,zorder=2,color='#c7d5cc')
plt.plot([36.8,63.2], [94.2,94.2], '--', lw=2,zorder=2,color='#c7d5cc')
plt.plot([43,57], [100.1,100.1], '-', lw=2,zorder=2,color='#c7d5cc')

pitch.scatter(88.4,50,s=65,color='#c7d5cc',ax=axs)

bounds = [(df_right_wing_back.shape[0]/total)*0.8/maxValue,
          (df_left_wing_back.shape[0]/total)*0.8/maxValue,
          (df_left_corner.shape[0]/total)*0.8/maxValue,
          (df_right_area_space.shape[0]/total)*0.8/maxValue,
          (df_right_corner.shape[0]/total)*0.8/maxValue,
          (df_left_half_space.shape[0]/total)*0.8/maxValue,
          (df_right_half_space.shape[0]/total)*0.8/maxValue]

norm = mpl.colors.BoundaryNorm(bounds, pearl_earring_cmap.N, extend='both')
cax = fig.add_axes([axs.get_position().x1-0.65,axs.get_position().y0-0.07,0.5,0.02])    
cbar = plt.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=pearl_earring_cmap),
              cax=cax, orientation='horizontal')
cbar.set_label('Passes Into The Box Per Zone', color="white",fontsize=28,fontproperties=fm_scada.prop)
cbar.outline.set_edgecolor('#c7d5cc')
cbar.ax.set_xticklabels(["0","37","44","53","58","62","68"])
plt.setp(plt.getp(cbar.ax.axes, 'xticklabels'), color="white",fontproperties=fm_scada.prop,fontsize = 18)

# bin_statistic = pitch.bin_statistic(df2.x, df2.y, statistic='count', bins=(6, 5), normalize=True)
# pitch.heatmap(bin_statistic, ax=axs, cmap=pearl_earring_cmap, edgecolor='#f9f9f9',zorder = 1)
