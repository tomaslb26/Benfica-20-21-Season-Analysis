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

def label_point(x,y,val,ax):
    positions_list = []
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for i, point in a.iterrows():
        if(point['val'] == "Haris Seferovic"):
            ax.text(point['x']-0.9, point['y']-0.21, str(point['val']), fontsize = '5', rotation = 1, weight = 'bold', color = 'white',fontproperties=fm_scada.prop)
        else:
            ax.text(point['x']-0.02, point['y']+0.25, str(point['val']), fontsize = '5', rotation = 1, weight = 'bold', color = 'white',fontproperties=fm_scada.prop,zorder=3)


fm_scada = FontManager(('https://github.com/googlefonts/scada/blob/main/fonts/ttf/'
                        'Scada-Regular.ttf?raw=true'))

mpl.rcParams['figure.dpi'] = 300
    
teamDict = {'Benfica': [299, 1.8529411764705883, 145.0],
            'Famalicao': [935, 2.0, 133.1],
            'Moreirense' : [108, 2.2941176470588234, 142.5],
            'Farense': [263, 1.7647058823529411, 147.6],
            'RioAve': [121, 2.323529411764706, 135.8],
            'Belenenses': [292, 1.7058823529411764, 146.9],
            'Boavista': [122, 1.6176470588235294, 130.0],
            'Braga': [288, 1.5, 138.5],
            'Maritimo': [264, 2.1176470588235294, 137.4],
            'Paços': [786, 1.411764705882353, 137.4],
            'Vitoria': [107, 2.0, 136.1],
            'GilVicente': [290, 2.088235294117647, 139.8],
            'Porto': [297, 1.4411764705882353, 142.9],
            'Portimonense': [1463, 1.7941176470588236, 149.7],
            'SantaClara': [251, 1.8235294117647058, 138.1],
            'Tondela': [8071, 1.7647058823529411, 141.8],
            'Nacional': [936, 2.5, 142.9],
            'Sporting': [296, 1.2058823529411764, 142.5]}


df = pd.DataFrame.from_dict(teamDict,orient='index')
df = df.reset_index()
df.columns = ["team_name","team_id","shots_allowed_per90","possession_lost_per90"]

fig = plt.figure()
fig.patch.set_facecolor('#4D4D53')

ax = plt.gca()
ax.set_facecolor('#4D4D53')
plt.grid(zorder = 1)
plt.rc('grid', linestyle="--", color='#E1C31D')

plt.scatter(df.shots_allowed_per90,df.possession_lost_per90,color="red",zorder = 2)
mpl.rcParams['axes.titlepad'] = 20
xlabel = plt.xlabel("Shots Allowed In Transition Per 90'",weight = 'bold',fontproperties=fm_scada.prop)
ylabel = plt.ylabel("Possession Lost Per 90'",weight = 'bold',fontproperties=fm_scada.prop)
#label_point(df['shots_allowed_per90'], df['possession_lost_per90'], df['team_name'], plt.gca())
ax.spines['bottom'].set_color('#E1C31D')
ax.spines['top'].set_color('#E1C31D')
ax.spines['left'].set_color('#E1C31D')
ax.spines['right'].set_color('#E1C31D')
xlabel.set_color("white")
ylabel.set_color("white")
ax.tick_params(axis='x', colors='none')
ax.tick_params(axis='y', colors='none')
[i.set_color("white") for i in plt.gca().get_xticklabels()]
[i.set_color("white") for i in plt.gca().get_yticklabels()]
[i.set_font_properties(fm_scada.prop) for i in plt.gca().get_xticklabels()]
[i.set_font_properties(fm_scada.prop) for i in plt.gca().get_yticklabels()]