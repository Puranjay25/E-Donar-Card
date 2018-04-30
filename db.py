import MySQLdb

def connect():
	a=MySQLdb.connect(user="root", host="localhost", db="hackathon", passwd="dontbeevil")
	b=a.cursor()
	return a,b