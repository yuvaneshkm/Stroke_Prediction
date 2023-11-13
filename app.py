# Importing necessary libraries:
from flask import Flask, render_template, request
from flask_cors import cross_origin
import pickle
import json
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# App:
app = Flask(__name__)

# Loading the model:
with open("Stroke_predictor.pickle", 'rb') as file:
    model = pickle.load(file)
file.close()

# Loading columns:
with open("columns.json", 'rb') as file:
    column = json.load(file)
file.close()
columns = column['data_columns']


@app.route('/')
@cross_origin()
def home():
    return render_template('home.html')


@app.route('/predict', methods=['GET', 'POST'])
@cross_origin()
def predict():
    if request.method=='POST':

        age = request.form['Age']
        work = request.form['work']
        residence = request.form['residence']

        avg_glu_lvl = request.form['glucose']
        avg_glu_lvl = float(avg_glu_lvl)

        bmi = request.form['bmi']
        bmi = float(bmi)

        smoke = request.form['smoke']
    
        a = np.zeros(len(columns))
    
        # age:
        a[0]=age
    
    
        # work_type:
        if work=='Children':
            a[1]=0
        elif work=='Government Job':
            a[1]=1
        elif work=='Self Employed':
            a[1]=2
        elif work=='Private Job':
            a[1]=3
        

        # Residence_type:
        if residence=='Urban':
            a[2]=1
        elif residence=='Rural':
            a[2]=0
        

        # avg_glucose_level:
        a[3]=avg_glu_lvl
    

        # bmi:
        a[4]=bmi
    

        # smoking_status:
        if smoke=='Unknown':
            a[5]=0
        elif smoke=='Never Smoked':
            a[5]=1
        elif smoke=='Formerly Smoked':
            a[5]=2
        elif smoke=='Smokes':
            a[5]=3
        
        
        # Prediction:
        stroke = model.predict([a])[0]

        if stroke==1:
            return render_template('home.html', prediction_text1="You have a high chance of getting Stroke. So, please consult your doctor!")
        else:
            return render_template('home.html', prediction_text2="You have a less chance of getting Stroke!")
        
    return render_template('home.html')


if __name__=='__main__':
    app.run(debug=True)
