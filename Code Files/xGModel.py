
# Import standard modules
import os
import sys

# Import Pandas library
import pandas as pd

# Import XGBoost classifier
from xgboost import XGBClassifier

# Import scikit-learn functions
from sklearn.metrics import average_precision_score
from sklearn.metrics import roc_auc_score

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

# Import scikit-plot functions
from scikitplot.metrics import plot_roc_curve
from scikitplot.metrics import plot_precision_recall_curve
import matplotlib.lines as mlines
from scikitplot.metrics import plot_calibration_curve

# Import SciPy function
from scipy.spatial import distance

import matplotlib.pyplot as plt

from mplsoccer import Pitch, VerticalPitch, FontManager
import matplotlib as mpl

fm_scada = FontManager(('https://github.com/googlefonts/scada/blob/main/fonts/ttf/'
                        'Scada-Regular.ttf?raw=true'))


mpl.rcParams['figure.dpi'] = 166

path_dataset = os.path.abspath(os.path.join(os.sep, os.getcwd(), os.pardir, 'data', 'scisports-shots.parquet'))
df_dataset = pd.read_parquet(path_dataset)

for action in ['action', 'action1', 'action2']:
    for side in ['start', 'end']:
        
        # Normalize the X location
        key_x = '{}_{}_x'.format(action, side)
        df_dataset[key_x] = df_dataset[key_x] / 105
               
        # Normalize the Y location
        key_y = '{}_{}_y'.format(action, side)
        df_dataset[key_y] = df_dataset[key_y] / 68
        
goal = (1, 0.5)

for action in ['action', 'action1', 'action2']:
    key_start_x = '{action}_start_x'.format(action=action)
    key_start_y = '{action}_start_y'.format(action=action)
    key_start_distance = '{action}_start_distance'.format(action=action)

    df_dataset[key_start_distance] = df_dataset.apply(lambda s: distance.euclidean((s[key_start_x], s[key_start_y]), goal), axis=1)
    
# Features
columns_features = ['action_start_x', 'action_start_y', 'action_body_part_id', 'action_start_distance', 'action1_start_distance', 'action2_start_distance']

# Label: 1 if a goal, 0 otherwise
column_target = 'action_result'

X = df_dataset[columns_features]
y = df_dataset[column_target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01)

classifier = XGBClassifier(objective='binary:logistic', max_depth=5, n_estimators=100)
classifier.fit(X_train, y_train)

y_pred = classifier.predict_proba(X_test)

pitch = VerticalPitch(pitch_type='opta',half=True,line_color="white",pitch_color='#4D4D53')  # showing axis labels is optional
fig, ax = pitch.draw()
fig.set_facecolor('#4D4D53')

pre_shots_transition = pd.read_csv('C:/Users/tomas/Documents/Benfica Data Driven Analysis/Game Data/shots_transition_spadl.csv')


inverted_shots_transition = pre_shots_transition[pre_shots_transition['start_x'] < 50]
final_shots_transition = pre_shots_transition[pre_shots_transition['start_x'] > 50]

inverted_shots_transition['start_x'] = 105-inverted_shots_transition['start_x']
inverted_shots_transition['start_y'] = 68-inverted_shots_transition['start_y']
inverted_shots_transition['action_1_x'] = 105-inverted_shots_transition['action_1_x']
inverted_shots_transition['action_1_y'] = 68-inverted_shots_transition['action_1_y']
inverted_shots_transition['action_2_x'] = 105-inverted_shots_transition['action_2_x']
inverted_shots_transition['action_2_y'] = 68-inverted_shots_transition['action_2_y']

shots_transition = pd.concat([inverted_shots_transition,final_shots_transition])
    
shots_transition['start_x'] = shots_transition['start_x']/105
shots_transition['start_y'] = shots_transition['start_y']/68
shots_transition['action_1_x'] = shots_transition['action_1_x']/105
shots_transition['action_1_y'] = shots_transition['action_1_y']/68
shots_transition['action_2_x'] = shots_transition['action_2_x']/105
shots_transition['action_2_y'] = shots_transition['action_2_y']/68

shots_transition['action_start_distance'] = shots_transition.apply(lambda s: distance.euclidean((s['start_x'], s['start_y']), goal), axis=1)
shots_transition['action1_start_distance'] = shots_transition.apply(lambda s: distance.euclidean((s['action_1_x'], s['action_1_y']), goal), axis=1)
shots_transition['action2_start_distance'] = shots_transition.apply(lambda s: distance.euclidean((s['action_2_x'], s['action_2_y']), goal), axis=1)

new_columns_features = ['start_x', 'start_y', 'bodypart_id', 'action_start_distance', 'action1_start_distance', 'action2_start_distance','result_name']


shots_transition = shots_transition[new_columns_features]

shots_transition = shots_transition.reset_index()

shots_transition = shots_transition.rename(columns={'start_x': 'action_start_x', 'start_y': 'action_start_y', 'bodypart_id': 'action_body_part_id'})

new_shots_transition = shots_transition[columns_features]

xg_values = classifier.predict_proba(new_shots_transition)

xG_list = []
for i in range(len(xg_values)):
    xG_list += [xg_values[i][1]]

xg_series = pd.Series(xG_list)

new_df = shots_transition.merge(xg_series.rename('xG_Value'), left_index=True, right_index=True)

new_df['action_start_x'] = new_df['action_start_x']*100
new_df['action_start_y'] = new_df['action_start_y']*100


new_df['marker_size'] = (new_df['xG_Value']
                                          / 1 * 300)

# new_df['color'] = 'red'
# new_df['color'].loc[new_df['result_name']=='success'] = 'green'
green_df= new_df.loc[new_df['result_name']=='success']

pass_nodes = pitch.scatter(new_df.action_start_x, new_df.action_start_y,
                            s=new_df.marker_size,
                            color='red', edgecolors='black', linewidth=0.5, alpha=1, ax=ax)

pass_nodes = pitch.scatter(green_df.action_start_x, green_df.action_start_y,
                            s=green_df.marker_size,
                            color='green', edgecolors='black', linewidth=0.5, alpha=1, ax=ax)

# big = mlines.Line2D([], [], color='red', marker='o', linestyle='None',
#                           markersize=2, label='', markeredgecolor = "black")
# big1 = mlines.Line2D([], [], color='red', marker='o', linestyle='None',
#                           markersize=7, label='', markeredgecolor = "black")
# key = mlines.Line2D([], [], color='red', marker='o', linestyle='None',
#                           markersize=12, label='', markeredgecolor = "black")
# progressive = mlines.Line2D([], [], color='red', marker='o', linestyle='None',
#                           markersize=17, label='', markeredgecolor = "black")

# legend = plt.legend(handles=[big,big1,key,progressive], loc=(0.1,-0.1), 
#             facecolor = '#4D4D53', edgecolor = '#565051', labelcolor = 'white', 
#             fontsize = 2, columnspacing = 6, ncol = 4 )

mSize = [0.05,0.10,0.2,0.4,0.6,1,0.5]
mSizeS = [300 * i for i in mSize]
mx = [95,93,90.5,87,82.5,77,23]
my = [60,60,60,60,60,60,60]
plt.scatter(mx,my,s=mSizeS,facecolors="red", edgecolor="black",zorder=1,linewidth=0.5)
plt.scatter(5,60,s=150,facecolors="green", edgecolor="black",zorder=1,linewidth=0.5)
plt.text(86,56,"xG", color="white", ha="center",va="center", zorder=1, fontsize=13,fontproperties=fm_scada.prop)
plt.text(77, 59.8, "1", fontsize=11, color="black", zorder=1,ha="center", va="center",fontproperties=fm_scada.prop,weight = 'bold')
plt.text(82.5, 59.8, "0.6", fontsize=8, color="black", zorder=1,ha="center", va="center",fontproperties=fm_scada.prop,weight = 'bold')
plt.text(87, 59.8, "0.4", fontsize=6, color="black", zorder=1,ha="center", va="center",fontproperties=fm_scada.prop,weight = 'bold')
plt.text(13, 59.8, "Goal", fontsize=13, color="white", zorder=1,ha="center", va="center",fontproperties=fm_scada.prop,weight = 'bold')
plt.text(31, 59.8, "Miss", fontsize=12, color="white", zorder=1,ha="center", va="center",fontproperties=fm_scada.prop,weight = 'bold')

plt.text(50, 110, 'Shots In Transition', color='white',
                  va='center', ha='center',
                  fontproperties=fm_scada.prop, fontsize=15)
plt.text(50, 105, 'Benfica 20/21', color='red',
                  va='center', ha='center',
                  fontproperties=fm_scada.prop, fontsize=12)
    