import pandas as pd
from modulesSoccer import offensiveTransitionClass
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import json
from mplsoccer import Pitch, VerticalPitch, FontManager
import matplotlib.patches as patches

def check(x):
    if(x['x'] == x['nextX'] and x['y'] == x['nextY']):
        return True
    else:
        return False

fm_scada = FontManager(('https://github.com/googlefonts/scada/blob/main/fonts/ttf/'
                        'Scada-Regular.ttf?raw=true'))


mpl.rcParams['figure.dpi'] = 166
#GET PLAYERS NAMES
file = open("C:/Users/tomas/Documents/Benfica Data Driven Analysis/Game Data/1st Half/Game 1.txt","r",encoding="utf8")
data= file.read()
file.close()
    
matchdata = json.loads(data) 
x = pd.DataFrame.from_dict(matchdata["events"])

away = pd.DataFrame.from_dict(matchdata["away"],orient='index')
players_dict = away[0]["players"]
players = pd.DataFrame.from_dict(players_dict)
players_numbers = players[['playerId','shirtNo','name']].copy()

df2 = pd.read_csv("C:/Users/tomas/Documents/Benfica Data Driven Analysis/allEventsBenfica.csv")
c1 = offensiveTransitionClass.offensiveTransitions(df2, 299)
new_df = c1.getPassesAfterTransitionDf()
weigl_df = new_df.loc[((new_df['teamId'] == 299) & (new_df['nextTeamId'] == 299) & (new_df['nextPlayerId'] == 142318) & (new_df['playerId'] == 142318))]
weigl_df['samePlace'] = weigl_df.apply(check,axis = 1)
pizzi_df = new_df.loc[((new_df['teamId'] == 299) & (new_df['nextTeamId'] == 299) & (new_df['nextPlayerId'] == 81928) & (new_df['playerId'] == 81928))]
pizzi_df['samePlace'] = pizzi_df.apply(check,axis = 1)
taarabt_df = new_df.loc[((new_df['teamId'] == 299) & (new_df['nextTeamId'] == 299) & (new_df['nextPlayerId'] == 24642) & (new_df['playerId'] == 24642))]
taarabt_df['samePlace'] = taarabt_df.apply(check,axis = 1)

pitch = VerticalPitch(pitch_type='opta', pitch_color='#4D4D53', line_color='#c7d5cc',pad_left=10,  # bring the left axis in 10 data units (reduce the size)
                      pad_right=10,  # bring the right axis in 10 data units (reduce the size)
                      pad_top=5,  # extend the top axis 10 data units
                      pad_bottom=5)

fig, axs = pitch.grid(figheight=30, title_height=0.08, space=0.1, ncols = 3, nrows = 3,
              # Turn off the endnote/title axis. I usually do this after
              # I am happy with the chart layout and text placement
              axis=False,
              title_space=0, grid_height=0.85, endnote_height=0.02,)
fig.set_facecolor('#4D4D53')

for count, ax in enumerate(axs['pitch'].flat):
    if(count == 0):
        temp_df = weigl_df.loc[(weigl_df['x'] < 33.3)]
        rect = patches.Rectangle((0,0),100,33.3,linewidth=1,edgecolor="red",facecolor='none')
    if(count == 1):
        temp_df = weigl_df.loc[(weigl_df['x'] >= 33.3) & (weigl_df['x'] < 66.6)]
        rect = patches.Rectangle((0,33.3),100,33.3,linewidth=1,edgecolor="red",facecolor='none')
    if(count == 2):
        temp_df = weigl_df.loc[(weigl_df['x'] >= 66.6)]
        rect = patches.Rectangle((0,66.6),100,33.3,linewidth=1,edgecolor="red",facecolor='none')
    if(count == 3):
        temp_df = pizzi_df.loc[(pizzi_df['x'] < 33.3)]
        rect = patches.Rectangle((0,0),100,33.3,linewidth=1,edgecolor="red",facecolor='none')
    if(count == 4):
        temp_df = pizzi_df.loc[(pizzi_df['x'] >= 33.3) & (pizzi_df['x'] < 66.6)]
        rect = patches.Rectangle((0,33.3),100,33.3,linewidth=1,edgecolor="red",facecolor='none')
    if(count == 5):
        temp_df = pizzi_df.loc[(pizzi_df['x'] >= 66.6)]
        rect = patches.Rectangle((0,66.6),100,33.3,linewidth=1,edgecolor="red",facecolor='none')
    if(count == 6):
        temp_df = taarabt_df.loc[(taarabt_df['x'] < 33.3)]
        rect = patches.Rectangle((0,0),100,33.3,linewidth=1,edgecolor="red",facecolor='none')
    if(count == 7):
        temp_df = taarabt_df.loc[(taarabt_df['x'] >= 33.3) & (taarabt_df['x'] < 66.6)]
        rect = patches.Rectangle((0,33.3),100,33.3,linewidth=1,edgecolor="red",facecolor='none')
    if(count == 8):
        temp_df = taarabt_df.loc[(taarabt_df['x'] >= 66.6)]
        rect = patches.Rectangle((0,66.6),100,33.3,linewidth=1,edgecolor="red",facecolor='none')
    ax.add_patch(rect)
    temp_df1 = temp_df.loc[temp_df['samePlace'] == True]
    temp_df2 = temp_df.loc[temp_df['samePlace'] == False]
    nodes = pitch.scatter(temp_df2.x, temp_df2.y, color = 'red', edgecolors = "white", linewidth = 1, ax = ax, alpha = 1, zorder = 1)
    nodes = pitch.scatter(temp_df2.nextX, temp_df2.nextY, color = 'green', edgecolors = "white", linewidth = 1, ax = ax, alpha = 1, zorder = 1)
    arrows = pitch.lines(temp_df2.x,temp_df2.y,temp_df2.nextX,temp_df2.nextY,ax=ax,
                      color = "black", zorder = 4, lw = 1)
    nodes = pitch.scatter(temp_df1.nextX, temp_df1.nextY, color = 'green', edgecolors = "black", linewidth = 1, ax = ax, alpha = 1)
    arrows = pitch.arrows(temp_df.nextX,temp_df.nextY,temp_df.nextEndX,temp_df.nextEndY,ax=ax,
                      color = "red" , edgecolor = "white", zorder = 1, width = 1.4,headwidth=10,headlength=10)
    
axs['title'].text(-0.7, 1, "How are Benfica midfielders failing to pass after winning the ball?", fontsize=70,fontproperties=fm_scada.prop,
                   color = "white")

axs['title'].text(-0.7, 0.6, "Benfica 20/21", fontsize=55,fontproperties=fm_scada.prop,
                   color = "black")

axs['title'].text(0.06, 0.1, "Defensive\n   Third", fontsize=45,fontproperties=fm_scada.prop,
                   color = "white")

axs['title'].text(0.45, 0.1, "Middle\n Third", fontsize=45,fontproperties=fm_scada.prop,
                   color = "white")

axs['title'].text(0.80, 0.1, "Opposition\n    Third", fontsize=45,fontproperties=fm_scada.prop,
                   color = "white")

axs['endnote'].text(-0.43, 0.5, '@PositionIsKeyPT', color='#c7d5cc',
                    va='center', ha='right', fontsize=45,
                    fontproperties=fm_scada.prop)

big = mlines.Line2D([], [], color='green', marker='o', linestyle='None',
                          markersize=27, label='Reception', markeredgecolor = "white")
key = mlines.Line2D([], [], color='red', marker='o', linestyle='None',
                          markersize=27, label='Pass Location', markeredgecolor = "white")
x1 = mlines.Line2D([], [], color='green', marker='o', linestyle='None',
                          markersize=27, label='Ball Recovery and Pass Location', markeredgecolor = "black")
legend = plt.legend(handles=[big,key,x1], loc="lower right", 
            facecolor = '#4D4D53', edgecolor = '#565051', labelcolor = 'white', 
            fontsize = 25, handletextpad = 0.1, ncol = 4 )


#plt.savefig(dpi=300,fname='C:/Users/tomas/Documents/Benfica Data Driven Analysis/weiglPizziTaarabt.png')

        