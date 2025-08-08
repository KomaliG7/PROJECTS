"""from flask import Flask, render_template,request
app = Flask(__name__)

@app.route('/', method=['post'])
def home():
    return render_template('home.html')

if __name__==__name__:
    app.run(host='127.0.0.1',port=4500,debug=True)"""

from flask import Flask, render_template,request,jsonify
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn import metrics

app=Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('homepage.html')
@app.route('/login')
def login():
    return render_template('loginpage.html')

@app.route('/LoginAction', method=['post'])
def LoginAction():
    if request.method=='post':
        email=request.form('email')
        password=request.form('pass')
        if (email == 'admin@gmail.com') and (password=='Admin'):
            return render_template('upload.html')
        
    return render_template('homepage.html')

if __name__=="__main__":
    app.run(debug=True)