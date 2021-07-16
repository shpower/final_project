from flask import request, render_template
import json
import pandas as pd
import pickle
import seaborn as sb

df = sb.load_dataset('diamonds').head(20)


def configure(app):

    @app.route('/')
    def rtemplate():
        return render_template('main.html', data=df)

    @app.route('/details/<int:id>')
    def getdetails(id):
        return render_template('details.html', item=df.iloc[id])

    @app.route('/addnew')
    def add_new():
        return render_template('addnew.html')

    @app.route('/predict')
    def predict():
        return render_template('predict.html')
