from flask import *
import mysql.connector
from werkzeug.utils import secure_filename

import os
import csv
app=Flask(__name__)
app.secret_key="dnt tell" # 
myconn = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="feedback"
)





@app.route("/")
@app.route("/register",methods=['GET','POST'])
def register():
	 return render_template("register.html")

@app.route("/about")
def about():
     return render_template("about.html")

@app.route("/login",methods=['GET','POST'])
def login():
	    if request.method=="POST":
		    
		     uname=request.form['uname']
		     pwd=request.form['pwd']
		
		
	    return render_template("login.html")

@app.route("/eventcreation",methods=['GET','POST'])
def eventcreation():
    if request.method=="POST":
        eventname=request.form['eventname']
        courses=request.form.getlist('courses')
        courses=','.join(courses)
        mycur=myconn.cursor()
        mycur.execute("""insert into event(eventname,courses)values(%s,%s)""",(eventname,courses))
        myconn.commit()
        flash("Registered successfully")

        return redirect(url_for('eventcreation'))
    else:

        return render_template("eventcreation.html")

@app.route("/view",methods=['GET','POST'])
def view():
	
	cur=myconn.cursor()
	cur.execute("select * from event")
	data=cur.fetchall()
	return render_template("view.html",data=data)

@app.route("/delete",methods=['GET','POST'])
def delete():
	if request.method == "POST":
		id=request.form['delete']
		cur=myconn.cursor()
		cur.execute("delete from event where sno=%s"%(id))
		myconn.commit()
		flash("Deleted Successfully")
		return redirect(url_for('view'))



@app.route("/edit",methods=['GET','POST'])
def edit():
	if request.method == "POST":
		id=request.form['edit']
		cur=myconn.cursor()
		cur.execute("select * from event where sno=%s"%(id))
		data=cur.fetchall()
		courses=data[0][-1].split(',')
		return render_template("eventedit.html",data=data,courses= courses)

	return "KJUHKJHKJW"



if __name__=="__main__":
        app.run(debug=True)