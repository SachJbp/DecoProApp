#import numpy as np
from flask import Flask, request, jsonify, render_template, url_for, make_response
import pickle
from flask import send_from_directory
#import pandas as pd
from werkzeug import secure_filename
import os
import math
import pandas as pd
import DemandPrediction
from io import BytesIO
from google.cloud import storage


app = Flask(__name__)
#model = pickle.load(open('randomForestRegressor.pkl','rb'))

#CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
       #if request.method == 'POST':
       #   f = request.files.get('file')
       #uploaded_file = request.files.get('file')

       if request.method == 'POST':
          
           df = pd.read_excel(request.files.get('file1'))
           df2 = pd.read_excel(request.files.get('file2'))
           df=DemandPrediction.demandpred(df.copy(),df2.copy())

           resp = make_response(df.to_csv())
           resp.headers["Content-Disposition"] = "attachment; filename=Demand.csv"
           resp.headers["Content-Type"] = "text/csv"
           return resp
           #return render_template('home1.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)
           #return "good"
       return "nice"

@app.route('/')
def home():
    #return 'Hello World'
    return render_template('home1.html')
    #return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
