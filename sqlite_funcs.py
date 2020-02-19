#!/usr/bin/python3

import sqlite3
import re
from datetime import date

date_pattern = re.compile(r'(\d\d)-(\d\d)-(\d\d\d\d)', )
search = date_pattern.search("This is 09-06-2020")

exercises = [
			'DB_Bench_Press',
			'DB_Shoulder_Press',
			'DB_Inclince_Press',
			'Lat_Pulldown',
			'Seated_Cable_Row',
			'DB_Row',
			'Face_Pull',
			'Side_Raise',
			'DB_Hammer',
			'DB_Skulls'
			]

# Access our database. 
class ConnectDatabase:
	def __init__(self):
		pass

	def connect(self): 
		self.con = sqlite3.connect('data.db')
		self.c = self.con.cursor()

	def disconnect(self):
		self.c.close()
		self.con.close()

	def create_table(self, exers):

		self.connect()

		for each in exers:
			self.c.execute(f'''CREATE TABLE IF NOT EXISTS "{each}" (Date TEXT, 
					Weight REAL, Sets REAL, Reps1 REAL, Reps2 REAL, Reps3 REAL,
					Reps4 REAL, Reps5 REAL, Reps6 REAL, Reps7 REAL, Reps8 REAL, 
					Reps9 REAL, Reps10 REAL)''')

		self.disconnect()

	def insert_to_table(self, exercise):
		'''
			Insert values based on user input from GUI to database.
		'''

		self.connect()

		self.c.execute(f'''INSERT INTO {exercise} (Date, Weight, Sets, Reps1,
				Reps2, Reps3, Reps4, Reps5, Reps6, Reps7, Reps8, Reps9,
				Reps10) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
				("19-2-2020", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))

		self.con.commit()

		self.disconnect()

	def get_tables(self):
		'''
			Fetch all tables from data.db and store them into lists. 
			Get all the exercises listed in the database.
			Format the fetched data into neater output to our kivy app. 
		'''
		self.connect()

		table_list = []
		table_list2 = [] 

		self.c.execute('SELECT name FROM sqlite_master WHERE type="table"')

		reader = self.c.fetchall()

		# Get all listed tables in database.
		for each in reader:
			table_list.append(each[0])

		# Replace underscores with spaces for our UI output.
		for each in table_list:
			split_list = each.split('_')
			join_list =  ' '.join(split_list)
			table_list2.append(join_list)

		self.disconnect()

		return table_list, table_list2

	def get_latest(self, exercise):
		'''
			Fetch the latest data regarding the exercise selected.
			For example, if the latest datef for Bench Press is June 16,
				fetch all Bench Press data for June 16. 
		'''
		self.connect()

		# Replace spaces in exercise with underscores.
		split_list = exercise.split(" ")
		join_list = '_'.join(split_list)

		self.c.execute(f'SELECT * FROM "{join_list}"')
		
		# Fetch everything from selected table.
		reader = self.c.fetchall()
		# Fetch the last/latest entry in table.
		latest_date = reader[-1]

		self.disconnect()

		return latest_date
		

if __name__ == '__main__':
	my_db = ConnectDatabase()
	print(my_db.get_all_exercises())






