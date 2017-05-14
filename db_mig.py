import pandas_datareader.data as web
import datetime    
import sqlite3

start = datetime.datetime(1999, 1, 1)
end = datetime.datetime(2017, 5, 6)

conn = sqlite3.connect("viki/data.db")

def strCode(code_int):
	code_str = str(code_int)
	code_str = "0" * (6-len(code_str)) + code_str
	return code_str

cur = conn.cursor()
cur.execute("select * from company;")
rows = cur.fetchall()
for row in rows:
	code = strCode(row[1])+".KS"
	kospi = 1
	date = None
	try:
		df = web.DataReader(code, 'yahoo', start, end)
		kospi = 1
		date = df.first_valid_index()
	except Exception as inst:
		kospi = 0
	if date != None:
		date = date.to_datetime()
	cur.execute("insert or replace into company2 values (?,?,?,?,?)", (row[0], row[1], row[2], kospi, date))
	conn.commit()
	print code
conn.close()