from flask import request, render_template
import json
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

        v = dfmodel.predict([carat, cut, color, clarity, depth, table, 0, x, y, z])
        return render_template('res.html',val=v)

    
