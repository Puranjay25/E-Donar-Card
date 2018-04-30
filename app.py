from flask import Flask, render_template, session, request, redirect, url_for, session
from db import connect

app=Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/view',methods=['GET'])
def view():
	a,b=connect()
	detail=b.execute("Select Id, Username, Email, contact, Age, Balance from signup where Username='Alex'")
	details=b.fetchall()
	a.commit()
	a.close()
	b.close()
	return render_template('viewcard.html',details=details)

@app.route('/claim')
def claim():
	return render_template('claim.html')

@app.route('/logout')
def logout():
	return redirect(url_for('index'))

@app.route('/usecard',methods=['GET','POST'])
def usecard():
	return render_template('usecard.html')

@app.route('/claimed')
def claimed():
	a,b=connect()
	ids1=request.form.get("name1",False)
	ids2=request.form.get("name2",False)
	unit=request.form.get("units",False)
	balance1=b.execute("select Balance from signup where Id='%s'"%(ids1))
	b.execute("update signup set Balance='%s' where Id ='%s'"%(balance1+unit,ids1))
	balance2=b.execute("select Balance from signup where Id='%s'"%(ids2))
	b.execute("update signup set Balance='%s' where Id ='%s'"%(balance2-unit,ids2))
	a.commit()
	a.close()
	b.close()
	return render_template('usecard.html')

@app.route('/requests',methods=['POST','GET'])
def requests():
	if request.method=='POST':
		a,b=connect()
		name=request.form.get("name",False)
		contact=request.form.get("phone",False)
		address=request.form.get("address",False)
		bg=request.form.get("bg",False)
		unit=request.form.get("unit",False)
		if name!='':
			b.execute("insert into request(Name, Contact, Address, Blood_group, Units) values(%s, %s, %s, %s, %s)",(name, contact, address,bg,unit))
		a.commit()
		a.close()
		b.close()
	return render_template('Request.html')

@app.route('/donarinfo')
def donarinfo():
	a,b=connect()
	detail=b.execute("select * from request")
	details=b.fetchall()
	return render_template('Donar_information.html',details=details)

@app.route('/homepage')
def homepage():
	a,b=connect()
	names=b.execute("select id, Name, Blood_group, Units from request ")
	name=b.fetchall()
	return render_template('homepage.html',name=name)

@app.route('/login',methods=['POST','GET'])
def login():
	if request.method=='POST':
		a,b=connect()
		Name=request.form.get("Name",False)
		Password=request.form.get("Password",False)
		if Name!='':
			get_username=b.execute("select * from signup where Username='%s'"%(Name))
			get_pass=b.fetchone()[5]
			if get_pass==Password:
				return redirect(url_for('homepage'))
			else:
				return redirect(url_for('login'))
		session['username']=Name
		session['logged_in']=True
		a.commit()
		a.close()
		b.close()
	return render_template('login.html')

@app.route('/signup',methods=['POST','GET'])
def signup():
	if request.method=='POST':
		a,b=connect()
		name=request.form.get("Name",False)
		mail=request.form.get("E-mail",False)
		contact=request.form.get("Contact",False)
		age=request.form.get("age",False)
		password=request.form.get("Password",False)
		confirm=request.form.get("Confirm-Password",False)
		if name!='':
			b.execute("insert into signup(Username, Email, contact, Age, Password, Confirm_Password) values(%s, %s, %s, %s, %s, %s)",
				(name, mail, contact, age, password, confirm))
		a.commit()
		a.close()
		b.close()
	return render_template('signup.html')

if __name__=='__main__':
	app.run(debug=True)