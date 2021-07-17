from flask import request, render_template
import numpy as np
import pandas as pd
import pickle
import seaborn as sb

df = sb.load_dataset('diamonds')
df.to_csv('./data/diamonds.csv', index=False)

def init():
    global df
    df = pd.read_csv('./data/diamonds.csv')


def show_alert():
    alert = "Prediction page - Please enter valid input in the page fields"
    return render_template("primary_alert.html", data=alert)

def show_model_alert(alert):
    return render_template("model_alert.html", data=alert)

def load_model(filename):

    with open('./models/' + filename, 'rb') as model:
        return pickle.load(model)

def get_model(input):
    carat = input[0]
    x = input[6]
    y = input[7]
    z = input[8]
    color_dict = {'D':1, 'E':2, 'F':3, 'G':4, 'H':5, 'I':6, 'J':7}
    clarity_dict = {'IF':1, 'VVS1':2, 'VVS2':3, 'VS1':4, 'VS2':5, 'SI1':6, 'SI2':7, 'I1':8}
    cut_dict = {'Ideal':1, 'Premium':2, 'Very Good':3, 'Good':4, 'Fair':5}
    input[1] = cut_dict[input[1]]
    input[2] = color_dict[input[2]]
    input[3] = clarity_dict[input[3]]

    volume = x*y*z
    if carat <= 0.5:
        return load_model('df31model.sav')

    elif 0.6 >= carat > 0.5:
        return load_model('df32model.sav')

    elif 1.2 >= carat > 0.6:
        if x<6:
            return load_model('df331model.sav')
        else:
            return load_model('df332model.sav')

    elif 1.2 >= carat > 0.6:
        if x<6:
            return load_model('df331model.sav')
        else:
            return load_model('df332model.sav')

        
    elif carat > 1.2 and volume < 300:
        if volume < 225:
            return load_model('df341model.sav')
        else:
            return load_model('df342model.sav')

    else:
        return "not enough data to predict the price of this diamond" 


def configure(app):

    @app.route('/')
    def rtemplate():
        init()
        return render_template('main.html', data=df.head(20))

    @app.route('/details/<int:id>')
    def getdetails(id):
        return render_template('details.html', item=df.iloc[id])

    @app.route('/addnew')
    def add_new():
        return render_template('addnew.html')

    @app.route('/predict')
    def predict():
        return render_template('predict.html')

    @app.route('/additem', methods=['POST'])
    def additem():
        global df
        carat = float(request.form['carat'])
        cut = request.form['cut']
        color = request.form['color']
        clarity = request.form['clarity']
        depth = float(request.form['depth'])
        table = float(request.form['table'])
        x = float(request.form['x'])
        y = float(request.form['y'])
        z = float(request.form['z'])
        price = float(request.form['price'])
        df.loc[df.index.size] = [carat, cut, color,
                                 clarity, depth, table, price, x, y, z]
        df.to_csv('./data/diamonds.csv',index=False)
        return render_template('ok.html')

    @app.route('/predict',methods=['POST'])
    def predict_diamond():
        try:
            carat = float(request.form['carat'])
            depth = float(request.form['depth'])
            table = float(request.form['table'])
            x = float(request.form['x'])
            y = float(request.form['y'])
            z = float(request.form['z'])
        except ValueError:
            return show_alert()
    
        cut = request.form['cut']
        color = request.form['color']
        clarity = request.form['clarity']
        
        if "Select" in color or "Select" in clarity or "Select" in cut:
            return show_alert()

        input = [carat, cut, color, clarity, depth, table, x, y, z]
        model = get_model(input)
        if type(model) == str:
            return show_model_alert(model)
        try:
            pred = model.predict(np.reshape(input, [1, -1]))
        except:
            volume = input[6] * input[7] * input[8]
            input.append(volume)
            pred = model.predict(np.reshape(input, [1, -1]))
        return render_template('res.html',val=pred)

    
