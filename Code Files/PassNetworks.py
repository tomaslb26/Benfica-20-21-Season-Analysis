import glob, os
import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.colors import to_rgba
from mplsoccer import Pitch, VerticalPitch, FontManager
from highlight_text import ax_text
from mplsoccer.statsbomb import read_event, EVENT_SLUG

# a fontmanager object for using a google font
fm_scada = FontManager(('https://github.com/googlefonts/scada/blob/main/fonts/ttf/'
                        'Scada-Regular.ttf?raw=true'))

fileList = []

os.chdir("C:/Users/tomas/Documents/Benfica Data Driven Analysis/Game Data/2nd Half")
for file in glob.glob("*.txt"):
   fileList += [file]
   
#savePlot(fileList)

# def savePlot(fileInput):
pitch = Pitch(pitch_type='opta', pitch_color='#4D4D53', line_color='#c7d5cc')
fig, axs = pitch.grid(figheight=25, title_height=0.08, endnote_space=0, ncols = 5, nrows = 4,
              # Turn off the endnote/title axis. I usually do this after
              # I am happy with the chart layout and text placement
              axis=False,
              title_space=0, grid_height=0.82, endnote_height=0.05)
fig.set_facecolor('#4D4D53')

axs['title'].text(0, 0.8, "Benfica Pass Network Second Half of the Season", fontsize=40,
                  fontproperties=fm_scada.prop, va='top', ha='left', color = "white")
axs['title'].text(0, 0.5, "Liga Nos 20/21", fontsize=30,
                  fontproperties=fm_scada.prop, va='top', ha='left', color = "red")

for count, ax in enumerate(axs['pitch'].flat):
    if(count >= 17):
        ax.remove()
        continue
    #print(fileList[count])
    file = open(fileList[count],"r",encoding="utf8")
    data= file.read()
    file.close()
    
    matchdata = json.loads(data) 
    
    x = pd.DataFrame.from_dict(matchdata["events"])
    home = pd.DataFrame.from_dict(matchdata["home"],orient='index')
    away = pd.DataFrame.from_dict(matchdata["away"],orient='index')
    
    if(home[0]["teamId"] == 299):
        players_dict = home[0]["players"]
        title = away[0]['name'] + " (H)"
    
    if(away[0]["teamId"] == 299):
        players_dict = away[0]["players"]
        title = home[0]['name'] + " (A)"
    
    players = pd.DataFrame.from_dict(players_dict)
    players_numbers = players[['playerId','shirtNo']].copy()
    
    
    df = x[['id','eventId','minute','second','teamId','x','y','type','outcomeType','playerId','endX','endY']].copy()
    
    
    
    df = df[df['teamId'] == 299]
    
    df = df.join(players_numbers.set_index('playerId'), on = 'playerId')
    df['passer'] = df['playerId']
    df['recipient'] = df['playerId'].shift(-1)
    
    df.loc[df.type == {'value': 1, 'displayName': 'Pass'},'type'] = "Pass"
    df.loc[df.outcomeType == {'value': 1, 'displayName': 'Successful'},'outcomeType'] = "Successful"
    
    passes = df[df['type'] == "Pass"]
    successful = passes[passes['outcomeType'] == "Successful"]
    
    subs = df[df['type'] ==  {'value': 18, 'displayName': 'SubstitutionOff'}] 
    subs = subs['minute']
    firstSub = subs.min()
    
    if(firstSub < 20):
        secondSub = subs.loc[subs>firstSub].min()
        successful = successful[ successful['minute'] < secondSub]
        successful = successful[ successful['minute'] > firstSub]
    else:
        # successful = successful[ successful['minute'] < 66]
        successful = successful[ successful['minute'] < firstSub]
        
    
    pas = pd.to_numeric(successful['passer'],downcast='integer')
    rec = pd.to_numeric(successful['recipient'],downcast='integer')
    
    successful['passer'] = pas
    successful['recipient'] = rec
    
    average_locations = successful.groupby('passer').agg({'x':['mean'],'y':['mean','count']})
    average_locations.columns = ['x','y','count']
    
    pass_between = successful.groupby(['passer','recipient']).id.count().reset_index()
    pass_between.rename({'id':'pass_count'},axis = 'columns', inplace = True )
    
    pass_between = pass_between.merge(average_locations, left_on = 'passer', right_index = True)
    pass_between = pass_between.merge(average_locations, left_on = 'recipient', right_index = True,suffixes = ['','_end'])
    
    pass_between = pass_between.set_index('passer').join(players_numbers.set_index('playerId'))
    
    pass_iterate = pass_between.copy()
    pass_between = pass_between[pass_between['pass_count'] > 2]
    
    pass_iterate['shirtNo'] = pass_iterate['shirtNo'].apply(str)
    
    #Lines Design
    
    MAX_LINE_WIDTH = 14
    MAX_MARKER_SIZE = 1500
    pass_between['width'] = (pass_between.pass_count / pass_between.pass_count.max() *
                            MAX_LINE_WIDTH)
    average_locations['marker_size'] = (average_locations['count']
                                          / average_locations['count'].max() * MAX_MARKER_SIZE)
    
    
    
    MIN_TRANSPARENCY = 0.3
    color = np.array(to_rgba('white'))
    color = np.tile(color, (len(pass_between), 1))
    c_transparency = pass_between.pass_count / pass_between.pass_count.max()
    c_transparency = (c_transparency * (1 - MIN_TRANSPARENCY)) + MIN_TRANSPARENCY
    color[:, 3] = c_transparency


    arrows = pitch.lines(pass_between.x,pass_between.y,pass_between.x_end,pass_between.y_end,ax=ax,
                      color = color, lw = pass_between.width, zorder = 1)
    
    nodes = pitch.scatter(average_locations.x, average_locations.y, color = 'red', edgecolors = "white", linewidth = 2, s = average_locations.marker_size, ax = ax, alpha = 1)
    
    list_aux = []
    for index, row in pass_iterate.iterrows():
        pitch.annotate(row.shirtNo, xy=(row.x, row.y), c='white', va='center',
                        ha='center', size=16, weight='bold', ax=ax)
        
    ax_text(2, 5, title, ha='left', va='center', fontsize=25,
                fontproperties=fm_scada.prop, ax=ax, color = 'white')
    
    
# fileList = []

# os.chdir("C:/Users/tomas/Documents/Benfica Data Driven Analysis/Game Data/1st Half")
# for file in glob.glob("*.txt"):
#    fileList += [file]
   
# savePlot(fileList)
# saveTitle = "C:/Users/tomas/Documents/Benfica Data Driven Analysis/Game Data/" + title + ".png"

plt.savefig(dpi=plt.gcf().dpi,fname='C:/Users/tomas/Documents/Benfica Data Driven Analysis/passNetwork2ndHalf.png',bbox_inches='tight', pad_inches=0)
