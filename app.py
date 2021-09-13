# Importing essential libraries
from flask import Flask, render_template, request
import pickle
import numpy as np

# Load the Random Forest CLassifier model
filename = 'first-innings-score-lr-model.pkl'
regressor = pickle.load(open(filename, 'rb'))
reg=pickle.load(open("ipl_winner_model.pkl",'rb'))

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    temp_array = list()
    
    if request.method == 'POST':
        
        team1 = request.form['batting-team']
        if team1 == 'Chennai Super Kings':
            temp_array = temp_array + [1,0,0,0,0,0,0,0]
        elif team1 == 'Delhi Daredevils':
            temp_array = temp_array + [0,1,0,0,0,0,0,0]
        elif team1 == 'Kings XI Punjab':
            temp_array = temp_array + [0,0,1,0,0,0,0,0]
        elif team1 == 'Kolkata Knight Riders':
            temp_array = temp_array + [0,0,0,1,0,0,0,0]
        elif team1 == 'Mumbai Indians':
            temp_array = temp_array + [0,0,0,0,1,0,0,0]
        elif team1 == 'Rajasthan Royals':
            temp_array = temp_array + [0,0,0,0,0,1,0,0]
        elif team1 == 'Royal Challengers Bangalore':
            temp_array = temp_array + [0,0,0,0,0,0,1,0]
        elif team1 == 'Sunrisers Hyderabad':
            temp_array = temp_array + [0,0,0,0,0,0,0,1]
            
            
        bowling_team = request.form['bowling-team']
        if bowling_team == 'Chennai Super Kings':
            temp_array = temp_array + [1,0,0,0,0,0,0,0]
        elif bowling_team == 'Delhi Daredevils':
            temp_array = temp_array + [0,1,0,0,0,0,0,0]
        elif bowling_team == 'Kings XI Punjab':
            temp_array = temp_array + [0,0,1,0,0,0,0,0]
        elif bowling_team == 'Kolkata Knight Riders':
            temp_array = temp_array + [0,0,0,1,0,0,0,0]
        elif bowling_team == 'Mumbai Indians':
            temp_array = temp_array + [0,0,0,0,1,0,0,0]
        elif bowling_team == 'Rajasthan Royals':
            temp_array = temp_array + [0,0,0,0,0,1,0,0]
        elif bowling_team == 'Royal Challengers Bangalore':
            temp_array = temp_array + [0,0,0,0,0,0,1,0]
        elif bowling_team == 'Sunrisers Hyderabad':
            temp_array = temp_array + [0,0,0,0,0,0,0,1]
            
            
        overs = float(request.form['overs'])
        runs = int(request.form['runs'])
        wickets = int(request.form['wickets'])
        runs_in_prev_5 = int(request.form['runs_in_prev_5'])
        wickets_in_prev_5 = int(request.form['wickets_in_prev_5'])
        
        temp_array = temp_array + [overs, runs, wickets, runs_in_prev_5, wickets_in_prev_5]
        
        data = np.array([temp_array])
        my_prediction = int(regressor.predict(data)[0])
              
        return render_template('result.html', lower_limit = my_prediction-10, upper_limit = my_prediction+5)



@app.route('/matchprediction')
def matchprediction():
   return render_template('matchpredict.html')



@app.route('/iplwinner', methods=['POST'])
def iplwinner():
    temp_list = list()
    
    if request.method == 'POST':
  
                
        team1 = request.form['team1']
        if team1 == 'Chennai Super Kings':
            temp_list = temp_list + [1,0,0,0,0,0,0,0]
        elif team1 == 'Delhi Capitals':
            temp_list = temp_list + [0,1,0,0,0,0,0,0]
        elif team1 == 'Kings XI Punjab':
            temp_list = temp_list + [0,0,0,1,0,0,0,0]
        elif team1 == 'Kolkata Knight Riders':
            temp_list = temp_list + [0,0,1,0,0,0,0,0]
        elif team1 == 'Mumbai Indians':
            temp_list = temp_list + [0,0,0,0,1,0,0,0]
        elif team1 == 'Rajasthan Royals':
            temp_list = temp_list + [0,0,0,0,0,0,1,0]
        elif team1 == 'Royal Challengers Bangalore':
            temp_list = temp_list + [0,0,0,0,0,1,0,0]
        elif team1 == 'Sunrisers Hyderabad':
            temp_list = temp_list + [0,0,0,0,0,0,0,1]
            
            
        
                
        team2=request.form['team2']
        if team2 == 'Chennai Super Kings':
            temp_list = temp_list + [1,0,0,0,0,0,0,0]
        elif team2 == 'Delhi Capitals':
            temp_list = temp_list + [0,1,0,0,0,0,0,0]
        elif team2 == 'Kings XI Punjab':
            temp_list = temp_list + [0,0,0,1,0,0,0,0]
        elif team2 == 'Kolkata Knight Riders':
            temp_list = temp_list + [0,0,1,0,0,0,0,0]
        elif team2 == 'Mumbai Indians':
            temp_list = temp_list + [0,0,0,0,1,0,0,0]
        elif team2 == 'Rajasthan Royals':
            temp_list = temp_list + [0,0,0,0,0,0,1,0]
        elif team2 == 'Royal Challengers Bangalore':
            temp_list = temp_list + [0,0,0,0,0,1,0,0]
        elif team2 == 'Sunrisers Hyderabad':
            temp_list = temp_list + [0,0,0,0,0,0,0,1]
                

        tos_win=int(request.form['tos_win'])
        tos_des=request.form['tosdes']
        if tos_win==1 and tos_des=="Batting":
            tsw=1
        else:
            tsw=0
          
        temp_list = temp_list + [tos_win,tsw]
        ask="match is going to win by "        

        #return ask
        data = np.array([temp_list])
        my_pred = int(reg.predict(data))
        if my_pred==1:
            ask+=team1
        else:
            ask+=team2    

        return "<h1>"+ask+"</h1>"


















@app.route('/contact')
def  contactus():
   return render_template('contact.html')




   
if __name__ == '__main__':
	app.run(debug=True)