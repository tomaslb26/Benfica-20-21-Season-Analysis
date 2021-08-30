# -*- coding: utf-8 -*-
"""
Created on Sun Aug  8 00:33:16 2021

@author: tomas
"""

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
import socceraction.spadl.config as spadlcfg
from socceraction.spadl import opta as opta
from socceraction.spadl.base import SPADLSchema
from socceraction.spadl.opta import (
    OptaCompetitionSchema,
    OptaEventSchema,
    OptaGameSchema,
    OptaPlayerSchema,
    OptaTeamSchema,
)
import socceraction.vaep.features as fs
import json

def searchQualifiers(x):
    listActions = [{'type': {'value': 6, 'displayName': 'CornerTaken'}},
                                        {'type': {'value': 107, 'displayName': 'ThrowIn'}},
                                        {'type': {'value': 5, 'displayName': 'FreekickTaken'}}]
    for dicte in x:
        for dict_action in listActions:
            if(dicte == dict_action):
                return True
    return False

actiontypes = [
    'pass',
    'cross',
    'throw_in',
    'freekick_crossed',
    'freekick_short',
    'corner_crossed',
    'corner_short',
    'take_on',
    'foul',
    'tackle',
    'interception',
    'shot',
    'shot_penalty',
    'shot_freekick',
    'keeper_save',
    'keeper_claim',
    'keeper_punch',
    'keeper_pick_up',
    'clearance',
    'bad_touch',
    'non_action',
    'dribble',
    'goalkick',
]

teamDict = {'Benfica': 299, 'Famalicao': 935, 'Moreirense' : 108, 'Farense': 263,
            'Rio Ave': 121, 'BelemSAD': 292, 'Boavista': 122, 'Braga': 288,
            'Marítimo': 264, 'Paços': 786, 'Vitoria': 107, 'Gil Vicente': 290,
            'Porto': 297, 'Portimonense': 1463, 'Santa Clara': 251, 'Tondela': 8071,
            'Nacional': 936, 'Sporting': 296}

def getTeamId(dir,id):
    data_dir = dir + "/2-2021-" + str(id) + ".json"
    with open(data_dir) as file:
        data = json.load(file)
        dict_e = data['away']

        return dict_e['teamId']
    
def isProgressive(x,y,endX,endY):
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

def convertXY(df):
    # df['start_x'] = 105-df['start_x']
    df['start_y'] = 68-df['start_y']
    # df['end_x'] = 105-df['end_x']
    df['end_y'] = 68-df['end_y']
    df['start_x'] = (df['start_x']/105)*120
    df['end_x'] = (df['end_x']/105)*120
    df['start_y'] = (df['start_y']/68)*80
    df['end_y'] = (df['end_y']/68)*80
    return df

fm_scada = FontManager(('https://github.com/googlefonts/scada/blob/main/fonts/ttf/'
                        'Scada-Regular.ttf?raw=true'))

mpl.rcParams['figure.dpi'] = 166

pitch = VerticalPitch(pitch_type='statsbomb', pitch_color='#4D4D53', line_color='#c7d5cc',line_zorder=2)


fig, axs = pitch.grid(figheight=20, title_height=0, space=0.05, ncols = 3, nrows = 2,
              # Turn off the endnote/title axis. I usually do this after
              # I am happy with the chart layout and text placement
              axis=False,
              title_space=0, grid_height=0.85, endnote_height=0)


fig.set_facecolor('#4D4D53')

df2 = pd.read_csv("C:/Users/tomas/Documents/Benfica Data Driven Analysis/allEventsBenfica.csv")

df2 = df2[((df2['playerId']==135127) | (df2['playerId']==146760) | (df2['playerId']==148484))]
df2 = df2[(df2['type'] == "{'value': 1, 'displayName': 'Pass'}") & (df2['outcomeType']=="{'value': 1, 'displayName': 'Successful'}")]

df2['x'] = df2['x']*1.2
df2['y'] = df2['y']*0.8
df2['endX'] = df2['endX']*1.2
df2['endY'] = df2['endY']*0.8
df2['y'] = 80 - df2['y']
df2['endY'] = 80 - df2['endY']
df2['qualifiers'] = df2['qualifiers'].apply(ast.literal_eval)
df2['isRemovable'] = df2['qualifiers'].apply(searchQualifiers)
df2 = df2[df2['isRemovable']==False]

df2['progressive'] = df2.apply(lambda row: isProgressive(row['x'],row['y'],row['endX'],row['endY']), axis=1)

df2 = df2[df2['progressive']==True]

folderList = ["C:/Users/tomas/Documents/Benfica Data Driven Analysis/Game Data/Teams/Benfica"]

df = pd.DataFrame(actiontypes,columns=['type_name'])
df['action_id'] = df.index 
allDribblesAndPasses = pd.DataFrame()
total = 0

for root_dir in folderList:
    teamName = root_dir.split("C:/Users/tomas/Documents/Benfica Data Driven Analysis/Game Data/Teams/")
    team_id = teamDict[teamName[1]]
    for gameId in range(1,35):
        home_id = getTeamId(root_dir, gameId)
        loader = opta.OptaLoader(
        root=root_dir, 
        parser='whoscored',
        feeds={'whoscored': "{competition_id}-{season_id}-{game_id}.json"})
        events = loader.events(game_id = gameId)
        events_spadl = opta.convert_to_actions(events, home_id)
        events_spadl = events_spadl.join(df.set_index('action_id'), on = 'type_id')
        dribbles = events_spadl[(events_spadl['type_name']=='dribble') | ((events_spadl['type_name']=='pass') & (events_spadl['result_id'] == 1))]
        allDribblesAndPasses = pd.concat([allDribblesAndPasses,dribbles])
        
allDribbles = allDribblesAndPasses[allDribblesAndPasses['type_name']=='dribble']
allDribbles.to_csv("C:/Users/tomas/Benfica-20-21-Season-Analysis/Data/allDribbles.csv")
        
df_allthree = allDribblesAndPasses[(allDribblesAndPasses['player_id']==135127) | (allDribblesAndPasses['player_id']==146760) | (allDribblesAndPasses['player_id']==148484)]

df_allthree = convertXY(df_allthree)

df_allthree['isProgressive'] = df_allthree.apply(lambda row: isProgressive(row['start_x'],row['start_y'],row['end_x'],row['end_y']), axis=1)
df_allthree = df_allthree[df_allthree['isProgressive'] == True]

for count, ax in enumerate(axs['pitch'].flat):
    if(count == 0):
        arrows = pitch.lines(df2[(df2['playerId']==135127)].x,
                              df2[(df2['playerId']==135127)].y,
                              df2[(df2['playerId']==135127)].endX,
                              df2[(df2['playerId']==135127)].endY,ax=ax,
                      color = "#ED2C0E", zorder = 4, lw = 4, comet = True)
        
    if(count == 1):
        arrows = pitch.lines(df2[(df2['playerId']==146760)].x,
                              df2[(df2['playerId']==146760)].y,
                              df2[(df2['playerId']==146760)].endX,
                              df2[(df2['playerId']==146760)].endY,ax=ax,
                      color = "#ED2C0E", zorder = 4, lw = 4, comet = True)
        
    if(count == 2):
        arrows = pitch.lines(df2[(df2['playerId']==148484)].x,
                      df2[(df2['playerId']==148484)].y,
                      df2[(df2['playerId']==148484)].endX,
                      df2[(df2['playerId']==148484)].endY,ax=ax,
              color = "#ED2C0E", zorder = 4, lw = 4, comet = True)
    if(count == 3):
                arrows = pitch.arrows(df_allthree[(df_allthree['player_id']==135127) & (df_allthree['type_name'] == 'dribble')].start_x,
                             df_allthree[(df_allthree['player_id']==135127) & (df_allthree['type_name'] == 'dribble')].start_y,
                             df_allthree[(df_allthree['player_id']==135127) & (df_allthree['type_name'] == 'dribble')].end_x,
                             df_allthree[(df_allthree['player_id']==135127) & (df_allthree['type_name'] == 'dribble')].end_y,ax=ax,
                      color = "yellow", zorder = 1, width = 1.4,headwidth=10,headlength=10)
    if(count == 4):
                arrows = pitch.arrows(df_allthree[(df_allthree['player_id']==146760) & (df_allthree['type_name'] == 'dribble')].start_x,
                             df_allthree[(df_allthree['player_id']==146760) & (df_allthree['type_name'] == 'dribble')].start_y,
                             df_allthree[(df_allthree['player_id']==146760) & (df_allthree['type_name'] == 'dribble')].end_x,
                             df_allthree[(df_allthree['player_id']==146760) & (df_allthree['type_name'] == 'dribble')].end_y,ax=ax,
                      color = "yellow", zorder = 1, width = 1.4,headwidth=10,headlength=10)
    if(count == 5):
                arrows = pitch.arrows(df_allthree[(df_allthree['player_id']==148484) & (df_allthree['type_name'] == 'dribble')].start_x,
                             df_allthree[(df_allthree['player_id']==148484) & (df_allthree['type_name'] == 'dribble')].start_y,
                             df_allthree[(df_allthree['player_id']==148484) & (df_allthree['type_name'] == 'dribble')].end_x,
                             df_allthree[(df_allthree['player_id']==148484) & (df_allthree['type_name'] == 'dribble')].end_y,ax=ax,
                      color = "yellow", zorder = 1, width = 1.4,headwidth=10,headlength=10)