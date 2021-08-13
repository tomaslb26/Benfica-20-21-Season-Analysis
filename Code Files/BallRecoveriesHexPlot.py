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

pitch = VerticalPitch( line_zorder=2, pitch_color='#565051',line_color='white',pitch_type='opta')
fig, axs = pitch.grid(ncols = 2, nrows = 1,
              figheight=30, endnote_height=0.03, endnote_space=0,axis=False,title_height=0.09, grid_height=0.84)

fig.set_facecolor('#565051')

mapaCores = LinearSegmentedColormap.from_list("Flamingo - 100 colors",
                                                  ['#e3aca7', '#c03a1d'], N=100)

count = 0

allBallRecoveries2021 = pd.DataFrame()
allBallRecoveries1819 = pd.DataFrame()
   
df2 = pd.read_csv("C:/Users/tomas/Documents/Benfica Data Driven Analysis/allEventsBenfica.csv")
c1 = offensiveTransitionClass.offensiveTransitions(df2, 299)
dicte = c1.getPossessionRecoveries("df")
columns1 = ['type','x','y']
df1 = pd.DataFrame(dicte,columns = columns1)
allBallRecoveries2021 = pd.concat([allBallRecoveries2021,df1])
    

count = 0

df3 = pd.read_csv("C:/Users/tomas/Documents/Benfica Data Driven Analysis/allEventsBenfica1819.csv")
c1 = offensiveTransitionClass.offensiveTransitions(df3, 299)
dicte1 = c1.getPossessionRecoveries("df")
columns1 = ['type','x','y']
df10 = pd.DataFrame(dicte1,columns = columns1)
allBallRecoveries1819 = pd.concat([allBallRecoveries1819,df10])
    
for count, ax in enumerate(axs['pitch'].flat):
    if(count == 0):
        hexmap = pitch.hexbin(allBallRecoveries1819.x, allBallRecoveries1819.y, ax=ax, edgecolors='black',
                              gridsize=(10,10), cmap="Reds", linewidth = 1.5)
        
    else:
        hexmap = pitch.hexbin(allBallRecoveries2021.x, allBallRecoveries2021.y, ax=ax, edgecolors='black',
                              gridsize=(10,10), cmap='Reds', linewidth = 1.5)
        
        
cax = fig.add_axes([ax.get_position().x1+0.01,ax.get_position().y0+0.025,0.03,ax.get_position().height-0.05])        
cbar = plt.colorbar(hexmap,cax=cax)
cbar.outline.set_edgecolor('black')
cbar.ax.yaxis.set_tick_params(color='black', width = 30, labelcolor = 'white')
for label in cbar.ax.get_yticklabels():
    label.set_fontsize(40)
    coords = label.get_position()
    label.set_position([coords[0]+0.2,coords[1]+0.2])
    
    
axs['title'].text(0.35, 0.5, "Ball Recoveries Hex Plot", fontsize=70,fontproperties=fm_scada.prop,
                   color = "white")

axs['title'].text(0.16, 0, "Benfica 18/19", fontsize=55,fontproperties=fm_scada.prop,
                   color = "#EDE20E")

axs['title'].text(0.7, 0, "Benfica 20/21", fontsize=55,fontproperties=fm_scada.prop,
                   color = "#EDE20E")

axs['endnote'].text(1.08, 0.5, '@PositionIsKeyPT', color='#c7d5cc',
                    va='center', ha='right', fontsize=40,
                    fontproperties=fm_scada.prop)


plt.tight_layout()
plt.savefig(dpi=166,fname='C:/Users/tomas/Documents/Benfica Data Driven Analysis/ballRecoveries.png',bbox_inches='tight', pad_inches=0)
        
    
    

