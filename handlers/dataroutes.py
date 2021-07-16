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
