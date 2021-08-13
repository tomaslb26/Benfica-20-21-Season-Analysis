import glob, os
import pandas as pd
import ast
import math
import json
from modulesSoccer import offensiveTransitionClass
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
import matplotlib as mpl
from matplotlib import rcParams
from matplotlib.colors import to_rgba
from mplsoccer import Pitch, VerticalPitch, FontManager
from highlight_text import ax_text
from mplsoccer.statsbomb import read_event, EVENT_SLUG
import matplotlib.patches as patches
from sklearn.cluster import KMeans

mpl.rcParams['figure.dpi'] = 166

fm_scada = FontManager(('https://github.com/googlefonts/scada/blob/main/fonts/ttf/'
                        'Scada-Regular.ttf?raw=true'))


df2 = pd.read_csv("C:/Users/tomas/Documents/Benfica Data Driven Analysis/allEventsBenfica.csv")
c2 = offensiveTransitionClass.offensiveTransitions(df2, 299)
dicte1 = c2.getPossessionRecoveries(flag = "df", actionColors = True)

new_df = dicte1[['nextType', 'nextX', 'nextY', 'nextEndX', 'nextEndY', 'nextPlayerId', 'nextTeamId',
                 'nextQualifiers', 'nextOutcome']].copy()

new_df = new_df[(new_df['nextX'] >= 55) & (new_df['nextX'] <= 85)]

X = np.array(new_df[['nextX','nextY','nextEndX','nextEndY']])
kmeans = KMeans(n_clusters = 3, random_state = 100)
kmeans.fit(X)
new_df['cluster'] = kmeans.predict(X)


pitch = VerticalPitch( pitch_color='#565051',line_color='white',pitch_type='opta')
fig, axs = pitch.draw(figsize=(17,21))

fig.set_facecolor('#565051')

cluster_0 = new_df[new_df['cluster']==0]
cluster_1 = new_df[new_df['cluster']==1]
cluster_2 = new_df[new_df['cluster']==2]
# cluster_3 = new_df[new_df['cluster']==3]
# cluster_4 = new_df[new_df['cluster']==4]

arrows = pitch.arrows(cluster_0.nextX,cluster_0.nextY,cluster_0.nextEndX,cluster_0.nextEndY,ax=axs,
                      color = "red", zorder = 4, width = 1.4,headwidth=10,headlength=10)
arrows = pitch.arrows(cluster_1.nextX,cluster_1.nextY,cluster_1.nextEndX,cluster_1.nextEndY,ax=axs,
                      color = "green", zorder = 4, width = 1.4,headwidth=10,headlength=10)
arrows = pitch.arrows(cluster_2.nextX,cluster_2.nextY,cluster_2.nextEndX,cluster_2.nextEndY,ax=axs,
                      color = "blue", zorder = 4, width = 1.4,headwidth=10,headlength=10)
# arrows = pitch.lines(cluster_3.nextX,cluster_3.nextY,cluster_3.nextEndX,cluster_3.nextEndY,ax=axs,
#                       color = "yellow", zorder = 4, lw = 1)
# arrows = pitch.lines(cluster_4.nextX,cluster_4.nextY,cluster_4.nextEndX,cluster_4.nextEndY,ax=axs,
#                       color = "purple", zorder = 4, lw = 1)

rect = patches.Rectangle((0,55),100,30,linewidth=3,edgecolor="red",facecolor='none')
axs.add_patch(rect)


# big = mlines.Line2D([], [], color='blue', marker='*', linestyle='None',
#                           markersize=23, label='Big Chance Created', markeredgecolor = "black")
# key = mlines.Line2D([], [], color='green', marker='X', linestyle='None',
#                           markersize=23, label='Key Pass', markeredgecolor = "black")
# progressive = mlines.Line2D([], [], color='yellow', marker='8', linestyle='None',
#                           markersize=23, label='Progressive Pass', markeredgecolor = "black")
# assist = mlines.Line2D([], [], color='red', marker='$A$', linestyle='None',
#                           markersize=21, label='Assist')

# legend = plt.legend(handles=[big,key,progressive,assist], loc="lower left", 
#             facecolor = '#565051', edgecolor = '#565051', labelcolor = 'white', 
#             fontsize = 20, handletextpad = 0.1, ncol = 4 )


# axs['pitch'].legend()

plt.text(50, 110, 'Clustering Passes After Successful Defensive Action', color='#dee6ea',
                  va='center', ha='center',
                  fontproperties=fm_scada.prop, fontsize=45)

plt.text(50, 105, 'Benfica 20/21', color='yellow',
                  va='center', ha='center',
                  fontproperties=fm_scada.prop, fontsize=35)

plt.text(50, 115, 'Pass After Transition Cluster', color='#565051',
                  va='center', ha='center',
                  fontproperties=fm_scada.prop, fontsize=45)

plt.text(20, -4, '@PositionIsKeyPT', color='white',
                  fontproperties=fm_scada.prop, fontsize=20)

#plt.tight_layout()

plt.savefig(dpi=166,fname='C:/Users/tomas/Documents/Benfica Data Driven Analysis/passesAfterTransition18192021.png')
        

