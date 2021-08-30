import glob, os
import pandas as pd
import json
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import matplotlib as mpl
from modulesSoccer import offensiveTransitionClass
import numpy as np
from matplotlib import rcParams
from matplotlib.colors import to_rgba
from mplsoccer import Pitch, VerticalPitch, FontManager
from highlight_text import ax_text
from mplsoccer.statsbomb import read_event, EVENT_SLUG


mpl.rcParams['figure.dpi'] = 166

fm_scada = FontManager(('https://github.com/googlefonts/scada/blob/main/fonts/ttf/'
                        'Scada-Regular.ttf?raw=true'))

fileList = []
fileList1819 = []

pitch = VerticalPitch( line_zorder=2, pitch_color='#4D4D53',line_color='white',pitch_type='opta')
fig,ax = pitch.draw(figsize=(17,21))

fig.set_facecolor('#4D4D53')

mapaCores = LinearSegmentedColormap.from_list("Flamingo - 100 colors",
                                                  ['#4D4D53', '#ED2C0E'], N=100)

count = 0

allBallRecoveries2021 = pd.DataFrame()
allBallRecoveries1819 = pd.DataFrame()
   
df2 = pd.read_csv("C:/Users/tomas/Documents/Benfica Data Driven Analysis/allEventsBenfica.csv")
c1 = offensiveTransitionClass.offensiveTransitions(df2, 299)
dicte = c1.getPossessionRecoveries("df",against=True)
columns1 = ['type','teamId','x','y']
df1 = pd.DataFrame(dicte,columns = columns1)
allBallRecoveries2021 = pd.concat([allBallRecoveries2021,df1])

allBallRecoveries2021['x'].loc[allBallRecoveries2021['teamId'] != 299] = 100 - allBallRecoveries2021['x']
allBallRecoveries2021['y'].loc[allBallRecoveries2021['teamId'] != 299] = 100 - allBallRecoveries2021['y']
      

hexmap = pitch.hexbin(allBallRecoveries2021.x, allBallRecoveries2021.y, ax=ax, edgecolors='black',
                      gridsize=(10,10), cmap=mapaCores, linewidth = 1.2)

cax = fig.add_axes([ax.get_position().x1+0.08,ax.get_position().y0-0.05,0.03,ax.get_position().height+0.1])        
cbar = plt.colorbar(hexmap,cax=cax)
cbar.outline.set_edgecolor('black')
cbar.ax.yaxis.set_tick_params(color='black', width = 30, labelcolor = 'white')
for label in cbar.ax.get_yticklabels():
    label.set_fontsize(40)
    coords = label.get_position()
    label.set_position([coords[0]+0.2,coords[1]+0.2])