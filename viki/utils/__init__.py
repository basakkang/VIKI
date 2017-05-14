import datetime
import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "data.db")

def strCode(code_int):
	code_str = str(code_int)
	code_str = "0" * (6-len(code_str)) + code_str
	return code_str

def getRandCompany(num):
	conn = sqlite3.connect(db_path)
	cur = conn.cursor()
	query = "SELECT * FROM company2 where kospi = 1 ORDER BY RANDOM();"
	cur.execute(query)
	rows = cur.fetchall()
	codes = map(lambda x: x[1], rows[:num])
	conn.close()
	return codes

def getCloseStartDate(codes):
	conn = sqlite3.connect(db_path)
	cur = conn.cursor()
	query = "SELECT start_date FROM company2 where name in ("
	for code in codes[:-1]:
		query += str(code) + ","
	query += str(codes[-1])
	query += ") ORDER BY start_date"
	cur.execute(query)
	rows = cur.fetchall()
	return datetime.datetime.strptime(rows[-1][0], '%Y-%m-%d %H:%M:%S')