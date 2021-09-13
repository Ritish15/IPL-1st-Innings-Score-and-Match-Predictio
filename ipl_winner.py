import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split


dataset=pd.read_csv('matches.csv')
copy_data = dataset.copy()
copy_data['city'].fillna('Dubai',inplace=True)
copy_data['umpire1'].fillna('Aleem Dar',inplace=True)

null_values_col = copy_data.isnull().sum()
null_values_col = null_values_col[null_values_col != 0].sort_values(ascending = False).reset_index()
null_values_col.columns = ["variable", "number of missing"]

consistent_teams = ['Kolkata Knight Riders', 'Chennai Super Kings', 'Rajasthan Royals',
                    'Mumbai Indians', 'Kings XI Punjab', 'Royal Challengers Bangalore',
                    'Delhi Capitals', 'Sunrisers Hyderabad']

df = copy_data[(copy_data['team1'].isin(consistent_teams)) & (copy_data['team2'].isin(consistent_teams))]
df = pd.DataFrame(df,columns=['team1', 'team2', 'toss_decision','toss_winner','city', 'venue', 'season', 'win_by_runs', 'win_by_wickets', 'umpire1', 'winner'])

df['winner'].fillna('Draw', inplace=True)
df.replace(['Kolkata Knight Riders', 'Chennai Super Kings', 'Rajasthan Royals',
                    'Mumbai Indians', 'Kings XI Punjab', 'Royal Challengers Bangalore',
                    'Delhi Capitals', 'Sunrisers Hyderabad']
                ,['KKR','CSK','RR','MI','KXIP','RCB','DC','SRH'],inplace=True)

encode = {'team1': {'KKR':1,'CSK':2,'RR':3,'MI':4,'KXIP':5,'RCB':6,'DC':7,'SRH':8},
          'team2': {'KKR':1,'CSK':2,'RR':3,'MI':4,'KXIP':5,'RCB':6,'DC':7,'SRH':8},
          'toss_winner': {'KKR':1,'CSK':2,'RR':3,'MI':4,'KXIP':5,'RCB':6,'DC':7,'SRH':8},
          'winner':{'KKR':1,'CSK':2,'RR':3,'MI':4,'KXIP':5,'RCB':6,'DC':7,'SRH':8,'Draw':9}}
df.replace(encode, inplace=True)


columns_to_remove = ['city', 'venue','season', 'win_by_runs', 'win_by_wickets', 'umpire1']
df.drop(labels=columns_to_remove, axis=1, inplace=True)

df.loc[df["toss_winner"]==df["team1"],"team1_toss_win"]=1
df.loc[df["toss_winner"]!=df["team1"],"team1_toss_win"]=0


df["team1_bat"]=0
df.loc[(df["team1_toss_win"]==1) & (df["toss_decision"]=="bat"),"team1_bat"]=1

df.loc[df["winner"]==df["team1"],"team1_win"]=1
df.loc[df["winner"]!=df["team1"],"team1_win"]=0


columns_to_remove = ['toss_decision', 'toss_winner','winner']
df.drop(labels=columns_to_remove, axis=1, inplace=True)


encode = {'team1': {1:'KKR',2:'CSK',3:'RR',4:'MI',5:'KXIP',6:'RCB',7:'DC',8:'SRH'},
           'team2': {1:'KKR',2:'CSK',3:'RR',4:'MI',5:'KXIP',6:'RCB',7:'DC',8:'SRH'} }       
df.replace(encode, inplace=True)

from sklearn.preprocessing import OneHotEncoder
encoded_df = pd.get_dummies(data=df, columns=['team1', 'team2'])

df = encoded_df[['team1_CSK','team1_DC','team1_KKR','team1_KXIP','team1_MI','team1_RCB','team1_RR','team1_SRH',
                         'team2_CSK','team2_DC','team2_KKR','team2_KXIP','team2_MI','team2_RCB','team2_RR','team2_SRH',
                      'team1_toss_win', 'team1_bat','team1_win' ]]




x=df.iloc[:,:-1].values
y=df.iloc[:,-1].values
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

from sklearn.linear_model import LogisticRegression

logreg = LogisticRegression()
logreg.fit(x_train, y_train)
print("**************************"+str(x_train.shape)+"*******")
# Creating a pickle file for the classifier
filename = 'ipl_winner_model.pkl'
pickle.dump(logreg, open(filename, 'wb'))
