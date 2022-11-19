# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re

  
app = Flask(__name__)
  
app.secret_key = 'a'

conn=ibm_db.connect(""DATABASE=bludb;HOSTNAME=6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30376;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;PROTOCOL=TCPIP;UID=nkq41110;PWD=2jpo8fPJraZ3KYPc",'','')

@app.route('/')

def homer():
    return render_template('index.html')


@app.route('/login',methods =['GET', 'POST'])
def login():
   msg=''

  if request.method=='post':
      username=request.form['username']
      password=request.form['password']
      sql="SELECT * FROM users WHERE username=? AND password=?"
     stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['Loggedin']=True
            session['id']=account['USERNAME']
            userid=account["USERNAME"]
            session['username']=account["USERNAME"]
            msg='Logged in successfully!'
            return render_template("dashboard.html",msg=msg)
        else:
            msg="Incorrect username/password"
    return render_template('login.html',msg=msg)


    return render_template('login.html')

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg=" "
    if request.method=="POST":
        
        username=request.form['username']
        password=request.form['password']
        email=request.form['email']
        sql="SELECT * FROM users WHERE username=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg="Account already exists!"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
            msg="Invalid email address"
        elif not re.match(r'[A-Za-z0-9]+',username):
            msg="name must contain only characters and numbers"
        else:
            insert_sql="INSERT INTO user VALUES(?,?,?)"
            prep_stmt=ibm_db.prepare(conn,insert_sql)
            ibm_db.bind_param(prep_stmt,1,email)
            ibm_db.bind_param(prep_stmt,2,username)
            ibm_db.bind_param(prep_stmt,3,password)
            ibm_db.execute(prep_stmt)
            msg='You have successfully registered!'
    elif request.method=='POST':
      msg='Please fill out of the form'
      
    return render_template('register.html')




    
if __name__ == '__main__':
   app.run(host='0.0.0.0',port=8080)
