import pandas as pd
import glob, os
from modulesSoccer import offensiveTransitionClass
from PIL import Image
import ast
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer import FontManager
import matplotlib as mpl

fm_scada = FontManager(('https://github.com/googlefonts/scada/blob/main/fonts/ttf/'
                        'Scada-Regular.ttf?raw=true'))
mpl.rcParams['figure.dpi'] = 300

def label_point(x,y,val,ax):
    positions_list = []
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for i, point in a.iterrows():
        if(point['val'] == "Farense" or point['val'] == "Paços de Ferreira" or point['val'] == "Nacional" or point['val'] == "Portimonense"):
            ax.text(point['x']-0.07, point['y']-0.14, str(point['val']), fontsize = '5', rotation = 1, weight = 'bold', color = 'white',fontproperties=fm_scada.prop)
        elif(point['val'] == "Portimonense"):
            ax.text(point['x']-0.13, point['y']+0.07, str(point['val']), fontsize = '5', rotation = 1, weight = 'bold', color = 'white',fontproperties=fm_scada.prop)
        else:
            ax.text(point['x']-0.07, point['y']+0.09, str(point['val']), fontsize = '5', rotation = 1, weight = 'bold', color = 'white',fontproperties=fm_scada.prop)
                
mpl.rcParams['font.family'] = 'sans-serif'              
mpl.rcParams['font.sans-serif'] = ['Oswald']
df = pd.read_csv("C:/Users/tomas/Documents/Benfica Data Driven Analysis/doneCalculations/ballRecoveriesDf.csv")
fig = plt.figure()
fig.patch.set_facecolor('#4D4D53')
ax = plt.gca()
ax.set_facecolor('#4D4D53')
plt.scatter(df.opponentHalf,df.ownHalf,color = df.markercolor, edgecolors = df.outline)
title = plt.title('Liga NOS 20/21:\n Where do teams get the ball back?', fontsize=15,weight = 'bold',fontproperties=fm_scada.prop)
title.set_color("white")
mpl.rcParams['axes.titlepad'] = 20
xlabel = plt.xlabel("Successful Defensive Actions \n Opponent Half per 90",weight = 'bold',fontproperties=fm_scada.prop)
ylabel = plt.ylabel("Successful Defensive Actions \n Own Half per 90",weight = 'bold',fontproperties=fm_scada.prop)
[i.set_color("white") for i in plt.gca().get_xticklabels()]
[i.set_color("white") for i in plt.gca().get_yticklabels()]
[i.set_font_properties(fm_scada.prop) for i in plt.gca().get_xticklabels()]
[i.set_font_properties(fm_scada.prop) for i in plt.gca().get_yticklabels()]
xlabel.set_color("white")
ylabel.set_color("white")
props = dict(boxstyle='square', facecolor='none', edgecolor = 'white')
plt.text(x = 7.1, y= 19 , s='Prefer to pressure\nthe opponent in their own half\nusing a higher pressure line', fontsize = 5
         ,color = "white",bbox = props,fontproperties=fm_scada.prop)
plt.text(x = 4.9, y= 20.9 , s="Prefer to invite\nopponent's pressure,\ndefending lower\non the pitch", fontsize = 5
         ,color = "white",bbox = props,fontproperties=fm_scada.prop)

ax.spines['bottom'].set_color('yellow')
ax.spines['top'].set_color('yellow')
ax.spines['left'].set_color('yellow')
ax.spines['right'].set_color('yellow')


label_point(df['opponentHalf'], df['ownHalf'], df['teamName'], plt.gca())
plt.tight_layout()
plt.show()
fig.savefig(dpi=plt.gcf().dpi,fname='C:/Users/tomas/Documents/Benfica Data Driven Analysis/scatterTransition.png')
