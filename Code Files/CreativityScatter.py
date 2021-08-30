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
#import seaborn as sns

fm_scada = FontManager(('https://github.com/googlefonts/scada/blob/main/fonts/ttf/'
                        'Scada-Regular.ttf?raw=true'))

def clean(x):
    return x['displayName']

def cleanQualifiers(x):
    newList = []
    for y in x:
        newList += [y['type']['displayName']]
    return newList

def searchQualifiers(x):
    for dicte in x:
        if(dicte == "BigChanceCreated"):
            return True
    return False     

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

def getProgressivePassesDf(df1):
    df1['x'] = df1['x']*1.2
    df1['y'] = df1['y']*0.8
    df1['endX'] = df1['endX']*1.2
    df1['endY'] = df1['endY']*0.8
    df1['progressive'] = df1.apply(lambda row: isProgressivePass(row['x'],row['y'],row['endX'],row['endY']), axis=1)
    df1 = df1[df1['progressive']==True]
    return df1


mpl.rcParams['figure.dpi'] = 300

df2 = pd.read_csv("C:/Users/tomas/Benfica-20-21-Season-Analysis/Data/allTeamsCSV/allEventsBenfica.csv")

df2['type'] = df2['type'].apply(ast.literal_eval)
df2['type'] = df2['type'].apply(clean)
df2['outcomeType'] = df2['outcomeType'].apply(ast.literal_eval)
df2['outcomeType'] = df2['outcomeType'].apply(clean)
df2['qualifiers'] = df2['qualifiers'].apply(ast.literal_eval)
df2['qualifiers'] = df2['qualifiers'].apply(cleanQualifiers)

df_progressive = df2[(df2['type'] == 'Pass') & (df2['outcomeType'] == 'Successful') & (df2['teamId']==299)]

df_progressive = getProgressivePassesDf(df_progressive)

df_passes_box = df2[(df2['endX'] > 83.2) & (df2['endX'] < 100) & (df2['endY'] > 21) & (df2['endY'] < 79) &
                    (df2['type'] == 'Pass') & (df2['outcomeType'] == 'Successful') & (df2['teamId']==299)]

players = {
               'Nicolás Otamendi': [75691,2430,9.3],
               'Jan Vertonghen': [21778,2405,9.3],
               'Gilberto': [119542,1487,11.5],
               'Gabriel Pires': [120103,1028,9.3],
               'Everton': [146760,1977,11.2],
               'Julian Weigl': [142318,2035,7.1],
               'Adel Taarabt': [24642,1645,11.2],
               'Pizzi': [81928,1854,10.4],
               'Diogo Gonçalves': [343029,1179,9.8],
               'Alejandro Grimaldo': [107252,2467,14],
               'Haris Seferovic': [74016,2263,9.0],
               'Darwin Núñez': [400828,1790,9.7],
               'Rafa': [135127,2194,14.1],
               'Lucas Verissimo': [300640,1137,10.1],
               'Gian-Luca Waldschmidt': [148484,1398,7.9]
               }

df2['BigChance'] = df2['qualifiers'].apply(searchQualifiers)
df2 = df2[(df2['BigChance'] == True) & (df2['teamId'] == 299)]

for key in players:
    df_big_chance = df2[df2['playerId'] == players[key][0]]
    players[key] += [df_big_chance.shape[0]*90/players[key][1]]
    
    df_pass_box = df_passes_box[df_passes_box['playerId'] == players[key][0]]
    players[key] += [df_pass_box.shape[0]*90/players[key][1]]
    
    df_progressive_pass = df_progressive[df_progressive['playerId'] == players[key][0]]
    players[key] += [df_progressive_pass.shape[0]*90/players[key][1]]
    


df = pd.DataFrame.from_dict(players,orient='index')
df = df.reset_index()
df.columns = ['playerName','playerId', 'minutesPlayed','PossessionLostPer90','BigChancesCreatedPer90','PassesIntoTheBoxPer90','ProgressivePassesPer90']

def label_point(x,y,val,ax):
    positions_list = []
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for i, point in a.iterrows():
        if(point['val'] == "Haris Seferovic"):
            ax.text(point['x']-0.9, point['y']-0.21, str(point['val']), fontsize = '5', rotation = 1, weight = 'bold', color = 'white',fontproperties=fm_scada.prop)
        elif(point['val'] == "Alejandro Grimaldo"):
            ax.text(point['x']-0.6, point['y']-0.26, "Grimaldo", fontsize = '5', rotation = 1, weight = 'bold', color = 'white',fontproperties=fm_scada.prop)
        elif(point['val'] == "Pizzi"):
            ax.text(point['x']-0.01, point['y']-0.35, str(point['val']), fontsize = '5', rotation = 1, weight = 'bold', color = 'white',fontproperties=fm_scada.prop)
        elif(point['val'] == "Jan Vertonghen"):
            ax.text(point['x']+0.01, point['y']-0.35, "Vertonghen", fontsize = '5', rotation = 1, weight = 'bold', color = 'white',fontproperties=fm_scada.prop)
        elif(point['val'] == "Nicolás Otamendi"):
            ax.text(point['x']-0.1, point['y']-0.4, "Otamendi", fontsize = '5', rotation = 1, weight = 'bold', color = 'white',fontproperties=fm_scada.prop)
        elif(point['val'] == "Lucas Verissimo"):
            ax.text(point['x']-0.03, point['y']+0.35, "Lucas V.", fontsize = '5', rotation = 1, weight = 'bold', color = 'white',fontproperties=fm_scada.prop)
        elif(point['val'] == "Julian Weigl"):
            ax.text(point['x']-0.02, point['y']+0.3, "Weigl", fontsize = '5', rotation = 1, weight = 'bold', color = 'white',fontproperties=fm_scada.prop)
        elif(point['val'] == "Gian-Luca Waldschmidt"):
            ax.text(point['x'] -0.7, point['y']+0.2, "Waldschmidt", fontsize = '5', rotation = 1, weight = 'bold', color = 'white',fontproperties=fm_scada.prop)
        elif(point['val'] == "Adel Taarabt"):
            ax.text(point['x']-0.1, point['y']-0.4, "Taarabt", fontsize = '5', rotation = 1, weight = 'bold', color = 'white',fontproperties=fm_scada.prop)
        elif(point['val'] == "Gabriel Pires"):
            ax.text(point['x']+0.1, point['y']+0.15, "Gabriel", fontsize = '5', rotation = 1, weight = 'bold', color = 'white',fontproperties=fm_scada.prop)
        elif(point['val'] == "Gilberto"):
            ax.text(point['x']-0.03, point['y']+0.25, "Gilberto", fontsize = '5', rotation = 1, weight = 'bold', color = 'white',fontproperties=fm_scada.prop)
        elif(point['val'] == "Diogo Gonçalves"):
            ax.text(point['x']-0.3, point['y']-0.4, "Diogo G.", fontsize = '5', rotation = 1, weight = 'bold', color = 'white',fontproperties=fm_scada.prop)
        else:
            ax.text(point['x']-0.02, point['y']+0.25, str(point['val']), fontsize = '5', rotation = 1, weight = 'bold', color = 'white',fontproperties=fm_scada.prop,zorder=3)


# fig = plt.figure()
# fig.patch.set_facecolor('#4D4D53')

# ax = plt.gca()
# ax.set_facecolor('#4D4D53')
# plt.grid(zorder = 1)
# plt.rc('grid', linestyle="--", color='white')

# plt.scatter(df.BigChancesCreatedPer90,df.PassesIntoTheBoxPer90,color="red",zorder = 2)
# mpl.rcParams['axes.titlepad'] = 20
# xlabel = plt.xlabel("Big Chances Created Per 90",weight = 'bold',fontproperties=fm_scada.prop)
# ylabel = plt.ylabel("Passes Into The Box Per 90",weight = 'bold',fontproperties=fm_scada.prop)
# label_point(df['BigChancesCreatedPer90'], df['PassesIntoTheBoxPer90'], df['playerName'], plt.gca())
# ax.spines['bottom'].set_color('red')
# ax.spines['top'].set_color('red')
# ax.spines['left'].set_color('red')
# ax.spines['right'].set_color('red')
# xlabel.set_color("white")
# ylabel.set_color("white")
# ax.tick_params(axis='x', colors='none')
# ax.tick_params(axis='y', colors='none')
# [i.set_color("white") for i in plt.gca().get_xticklabels()]
# [i.set_color("white") for i in plt.gca().get_yticklabels()]
# [i.set_font_properties(fm_scada.prop) for i in plt.gca().get_xticklabels()]
# [i.set_font_properties(fm_scada.prop) for i in plt.gca().get_yticklabels()]

# plt.plot(0,0,zorder=2,color='none')

# fig.savefig(dpi=plt.gcf().dpi,fname="C:/Users/tomas/Benfica-20-21-Season-Analysis/Viz/ChanceCreationScatter.png")


fig = plt.figure()
fig.patch.set_facecolor('#4D4D53')

ax = plt.gca()
ax.set_facecolor('#4D4D53')
plt.grid(zorder = 1)
plt.rc('grid', linestyle="--", color='white')

plt.scatter(df.PossessionLostPer90,df.ProgressivePassesPer90,color="red",zorder = 2)
mpl.rcParams['axes.titlepad'] = 20
xlabel = plt.xlabel("Possession Lost Per 90",weight = 'bold',fontproperties=fm_scada.prop)
ylabel = plt.ylabel("Progressive Passes Per 90",weight = 'bold',fontproperties=fm_scada.prop)
label_point(df['PossessionLostPer90'], df['ProgressivePassesPer90'], df['playerName'], plt.gca())
ax.spines['bottom'].set_color('red')
ax.spines['top'].set_color('red')
ax.spines['left'].set_color('red')
ax.spines['right'].set_color('red')
xlabel.set_color("white")
ylabel.set_color("white")
ax.tick_params(axis='x', colors='none')
ax.tick_params(axis='y', colors='none')
[i.set_color("white") for i in plt.gca().get_xticklabels()]
[i.set_color("white") for i in plt.gca().get_yticklabels()]
[i.set_font_properties(fm_scada.prop) for i in plt.gca().get_xticklabels()]
[i.set_font_properties(fm_scada.prop) for i in plt.gca().get_yticklabels()]

fig.savefig(dpi=plt.gcf().dpi,fname="C:/Users/tomas/Benfica-20-21-Season-Analysis/Viz/ProgressionAndSecurityScatter.png")




