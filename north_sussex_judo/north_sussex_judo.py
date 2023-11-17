
import sqlite3

# Connect to database
conn = sqlite3.connect('north_sussex_judo.db')
c = conn.cursor()

# Create tables
c.execute ('''
    CREATE TABLE IF NOT EXISTS athlete (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    weight INTEGER NOT NULL,
    training_plan_id INTEGER ALLOW NULL,
    weight_category_id INTEGER ALLOW NULL,       
    )
    ''')

c.execute ('''
    CREATE TABLE IF NOT EXISTS training_plan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    cost_per_month FLOAT ALLOW NULL,
    cost_per_hour  FLOAT ALLOW NULL,
    sessions_per_week INTGER NOT NULL,
    )
    ''')

c.execute ('''
    CREATE TABLE IF NOT EXISTS weight_category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    upper_weight_limit INTEGER NOT NULL,
    )
    ''')

c.execute ('''
    CREATE TABLE IF NOT EXISTS competition (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date TEXT NOT NULL,
    price FLOAT NOT NULL,
    )
    ''')

c.execute ('''
    CREATE TABLE IF NOT EXISTS competition_athlete (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    competition_id INTEGER NOT NULL,
    athlete_id INTEGER NOT NULL,       
    )
    ''')

c.execute ('''
    CREATE TABLE IF NOT EXISTS invoice (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date TEXT NOT NULL,
    amount FLOAT NOT NULL,
    athlete_id INTEGER ALLOW NULL,       
    )
    ''')
    
# Insert data into tables
conn.commit()

# Close connection to database
conn.close()

class Athlete:

   def __init__(self, name, weight, training_plan_id, weight_category_id):
        self.name = name
        self.weight = weight
        self.training_plan_id = training_plan_id
        self.weight_category_id = weight_category_id
        
   def __str__(self):
       return f'Athlete: {self.name}, {self.weight}, {self.training_plan_id}, {self.weight_category_id}'

class TrainingPlan:

    def __init__(self, name, cost_per_month, cost_per_hour, sessions_per_week):
          self.name = name
          self.cost_per_month = cost_per_month
          self.cost_per_hour = cost_per_hour
          self.sessions_per_week = sessions_per_week
          
    def __str__(self):
        return f'Training Plan: {self.name}, {self.cost_per_month}, {self.cost_per_hour}, {self.sessions_per_week}'

class WeightCategory:

    def __init__(self, name, upper_weight_limit):
          self.name = name
          self.upper_weight_limit = upper_weight_limit
          
    def __str__(self):
        return f'Weight Category: {self.name}, {self.upper_weight_limit}'
    
class Competition:

    def __init__(self, name, date, price):
          self.name = name
          self.date = date
          self.price = price
          
    def __str__(self):
        return f'Competition: {self.name}, {self.date}, {self.price}'

class Invoice:

    def __init__(self, name, date, amount, athlete_id):
          self.name = name
          self.date = date
          self.amount = amount
          self.athlete_id = athlete_id
          
    def __str__(self):
        return f'Invoice: {self.name}, {self.date}, {self.amount}, {self.athlete_id}'



