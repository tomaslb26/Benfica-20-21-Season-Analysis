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

fm_scada = FontManager(('https://github.com/googlefonts/scada/blob/main/fonts/ttf/'
                        'Scada-Regular.ttf?raw=true'))

mpl.rcParams['figure.dpi'] = 166

def isProgressivePass(x,y,endX,endY):
    distanceInitial = np.sqrt(np.square(120 - x) + np.square(40 - y))
    distanceFinal = np.sqrt(np.square(120 - endX) + np.square(40 - endY))
    if(x <= 60 and endX <= 60):
        if(distanceInitial - distanceFinal > 30):
            return True
    elif(x <= 60 and endX > 60):
        if(distanceInitial - distanceFinal > 15):
            return True
    elif(x > 60 and endX > 60):
        if(distanceInitial - distanceFinal > 10):
            return True
    return False

pitch = VerticalPitch(pitch_type='statsbomb', pitch_color='#4D4D53', line_color='#c7d5cc',line_zorder=2)

fig, axs = pitch.grid(figheight=40, title_height=0.08, space=0.1, ncols = 3, nrows = 2,
              # Turn off the endnote/title axis. I usually do this after
              # I am happy with the chart layout and text placement
              axis=False,
              title_space=0, grid_height=0.85, endnote_height=0.02)

fig.set_facecolor('#4D4D53')

df2 = pd.read_csv("C:/Users/tomas/Documents/Benfica Data Driven Analysis/allEventsBenfica.csv")

df2 = df2[((df2['playerId']==142318) | (df2['playerId']==75691) | (df2['playerId']==21778))]
df2 = df2[(df2['type'] == "{'value': 1, 'displayName': 'Pass'}") & (df2['outcomeType']=="{'value': 1, 'displayName': 'Successful'}")]

df2['x'] = df2['x']*1.2
df2['y'] = df2['y']*0.8
df2['endX'] = df2['endX']*1.2
df2['endY'] = df2['endY']*0.8
df2['y'] = 80 - df2['y']
df2['endY'] = 80 - df2['endY']

df1 = df2.copy()
df1 = df1[df1['x']<60]

df1['beginning'] = np.sqrt(np.square(120-df1['x']) + np.square(40 - df1['y']))
df1['end'] = np.sqrt(np.square(120 - df1['endX']) + np.square(40 - df1['endY']))

df1['progressive'] = df1.apply(lambda row: row['end']/ row['beginning'] < 0.75, axis = 1)


#df1['progressive'] = df1.apply(lambda row: isProgressivePass(row['x'],row['y'],row['endX'],row['endY']), axis=1)

df1 = df1[df1['progressive']==True]

pearl_earring_cmap = LinearSegmentedColormap.from_list("Pearl Earring - 10 colors",
                                                       ['#4D4D53','#ED2C0E'], N=100)

for count, ax in enumerate(axs['pitch'].flat):
    if(count == 0):
        arrows = pitch.lines(df1[df1['playerId']==21778].x,df1[df1['playerId']==21778].y,
                             df1[df1['playerId']==21778].endX,df1[df1['playerId']==21778].endY,ax=ax,
                      color = "#ED2C0E", zorder = 4, lw = 5, comet = True)
    if(count == 1):
        arrows = pitch.lines(df1[df1['playerId']==142318].x,df1[df1['playerId']==142318].y,
                             df1[df1['playerId']==142318].endX,df1[df1['playerId']==142318].endY,ax=ax,
                      color = "#ED2C0E", zorder = 4, lw = 5, comet = True)
    if(count == 2):
        arrows = pitch.lines(df1[df1['playerId']==75691].x,df1[df1['playerId']==75691].y,
                             df1[df1['playerId']==75691].endX,df1[df1['playerId']==75691].endY,ax=ax,
                      color = "#ED2C0E", zorder = 4, lw = 5, comet = True)
    if(count == 3):
        kdeplot = pitch.kdeplot(df2[df2['playerId']==21778].x,df2[df2['playerId']==21778].y, ax=ax, cmap=pearl_earring_cmap, shade=True, levels=10,zorder = 1)
    if(count == 4):
        kdeplot = pitch.kdeplot(df2[df2['playerId']==142318].x,df2[df2['playerId']==142318].y, ax=ax, cmap=pearl_earring_cmap, shade=True, levels=10,zorder = 1)
    if(count == 5):
        kdeplot = pitch.kdeplot(df2[df2['playerId']==75691].x,df2[df2['playerId']==75691].y, ax=ax, cmap=pearl_earring_cmap, shade=True, levels=10,zorder = 1)
        
plt.savefig(dpi=166,fname='C:/Users/tomas/Documents/Benfica Data Driven Analysis/progressiveHeatMap.png')
        