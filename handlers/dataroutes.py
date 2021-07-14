from flask import request,render_template
import json
import pandas as pd
import pickle


def configure(app):

    @app.route('/')
    def hello_world():
        return render_template('main.html',data=df)

 