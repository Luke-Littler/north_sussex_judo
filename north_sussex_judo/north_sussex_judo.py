# Author: Luke Littler
# Purpose: To create a database for North Sussex Judo Club

import sqlite3
import datetime
import calendar
import random

x = datetime.datetime.now()

conn = sqlite3.connect('north_sussex_judo.db')
c = conn.cursor()

c.execute ('''
    CREATE TABLE IF NOT EXISTS athlete (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    weight INTEGER,
    training_plan_id INTEGER,
    weight_category_id INTEGER     
    )
    ''')

c.execute ('''
    CREATE TABLE IF NOT EXISTS training_plan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    cost_per_month DECIMAL(10,2),
    cost_per_hour  DECIMAL(10,2),
    sessions_per_week INTEGER
    )
    ''')

if c.execute('SELECT * FROM training_plan').fetchone() is None:
 c.execute ('''
        INSERT INTO training_plan (id, name, cost_per_month, cost_per_hour, sessions_per_week) 
        VALUES 
        (0, 'Private Tuition', 0, 9.50, 0),    
        (1, 'Beginner', 100.00, 0, 2),
        (2, 'Intermediate', 120.00, 0, 3),
        (3, 'Elite', 140.00, 0, 5)
        ''')
 conn.commit()

c.execute ('''
    CREATE TABLE IF NOT EXISTS weight_category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    upper_weight_limit INTEGER
    )
    ''')

if c.execute('SELECT * FROM weight_category').fetchone() is None:
 c.execute ('''
        INSERT INTO weight_category (id, name, upper_weight_limit) 
        VALUES 
        (1, 'Flyweight', 66),
        (2, 'Lightweight', 73),
        (3, 'Light-middleweight', 81),
        (4, 'Middleweight', 90),       
        (5, 'Light-heavyweight', 100),
        (6, 'Heavyweight', 635)      
        ''')
 conn.commit()

c.execute ('''
    CREATE TABLE IF NOT EXISTS competition (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day TEXT,
    month TEXT,
    year TEXT,
    price DECIMAL(10,2) DEFAULT 22.50
    )
    ''')

c.execute ('''
    CREATE TABLE IF NOT EXISTS competition_athlete (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    competition_id INTEGER,
    athlete_id INTEGER
    )
    ''')

c.execute ('''
    CREATE TABLE IF NOT EXISTS invoice (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    athlete_id INTEGER,
    name TEXT,       
    weight INTEGER,
    weight_category TEXT,
    training_plan TEXT,
    sessions_per_week INTEGER,
    training_plan_cost DECIMAL(10,2),       
    private_sessions INTEGER,
    private_session_cost DECIMAL(10,2),
    private_session_total DECIMAL(10,2),       
    competition_id INTEGER DEFAULT 0,
    competition_cost DECIMAL(10,2) DEFAULT 0,       
    total DECIMAL(10,2),
    month TEXT,
    year TEXT      
    )
    ''')

conn.commit()

class Athlete:
   
   def __init__(self, name, weight, training_plan_id, weight_category_id):
        self.name = name
        self.weight = weight
        self.training_plan_id = training_plan_id
        self.weight_category_id = weight_category_id
        
   def __str__(self):
       return f'Athlete: {self.name}, {self.weight}, {self.training_plan_id}, {self.weight_category_id}'
   
   def athlete_menu():
    print(' ')
    print('Athlete Menu...')
    print(' ')
    print('Please select an option from the menu below: ')
    print('1. Register Athlete')
    print('2. Find Athlete')
    print('3. View Athletes')
    print(' ')
    print('M. Main Menu')
    print(' ')
    
    option = input('Please enter your option: ')
    if option == '1':
        Athlete.register_athlete()
    elif option == '2':
        Athlete.find_athlete(None)
    elif option == '3':
        Athlete.view_athletes()
    elif option == 'M':
        start()
    else:
        print('Invalid option selected')
        Athlete.athlete_menu()
   
   def register_athlete():
       print(' ')
       print('Register a new athlete...')
       print('')
       print('Please enter the following details:')
       name = input('Athlete Name: ')
       name = name.title()
       print(' ')
       print('You have entered ' + str(name) + '.') 
       print(' ')
       print('Is this correct?') 
       print('1. Yes')
       print('2. No')
       print(' ')
       option = input('Please enter your option: ')
       if option == '1':
              print(' ')
       elif option == '2':
              Athlete.register_athlete()
       else:
              print('Invalid option selected')
              Athlete.register_athlete()
              
       c.execute('INSERT INTO athlete (name) VALUES (?)', (name,))
       conn.commit()
       
       id = c.lastrowid
       
       print(str(name) + ' has been created in the database with ID ' + str(id) + '.')
       print(' ')
       
       Athlete.enter_training_plan(id, name)
      
   def enter_training_plan(id, name):
    print('Please select a training plan for ' + str(name) + ' from the list below:') 
    print(' ')
    sql = ('SELECT * FROM training_plan EXCEPT SELECT * FROM training_plan WHERE id = 0')
    c.execute(sql)
    training_plan = c.fetchall()
    training_plan_range = len(training_plan)
    for training_plan in training_plan: 
        print(str(training_plan[0]) + '. ' + str(training_plan[1]))
        print('Cost per month: ' + u'\u00a3' + str(format(training_plan[2],".2f")))
        print('Cost per hour: ' + u'\u00a3' + str(format(training_plan[3],".2f")))
        print('Sessions per week: ' + str(training_plan[4]))
        print(' ')
    
    training_plan_id = input('Please Enter Training Plan Number: ')
    if training_plan_id.isnumeric():
        if int(training_plan_id) <= int(training_plan_range):
            tp = ('SELECT id, name FROM training_plan WHERE id = ?')
            c.execute(tp, (training_plan_id,))
            training_plan = c.fetchone()
            print(' ')
            print('You have selected ' + str(training_plan[1]) + ' training plan.')
            print(' ')
            print('Is this correct?')
            print('1. Yes')
            print('2. No')
            print(' ')
            option = input('Please enter your option: ')
            if option == '1':
                print(' ')
                print(str(training_plan[1]) + ' training plan' + ' has been assigned to ' + str(name) + '.')
            elif option == '2':
                Athlete.enter_training_plan(id, name)
            else:
                print('Invalid option selected')
                Athlete.enter_training_plan(id, name)
        else:
            print(' ')
            print('Invalid training plan selected')
            print(' ')
            Athlete.enter_training_plan(id, name)
    else:
        print(' ')
        print('Invalid training plan selected')
        print(' ')
        Athlete.enter_training_plan(id, name)

    c.execute('UPDATE athlete SET training_plan_id = ? WHERE id = ?', (training_plan_id, id))
    conn.commit()
    
    Athlete.enter_weight(id, name)
    
   def enter_weight(id, name):
    print(' ')
    weight = input(str(name) + 's' + ' Weight(kg): ')
    if (weight.isnumeric() and int(weight) <= 635):
        print(' ')
        print('You have entered ' + str(weight) + 'kg for ' + str(name) + '.')
        print(' ')
        print('Is this correct?') 
        print('1. Yes')
        print('2. No')
        print(' ')
    else:
        print(' ') 
        print('Invalid weight entered, Please try again.')
        Athlete.enter_weight(id, name)
     
    option = input('Please enter your option: ')
    if option == '1':
         print(' ')
         print(str(weight) + 'kg has been assigned to ' + str(name) + '.')
         print(' ')
    elif option == '2':
         Athlete.enter_weight(id, name)
    else:
         print('Invalid option selected')
         Athlete.enter_weight(id, name)
    
    sql = ('SELECT id, upper_weight_limit FROM weight_category ORDER BY upper_weight_limit ASC')
    c.execute(sql)
    weight_category = c.fetchall()
    for weight_category in weight_category: 
        if int(weight) <= weight_category[1]:
             weight_category_id = weight_category[0]
             break
    
    c.execute('UPDATE athlete SET weight = ? WHERE id = ?', (weight, id))
    conn.commit()
        
    if weight_category_id > 0:
        c.execute('UPDATE athlete SET weight_category_id = ? WHERE id = ?', (weight_category_id, id))
        conn.commit()
        Athlete.print_athlete(id)
        
   def print_athlete(id):
    c.execute('SELECT * FROM athlete WHERE id = ?', (id,))
    athlete = c.fetchone()
    print('Registration complete:')
    print('------------------------------------------------')
    print('ID: ' + str(athlete[0]))
    print('Name: ' + str(athlete[1]))
    tp = ('SELECT id, name FROM training_plan WHERE id = ?')
    c.execute(tp, (athlete[3],))
    training_plan = c.fetchone()
    print('Training Plan: ' + str(training_plan[1]))
    print('Weight(kg): ' + str(athlete[2]))
    wc = ('SELECT id, name FROM weight_category WHERE id = ?')
    c.execute(wc, (athlete[4],))
    weight_category = c.fetchone()
    print('Weight Category: ' + str(weight_category[1])) 
    print('------------------------------------------------')
    print(' ')
    
    start()

   def find_athlete(athlete):
    print('Find Athlete...')
    print(' ')
    print('Please select an option from the menu below: ')
    print('1. Find Athlete by ID')
    print('2. Find Athlete by Name')
    print('3. Find Athlete by Weight')
    print('4. Find Athlete by Weight Category')
    print('5. Find Athlete by Training Plan')
    print('6. Find Athlete by Filtered Search')
    print(' ')
    print('M. Main Menu')
    print(' ')
    
    option = input('Please enter your option: ')
    if option == '1':
        Athlete.find_athlete_by_id(None)
    elif option == '2':
        Athlete.find_athlete_by_name()
    elif option == '3':
        Athlete.find_athlete_by_weight()
    elif option == '4':
        Athlete.find_athlete_by_weight_category()
    elif option == '5':
        Athlete.find_athlete_by_training_plan()
    elif option == '6':
        Athlete.find_athlete_by_filtered_search()
    elif option == 'M':
        start()
    else:
        print('Invalid option selected')
        Athlete.find_athlete()

   def find_athlete_by_id(athlete):
    if athlete is None:
        print(' ')
        print('Find Athlete...')
        print(' ')
        athlete = input('Please enter the Athlete ID:')
        c.execute('SELECT * FROM athlete WHERE id = ?', (athlete,))
        athlete = c.fetchone()
        Athlete.view_athlete(athlete)

   def find_athlete_by_name():
    print(' ')
    print('Find Athlete...')
    print(' ')
    name = input('Please enter the Athlete Name:')
    name = name.title()
    c.execute('SELECT * FROM athlete WHERE instr(name, ?)', (name,))
    results = c.fetchall()
    Athlete.athlete_search_results(results)

   def find_athlete_by_weight():
    print(' ')
    print('Find Athlete...')
    print(' ')
    weight = input('Please enter the Athlete Weight:')
    c.execute('SELECT * FROM athlete WHERE weight = ?', (weight,))
    results = c.fetchall()
    Athlete.athlete_search_results(results)

   def find_athlete_by_weight_category():
    print(' ')
    print('Find Athlete...')
    print(' ')
    print('Please select a weight category from the list below:')
    wc = ('SELECT * FROM weight_category')
    c.execute(wc)
    weight_category = c.fetchall()
    for weight_category in weight_category:
        print(str(weight_category[0]) + '. ' + str(weight_category[1]))
        print(' ')
    
    weight_category_id = input('Please enter the Weight Category Number: ')
    c.execute('SELECT * FROM athlete WHERE weight_category_id = ?', (weight_category_id,))
    results = c.fetchall()
    Athlete.athlete_search_results(results)

   def find_athlete_by_training_plan():
    print(' ')
    print('Find Athlete...')
    print(' ')
    print('Please select a training plan from the list below:') 
    tp = ('SELECT * FROM training_plan')
    c.execute(tp)
    training_plan = c.fetchall()
    for training_plan in training_plan:
        print(str(training_plan[0]) + '. ' + str(training_plan[1]))
        print(' ')
    
    training_plan_id = input('Please enter the Training Plan Number: ')
    c.execute('SELECT * FROM athlete WHERE training_plan_id = ?', (training_plan_id,))
    results = c.fetchall()
    Athlete.athlete_search_results(results)

   def find_athlete_by_filtered_search():
    print(' ')
    print('Find Athlete...')
    print(' ')
    print('If any of the following details are not known please enter 0: ') 
    name = input('Please enter the Athlete Name:')
    name = name.title()
    weight = input('Please enter the Athlete Weight():')
    tp = ('SELECT * FROM training_plan EXCEPT SELECT * FROM training_plan WHERE id = 0')
    c.execute(tp)
    training_plan = c.fetchall()
    for training_plan in training_plan:
        print(str(training_plan[0]) + '. ' + str(training_plan[1]))
        print(' ')
    training_plan = input('Please enter the Training Plan Number:')
    
    if name == '0' and weight == '0' and training_plan == '0':
        print(' ')
        print('Please enter at least one search criteria.')
        print(' ')
        Athlete.find_athlete_by_filtered_search()
    elif name == '0' and weight == '0':
        c.execute('SELECT * FROM athlete WHERE training_plan_id = ?', (training_plan,))
        results = c.fetchall()
        Athlete.athlete_search_results(results)
    elif name == '0' and training_plan == '0':
        c.execute('SELECT * FROM athlete WHERE weight = ?', (weight,))
        results = c.fetchall()
        Athlete.athlete_search_results(results)
    elif weight == '0' and training_plan == '0':
        c.execute('SELECT * FROM athlete WHERE instr(name, ?)', (name,))
        results = c.fetchall()
        Athlete.athlete_search_results(results)
    elif name == '0':
        c.execute('SELECT * FROM athlete WHERE weight = ? AND training_plan_id = ?', (weight, training_plan,))
        results = c.fetchall()
        Athlete.athlete_search_results(results)
    elif weight == '0':
        c.execute('SELECT * FROM athlete WHERE instr(name, ?) AND training_plan_id = ?', (name, training_plan,))
        results = c.fetchall()
        Athlete.athlete_search_results(results)
    elif training_plan == '0':
        c.execute('SELECT * FROM athlete WHERE instr(name, ?) AND weight = ?', (name, weight,))
        results = c.fetchall()
        Athlete.athlete_search_results(results)
    else: 
        c.execute('SELECT * FROM athlete WHERE instr(name, ?) AND weight = ? AND training_plan_id = ?', (name, weight, training_plan,))
        results = c.fetchall()
        Athlete.athlete_search_results(results)
        
   def athlete_search_results(results):
    if len(results) == 0:
        print(' ')
        print('No results found, Please try again.')
        print(' ')
        Athlete.find_athlete(None)
    else:
        print(' ')
        print('Search Results...')
        print(' ')
        for athlete in results:
            print(str(athlete[0]) + '. ' + str(athlete[1]))
            print('Weight(kg): ' + str(athlete[2]))

            tp = ('SELECT id, name FROM training_plan WHERE id = ?')
            c.execute(tp, (athlete[3],))
            training_plan = c.fetchone()
            print('Training Plan: ' + str(training_plan[1]))

            wc = ('SELECT id, name FROM weight_category WHERE id = ?')
            c.execute(wc, (athlete[4],))
            weight_category = c.fetchone()
            print('Weight Category: ' + str(weight_category[1]))
            print(' ')

        print('Please select an athlete from the list above: ')
        option = input('Please enter your option: ')
        c.execute('SELECT * FROM athlete WHERE id = ?', (option,))
        athlete = c.fetchone()
        Athlete.view_athlete(athlete)

   def view_athlete(athlete):
    if athlete is None:
        print(' ')
        print('Athlete not found, Please try again.')
        print(' ')
        Athlete.find_athlete(athlete)

    print(' ')
    print('Athlete ID: ' + str(athlete[0]))
    print('Name: ' + str(athlete[1]))

    tp = ('SELECT id, name FROM training_plan WHERE id = ?')
    c.execute(tp, (athlete[3],))
    training_plan = c.fetchone()
    print('Training Plan: ' + str(training_plan[1]))
    print('Weight(kg): ' + str(athlete[2]))

    wc = ('SELECT id, name FROM weight_category WHERE id = ?')
    c.execute(wc, (athlete[4],))
    weight_category = c.fetchone()
    print('Weight Category: ' + str(weight_category[1]))
    print(' ')
    print('Please select an option from the menu below:')

    invoice = c.execute('SELECT  * FROM invoice WHERE month = ? AND athlete_id = ?', (x.strftime("%B"), athlete[0],)).fetchone()

    if invoice is None:
        print('1. Create Invoice for ' + x.strftime("%B"))
    else:
        print('1. View Invoice for ' + x.strftime("%B"))
       
    print('2. Update Athlete')
    print(' ')
    print('M. Main Menu')
    print(' ')

    option = input('Please enter your option: ')

    if option == '1':
        if invoice is None:
            Invoice.create_invoice(athlete)
        else:
            Invoice.view_invoice(athlete, invoice)
    elif option == '2':
        Athlete.update_athlete(athlete)
    elif option == 'M':
        start()
    else:
        print('Invalid option selected')
        Athlete.find_athlete(athlete)
        
   def view_athletes():
    print(' ')
    print('Viewing All Athletes...')
    print(' ')
    athletes = c.execute('SELECT * FROM athlete').fetchall()
    for athlete in athletes:
        print(str(athlete[0]) + '. ' + str(athlete[1]))
        print('Weight(kg): ' + str(athlete[2]))

        tp = ('SELECT id, name FROM training_plan WHERE id = ?')
        c.execute(tp, (athlete[3],))
        training_plan = c.fetchone()
        print('Training Plan: ' + str(training_plan[1]))

        wc = ('SELECT id, name FROM weight_category WHERE id = ?')
        c.execute(wc, (athlete[4],))
        weight_category = c.fetchone()
        print('Weight Category: ' + str(weight_category[1]))
        print(' ')
        
    print('M. Main Menu')
    print(' ')
    print('Please select an athlete from the list above: ')
    option = input('Please enter your option: ')
    if option == 'M':
        start()
    else:
        c.execute('SELECT * FROM athlete WHERE id = ?', (option,))
        athlete = c.fetchone()
        Athlete.view_athlete(athlete)
   
   def update_athlete(athlete):
    print(' ')
    print('Update Athlete...')
    print(' ')
    print('Please select an option from the menu below:')
    print('1. Update Name')
    print('2. Update Weight')
    print('3. Update Training Plan')
    print(' ')
    print('M. Main Menu')
    print(' ')
    
    option = input('Please enter your option: ')
    if option == '1':
        Athlete.update_name(athlete)
    elif option == '2':
        Athlete.update_weight(athlete)
    elif option == '3':
        Athlete.update_training_plan(athlete)
    elif option == 'M':
        start()
    else:
        print('Invalid option selected')
        Athlete.update_athlete(athlete)
        
   def update_name(athlete):
    print(' ')
    name = input('Please enter the new name: ')
    print(' ')
    print('You have entered ' + str(name) + '.')
    print(' ')
    print('Is this correct?')
    print('1. Yes')
    print('2. No')
    print(' ')
    
    option = input('Please enter your option: ')
    if option == '1':
        c.execute('UPDATE athlete SET name = ? WHERE id = ?', (name, athlete[0]))
        conn.commit()
        print(' ')
        print('Name has been updated to ' + str(name) + '.')
        print(' ')
        c.execute('SELECT * FROM athlete WHERE id = ?', (athlete[0],))
        athlete = c.fetchone()
        Athlete.find_athlete(athlete)
    elif option == '2':
        Athlete.update_name(athlete)
    else:
        print('Invalid option selected')
        Athlete.update_name(athlete)
        
   def update_weight(athlete):
    print(' ')
    weight = int(input('Please enter the new weight: '))
    print(' ')
    print('You have entered ' + str(weight) + 'kg.')
    print(' ')
    print('Is this correct?')
    print('1. Yes')
    print('2. No')
    print(' ')
    
    option = input('Please enter your option: ')
    if option == '1':
        sql = ('SELECT id, upper_weight_limit FROM weight_category ORDER BY upper_weight_limit ASC')
        c.execute(sql)
        weight_category = c.fetchall()
        for weight_category in weight_category: 
            if int(weight) <= weight_category[1]:
                weight_category_id = weight_category[0]
                break
            
        c.execute('UPDATE athlete SET weight_category_id = ? WHERE id = ?', (weight_category_id, athlete[0]))
        conn.commit()
        c.execute('UPDATE athlete SET weight = ? WHERE id = ?', (weight, athlete[0]))
        conn.commit()
        print(' ')
        print('Weight has been updated to ' + str(weight) + 'kg.')
        print(' ')
        c.execute('SELECT * FROM athlete WHERE id = ?', (athlete[0],))
        athlete = c.fetchone()
        Athlete.view_athlete(athlete)
    elif option == '2':
        Athlete.update_weight(athlete)
    else:
        print('Invalid option selected')
        Athlete.update_weight(athlete)
        
   def update_training_plan(athlete):
    print(' ')
    print('Please select a training plan from the list below:')
    tp = ('SELECT * FROM training_plan EXCEPT SELECT * FROM training_plan WHERE id = 0')
    c.execute(tp)
    training_plan = c.fetchall()
    training_plan_range = len(training_plan)
    for training_plan in training_plan: 
        print(str(training_plan[0]) + '. ' + str(training_plan[1]))
        print('Cost per month: ' + u'\u00a3' + str(format(training_plan[2],".2f")))
        print('Cost per hour: ' + u'\u00a3' + str(format(training_plan[3],".2f")))
        print('Sessions per week: ' + str(training_plan[4]))
        print(' ')
    
    training_plan_id = input('Please Enter Training Plan Number: ')
    if training_plan_id.isnumeric():
        if int(training_plan_id) <= int(training_plan_range):
            tp = ('SELECT id, name FROM training_plan WHERE id = ?')
            c.execute(tp, (training_plan_id,))
            training_plan = c.fetchone()
            print(' ')
            print('You have selected ' + str(training_plan[1]) + ' training plan.')
            print(' ')
            print('Is this correct?')
            print('1. Yes')
            print('2. No')
            print(' ')
            option = input('Please enter your option: ')
        if option == '1':
            print(' ')
            print(str(training_plan[1]) + ' training plan' + ' has been assigned to ' + str(athlete[1]) + '.')
        elif option == '2':
            Athlete.update_training_plan(athlete)
        else:
            print('Invalid option selected')
            Athlete.update_training_plan(athlete)
    else:
        print(' ')
        print('Invalid training plan selected')
        print(' ')
        Athlete.update_training_plan(athlete)
    
    c.execute('UPDATE athlete SET training_plan_id = ? WHERE id = ?', (training_plan_id, athlete[0]))
    conn.commit()
    c.execute('SELECT * FROM athlete WHERE id = ?', (athlete[0],))
    athlete = c.fetchone()
    Athlete.view_athlete(athlete)
    
class TrainingPlan:

   def __init__(self, name, cost_per_month, cost_per_hour, sessions_per_week):
          self.name = name
          self.cost_per_month = cost_per_month
          self.cost_per_hour = cost_per_hour
          self.sessions_per_week = sessions_per_week
          
   def __str__(self):
        return f'Training Plan: {self.name}, {self.cost_per_month}, {self.cost_per_hour}, {self.sessions_per_week}'   

   def training_plan_menu():
    print(' ')
    print('Training Plan Menu...')
    print(' ')
    print('Please select an option from the menu below: ')
    print('1. Create Training Plan')
    print('2. View Training Plans')
    print(' ')
    print('M. Main Menu')
    print(' ')
    
    option = input('Please enter your option: ')
    if option == '1':
        TrainingPlan.create_training_plan()
    elif option == '2':
        TrainingPlan.view_training_plans()
    elif option == 'M':
        start()
    else:
        print('Invalid option selected')
        TrainingPlan.training_plan_menu()
        
   def create_training_plan():
    print(' ')
    print('Create a new training plan...')
    print('')
    print('Please enter the following details:')
    name = input('Training Plan Name: ')
    name = name.title()
    print(' ')
    print('You have entered ' + str(name) + '.') 
    print(' ')
    print('Is this correct?') 
    print('1. Yes')
    print('2. No')
    print(' ')
    option = input('Please enter your option: ')
    if option == '1':
        print(' ')
    elif option == '2':
        TrainingPlan.create_training_plan()
    else:
        print('Invalid option selected')
        TrainingPlan.create_training_plan()
        
    c.execute('INSERT INTO training_plan (name) VALUES (?)', (name,))
    conn.commit()
    
    id = c.lastrowid
    
    print(str(name) + ' has been created in the database with ID ' + str(id) + '.')
    print(' ')
    
    TrainingPlan.enter_cost_per_month(id, name)
    
   def enter_cost_per_month(id, name):
    print(' ')
    cost_per_month = float(input('Please enter the cost per month: '))
    print(' ')
    print('You have entered ' + u'\u00a3' + str(format(cost_per_month,".2f")) + '.')
    print(' ')
    print('Is this correct?')
    print('1. Yes')
    print('2. No')
    print(' ')
    
    option = input('Please enter your option: ')
    if option == '1':
         print(' ')
         print(u'\u00a3' + str(format(cost_per_month,".2f")) + ' has been assigned to ' + str(name) + '.')
         print(' ')
    elif option == '2':
         TrainingPlan.enter_cost_per_month(id, name)
    else:
         print('Invalid option selected')
         TrainingPlan.enter_cost_per_month(id, name)
    
    c.execute('UPDATE training_plan SET cost_per_month = ? WHERE id = ?', (cost_per_month, id))
    conn.commit()
    
    TrainingPlan.enter_cost_per_hour(id, name)
    
   def enter_cost_per_hour(id, name):
    print(' ')
    cost_per_hour = float(input('Please enter the cost per hour: '))
    print(' ')
    print('You have entered ' + u'\u00a3' + str(format(cost_per_hour,".2f")) + '.')
    print(' ')
    print('Is this correct?')
    print('1. Yes')
    print('2. No')
    print(' ')
    
    option = input('Please enter your option: ')
    if option == '1':
         print(' ')
         print(u'\u00a3' + str(format(cost_per_hour,".2f")) + ' has been assigned to ' + str(name) + '.')
         print(' ')
    elif option == '2':
         TrainingPlan.enter_cost_per_hour(id, name)
    else:
         print('Invalid option selected')
         TrainingPlan.enter_cost_per_hour(id, name)
    
    c.execute('UPDATE training_plan SET cost_per_hour = ? WHERE id = ?', (cost_per_hour, id))
    conn.commit()
    
    TrainingPlan.enter_sessions_per_week(id, name)
    
   def enter_sessions_per_week(id, name):
    print(' ')
    sessions_per_week = int(input('Please enter the sessions per week: '))
    print(' ')
    print('You have entered ' + str(sessions_per_week) + '.')
    print(' ')
    print('Is this correct?')
    print('1. Yes')
    print('2. No')
    print(' ')
    
    option = input('Please enter your option: ')
    if option == '1':
         print(' ')
         print(str(sessions_per_week) + ' has been assigned to ' + str(name) + '.')
         print(' ')
    elif option == '2':
         TrainingPlan.enter_sessions_per_week(id, name)
    else:
         print('Invalid option selected')
         TrainingPlan.enter_sessions_per_week(id, name)
    
    c.execute('UPDATE training_plan SET sessions_per_week = ? WHERE id = ?', (sessions_per_week, id))
    conn.commit()
    
    TrainingPlan.print_training_plan(id)
    
   def print_training_plan(id):
    c.execute('SELECT * FROM training_plan WHERE id = ?', (id,))
    training_plan = c.fetchone()
    print('Registration complete:')
    print('------------------------------------------------')
    print('ID: ' + str(training_plan[0]))
    print('Name: ' + str(training_plan[1]))
    print('Cost per month: ' + u'\u00a3' + str(format(training_plan[2],".2f")))
    print('Cost per hour: ' + u'\u00a3' + str(format(training_plan[3],".2f")))
    print('Sessions per week: ' + str(training_plan[4]))
    print('------------------------------------------------')
    print(' ')
    
    start()
 
   def view_training_plans():
    print(' ')
    print('Viewing All Training Plans...')
    print(' ')
    tp = ('SELECT * FROM training_plan')
    c.execute(tp)
    training_plan = c.fetchall()
    for training_plan in training_plan:
        print(str(training_plan[0]) + '. ' + str(training_plan[1]))
        print('Cost per month: ' + u'\u00a3' + str(format(training_plan[2],".2f")))
        print('Cost per hour: ' + u'\u00a3' + str(format(training_plan[3],".2f")))
        print('Sessions per week: ' + str(training_plan[4]))
        print(' ')
    
    print('M. Main Menu')
    print(' ')
    print('Please select a training plan from the list above.')
    option = input('Please enter your option: ')
    print(' ')
    if option == 'M':
        start()
    tp = ('SELECT id, name FROM training_plan WHERE id = ?')
    c.execute(tp, (option,))
    training_plan = c.fetchone()
    print('You have selected ' + str(training_plan[1]) + ' training plan.')
    print(' ')
    print('Please select an option from the menu below:')
    print('1. Update Cost per month')
    print('2. Update Cost per hour')
    print('3. Update Sessions per week')
    print(' ')
    print('M. Main Menu')
    print(' ')
    
    option = input('Please enter your option: ')
    if option == '1':
        TrainingPlan.update_cost_per_month(training_plan)
    elif option == '2':
        TrainingPlan.update_cost_per_hour(training_plan)
    elif option == '3':
        TrainingPlan.update_sessions_per_week(training_plan)
    elif option == 'M':
        start()
    else:
        print('Invalid option selected')
        TrainingPlan.view_training_plans()
        
   def update_cost_per_month(training_plan):
    print(' ')
    cost_per_month = float(input('Please enter the new cost per month: '))
    print(' ')
    print('You have entered ' + u'\u00a3' + str(format(cost_per_month,".2f")) + '.')
    print(' ')
    print('Is this correct?')
    print('1. Yes')
    print('2. No')
    print(' ')
    
    option = input('Please enter your option: ')
    if option == '1':
        c.execute('UPDATE training_plan SET cost_per_month = ? WHERE id = ?', (cost_per_month, training_plan[0]))
        conn.commit()
        print(' ')
        print('Cost per month has been updated to ' + u'\u00a3' + str(format(cost_per_month,".2f")) + '.')
        print(' ')
        TrainingPlan.view_training_plans()
    elif option == '2':
        TrainingPlan.update_cost_per_month(training_plan)
    else:
        print('Invalid option selected')
        TrainingPlan.update_cost_per_month(training_plan)
        
   def update_cost_per_hour(training_plan):
    print(' ')
    cost_per_hour = float(input('Please enter the new cost per hour: '))
    print(' ')
    print('You have entered ' + u'\u00a3' + str(format(cost_per_hour,".2f")) + '.')
    print(' ')
    print('Is this correct?')
    print('1. Yes')
    print('2. No')
    print(' ')
    
    option = input('Please enter your option: ')
    if option == '1':
        c.execute('UPDATE training_plan SET cost_per_hour = ? WHERE id = ?', (cost_per_hour, training_plan[0]))
        conn.commit()
        print(' ')
        print('Cost per hour has been updated to ' + u'\u00a3' + str(format(cost_per_hour,".2f")) + '.')
        print(' ')
        TrainingPlan.view_training_plans()
    elif option == '2':
        TrainingPlan.update_cost_per_hour(training_plan)
    else:
        print('Invalid option selected')
        TrainingPlan.update_cost_per_hour(training_plan)
        
   def update_sessions_per_week(training_plan):
    print(' ')
    sessions_per_week = int(input('Please enter the new sessions per week: '))
    print(' ')
    print('You have entered ' + str(sessions_per_week) + '.')
    print(' ')
    print('Is this correct?')
    print('1. Yes')
    print('2. No')
    print(' ')
    
    option = input('Please enter your option: ')
    if option == '1':
        c.execute('UPDATE training_plan SET sessions_per_week = ? WHERE id = ?', (sessions_per_week, training_plan[0]))
        conn.commit()
        print(' ')
        print('Sessions per week has been updated to ' + str(sessions_per_week) + '.')
        print(' ')
        TrainingPlan.view_training_plans()
    elif option == '2':
        TrainingPlan.update_sessions_per_week(training_plan)
    else:
        print('Invalid option selected')
        TrainingPlan.update_sessions_per_week(training_plan)
        
class WeightCategory:

   def __init__(self, name, upper_weight_limit):
          self.name = name
          self.upper_weight_limit = upper_weight_limit
          
   def __str__(self):
        return f'Weight Category: {self.name}, {self.upper_weight_limit}'
   
   def weight_category_menu():
    print(' ')
    print('Weight Category Menu...')
    print(' ')
    print('Please select an option from the menu below: ')
    print('1. Create Weight Category')
    print('2. View Weight Categories')
    print(' ')
    print('M. Main Menu')
    print(' ')
    
    option = input('Please enter your option: ')
    if option == '1':
        WeightCategory.create_weight_category()
    elif option == '2':
        WeightCategory.view_weight_categories()
    elif option == 'M':
        start()
    else:
        print('Invalid option selected')
        WeightCategory.weight_category_menu()
        
   def create_weight_category():
    print(' ')
    print('Create a new weight category...')
    print('')
    print('Please enter the following details:')
    name = input('Weight Category Name: ')
    name = name.title()
    print(' ')
    print('You have entered ' + str(name) + '.') 
    print(' ')
    print('Is this correct?') 
    print('1. Yes')
    print('2. No')
    print(' ')
    option = input('Please enter your option: ')
    if option == '1':
        print(' ')
    elif option == '2':
        WeightCategory.create_weight_category()
    else:
        print('Invalid option selected')
        WeightCategory.create_weight_category()
        
    c.execute('INSERT INTO weight_category (name) VALUES (?)', (name,))
    conn.commit()
    
    id = c.lastrowid
    
    print(str(name) + ' has been created in the database with ID ' + str(id) + '.')
    print(' ')
    
    WeightCategory.enter_upper_weight_limit(id, name)
    
   def enter_upper_weight_limit(id, name):
    print(' ')
    upper_weight_limit = int(input('Please enter the upper weight limit: '))
    print(' ')
    print('You have entered ' + str(upper_weight_limit) + '.')
    print(' ')
    print('Is this correct?')
    print('1. Yes')
    print('2. No')
    print(' ')
    
    option = input('Please enter your option: ')
    if option == '1':
         print(' ')
         print(str(upper_weight_limit) + ' has been assigned to ' + str(name) + '.')
         print(' ')
    elif option == '2':
         WeightCategory.enter_upper_weight_limit(id, name)
    else:
         print('Invalid option selected')
         WeightCategory.enter_upper_weight_limit(id, name)
    
    c.execute('UPDATE weight_category SET upper_weight_limit = ? WHERE id = ?', (upper_weight_limit, id))
    conn.commit()
    
    WeightCategory.print_weight_category(id)
    
   def print_weight_category(id):
    c.execute('SELECT * FROM weight_category WHERE id = ?', (id,))
    weight_category = c.fetchone()
    print('Registration complete:')
    print('------------------------------------------------')
    print('ID: ' + str(weight_category[0]))
    print('Name: ' + str(weight_category[1]))
    print('Upper Weight Limit: ' + str(weight_category[2]))
    print('------------------------------------------------')
    print(' ')
    
    start()
   
   def view_weight_categories():
    print(' ')
    print('Viewing All Weight Categories...')
    print(' ')
    wc = ('SELECT * FROM weight_category')
    c.execute(wc)
    weight_category = c.fetchall()
    for weight_category in weight_category:
        print(str(weight_category[0]) + '. ' + str(weight_category[1]))
        print('Upper Weight Limit: ' + str(weight_category[2]))
        print(' ')
    
    print('M. Main Menu')
    print(' ')
    print('Please select a weight category from the list above.')
    option = input('Please enter your option: ')
    print(' ')
    if option == 'M':
        start()
    wc = ('SELECT id, name FROM weight_category WHERE id = ?')
    c.execute(wc, (option,))
    weight_category = c.fetchone()
    print('You have selected ' + str(weight_category[1]) + ' weight category.')
    print(' ')
    print('Please select an option from the menu below:')
    print('1. Update Upper Weight Limit')
    print(' ')
    print('M. Main Menu')
    print(' ')
    
    option = input('Please enter your option: ')
    if option == '1':
        WeightCategory.update_upper_weight_limit(weight_category)
    elif option == 'M':
        start()
    else:
        print('Invalid option selected')
        WeightCategory.view_weight_categories()
        
   def update_upper_weight_limit(weight_category):
    print(' ')
    upper_weight_limit = int(input('Please enter the new upper weight limit: '))
    print(' ')
    print('You have entered ' + str(upper_weight_limit) + '.')
    print(' ')
    print('Is this correct?')
    print('1. Yes')
    print('2. No')
    print(' ')
    
    option = input('Please enter your option: ')
    if option == '1':
        c.execute('UPDATE weight_category SET upper_weight_limit = ? WHERE id = ?', (upper_weight_limit, weight_category[0]))
        conn.commit()
        print(' ')
        print('Upper weight limit has been updated to ' + str(upper_weight_limit) + '.')
        print(' ')
        WeightCategory.view_weight_categories()
    elif option == '2':
        WeightCategory.update_upper_weight_limit(weight_category)
    else:
        print('Invalid option selected')
        WeightCategory.update_upper_weight_limit(weight_category)
    
class Competition:

   def __init__(self, name, date, price):
          self.name = name
          self.date = date
          self.price = price
          
   def __str__(self):
        return f'Competition: {self.name}, {self.date}, {self.price}'
   
   def competition_menu():
    print(' ')
    print('Competition Menu...')
    print(' ')
    print('Please select an option from the menu below: ')
    print('1. Create Competitions')
    print('2. View Competitions')
    print(' ')
    print('M. Main Menu')
    print(' ')
    
    option = input('Please enter your option: ')
    print(' ')
    if option == '1':
        year = int(input('Please enter the year for new competitions: '))
        print(' ')
        sql = ('SELECT * FROM competition WHERE year = ?')
        c.execute(sql, (year,))
        results = c.fetchall()
        if len(results) == 0:
            Competition.create_competitions(year)
            
        else:
            print(' ')
            print('Competitions for ' + str(year) + ' have already been created.')
            Competition.competition_menu()
        Competition.create_competitions(year)
    elif option == '2':
        Competition.view_competitions()
    elif option == 'M':
        start()
    else:
        print('Invalid option selected')
        Competition.competition_menu()
   
   def view_competitions():
    print(' ')
    print('Viewing All Competitions...')
    print(' ')
    c.execute('SELECT * FROM competition')
    competitions = c.fetchall()
    for competition in competitions:
        print(str(competition[0]) + '. Saturday, ' + str(competition[1]) + '/' + str(competition[2]) + '/' + str(competition[3]))
        print('Price: ' + u'\u00a3' + str(format(competition[4],".2f")))
        print(' ')
    
    print('M. Main Menu')
    print('C. Create Competitions')
    print(' ')
    option = input('Please enter your option from the list above: ')
    print(' ')
    if option == 'M':
        start()
    elif option == 'C':
        year = int(input('Please enter the year for new competitions: '))
        Competition.create_competitions(year) 
    c.execute('SELECT * FROM competition WHERE id = ?', (option,))
    competition = c.fetchone()
    print('You have selected Saturday, ' + str(competition[1]) + '/' + str(competition[2]) + '/' + str(competition[3]) + ' competition.')
    print(' ')
    print('Registrations start on the 1st of each month and are only open for the competition that month.')
    print('To register an athlete, please invoice the athlete and select "yes" to the competiton option.')
    print(' ')
    print('Please select an option from the menu below:')
    print('1. Update Price')
    print('2. Register Athlete')
    print(' ')
    print('M. Main Menu')
    print(' ')
    
    option = input('Please enter your option: ')
    if option == '1':
        Competition.update_price(competition)
    elif option == '2':
        Athlete.find_athlete(None)
    elif option == 'M':
        start()
    else:
        print('Invalid option selected')
        Competition.view_competitions()
        
   def update_price(competition):
    print(' ')
    price = float(input('Please enter the new price: '))
    print(' ')
    print('You have entered ' + u'\u00a3' + str(format(price,".2f")) + '.')
    print(' ')
    print('Is this correct?')
    print('1. Yes')
    print('2. No')
    print(' ')
    
    option = input('Please enter your option: ')
    if option == '1':
        c.execute('UPDATE competition SET price = ? WHERE id = ?', (price, competition[0]))
        conn.commit()
        print(' ')
        print('Price has been updated to ' + u'\u00a3' + str(format(price,".2f")) + '.')
        print(' ')
        Competition.view_competitions()
    elif option == '2':
        Competition.update_price(competition)
    else:
        print('Invalid option selected')
        Competition.update_price(competition)
   
   def create_competitions(year):
    for month in range (1, 13):
       cal = calendar.monthcalendar(year, month)
       weekone = cal[0]
       weektwo = cal[1]
       weekthree = cal[2]
        
       if weekone[calendar.SATURDAY]:
           saturday = weektwo[calendar.SATURDAY]
           c.execute('INSERT INTO competition (day, month, year) VALUES (?, ?, ?)', (saturday, month, year))
           conn.commit()      
       else:
           saturday = weekthree[calendar.SATURDAY]
           c.execute('INSERT INTO competition (day, month, year) VALUES (?, ?, ?)', (saturday, month, year))
           conn.commit()
           
    print(' ')
    print('Competitions for ' + str(year) + ' have been created.')
    print(' ')
    
    start()

class Invoice:

   def __init__(self, name, date, amount, athlete_id):
          self.name = name
          self.date = date
          self.amount = amount
          self.athlete_id = athlete_id
          
   def __str__(self):
        return f'Invoice: {self.name}, {self.date}, {self.amount}, {self.athlete_id}'
  
   def invoice_menu():
    print(' ')
    print('Invoice Menu...')
    print(' ')
    print('Please select an option from the menu below:')
    print('1. View Invoice by ID')
    print('2. View Invoices by Athlete')
    print('3. View Invoices by Month')
    print('4. View Invoices by Year')
    print('5. View All Invoices')
    print(' ')
    print('M. Main Menu')
    print(' ')
    
    option = input('Please enter your option: ')
    print(' ')
    if option == '1':
        Invoice.view_invoice_by_id()
    elif option == '2':
        Invoice.view_invoices_by_athlete()
    elif option == '3':
        Invoice.view_invoices_by_month()
    elif option == '4':
        Invoice.view_invoices_by_year()
    elif option == '5':
        Invoice.view_all_invoices()
    elif option == 'M':
        start()
    else:
        print('Invalid option selected')
        Invoice.invoice_menu()
   
   def view_invoice_by_id():
    print(' ')
    id = input('Please enter the Invoice ID: ')
    print(' ')
    c.execute('SELECT * FROM invoice WHERE id = ?', (id,))
    invoice = c.fetchone()
    if invoice is None:
        print('Invoice not found!')
        Invoice.invoice_menu()
    else:
        athlete = invoice[1]
        Invoice.view_invoice(athlete, invoice)
    
    print('M. Main Menu')
    print(' ')
    option = input('Please enter your option: ')
    print(' ')
    if option == 'M':
        start()
    else:
        print('Invalid option selected')
        Invoice.view_invoice_by_id()
   
        
   def view_all_invoices():
    print(' ')
    print('Viewing All Invoices...')
    print(' ')
    c.execute('SELECT * FROM invoice')
    invoices = c.fetchall()
    for invoice in invoices:
        athlete = invoice[1]
        Invoice.view_invoice(athlete, invoice)
        print(' ')
    
    print('M. Main Menu')
    print(' ')
    option = input('Please enter your option: ')
    print(' ')
    if option == 'M':
        start()
    else:
        print('Invalid option selected')
        Invoice.view_all_invoices()
        
   def view_invoices_by_athlete():
    print(' ')
    athlete = input('Please enter the Athlete ID: ')
    print(' ')
    c.execute('SELECT * FROM invoice WHERE athlete_id = ?', (athlete,))
    invoices = c.fetchall()
    for invoice in invoices:
        Invoice.view_invoice(athlete, invoice)
    
    print('M. Main Menu')
    print(' ')
    option = input('Please enter your option: ')
    print(' ')
    if option == 'M':
        start()
    else:
        print('Invalid option selected')
        Invoice.view_invoices_by_athlete()
        
   def view_invoices_by_month():
    print(' ')
    month = input('Please enter the month number: ')
    month = calendar.month_name[int(month)]
    print(' ')
    c.execute('SELECT * FROM invoice WHERE month = ?', (month,))
    invoices = c.fetchall()
    for invoice in invoices:
        athlete = invoice[1]
        Invoice.view_invoice(athlete, invoice)
        print(' ')
    
    print('M. Main Menu')
    print(' ')
    option = input('Please enter your option: ')
    print(' ')
    if option == 'M':
        start()
    else:
        print('Invalid option selected')
        Invoice.view_invoices_by_month()
        
   def view_invoices_by_year():
    print(' ')
    year = input('Please enter the year number: ')
    print(' ')
    c.execute('SELECT * FROM invoice WHERE year = ?', (year,))
    invoices = c.fetchall()
    for invoice in invoices:
        athlete = invoice[1]
        Invoice.view_invoice(athlete, invoice)
        print(' ')
    
    print('M. Main Menu')
    print(' ')
    option = input('Please enter your option: ')
    print(' ')
    if option == 'M':
        start()
    else:
        print('Invalid option selected')
        Invoice.view_invoices_by_year()
     
   def create_invoice(athlete):
    c.execute('SELECT * FROM training_plan WHERE id = ?', (athlete[3],))
    training_plan = c.fetchone()
    amount = training_plan[2]
    print(' ')
    print('Create ' + x.strftime("%B") + ' invoice for ' +  str(athlete[1]) + '...')
    print(' ')
    print('Please enter number of private sessions in ' + x.strftime("%B"))
    print('Maximum of 5 sessions per month')
    print(' ')
    sessions = int(input('Number of sessions: '))
    print(' ')
    print('You have entered ' + str(sessions) + ' sessions.')
    print(' ')
    print('Is this correct?')
    print('1. Yes')
    print('2. No')
    print(' ')
    
    option = input('Please enter your option: ')
    if option == '1':
        if sessions <= 5:
            c.execute('SELECT * FROM training_plan WHERE id = 0')
            training_plan = c.fetchone()
            amount = amount + (sessions * training_plan[3])
            print(' ')
            if athlete[3] > 1:
                print('Has ' + str(athlete[1]) + ' entered ' + x.strftime("%B") + "'s " + 'competition')
                print('1. Yes')
                print('2. No')
                print(' ')
                option = input('Please enter your option: ')
                if option == '1':
                    sql = ('SELECT * FROM competition WHERE month = ?')
                    c.execute(sql, (x.strftime("%#m"),))
                    competition = c.fetchone()
                    c.execute('INSERT INTO competition_athlete (competition_id, athlete_id) VALUES (?, ?)', (competition[0], athlete[0]))
                    conn.commit()
                    print(' ')
                    amount = amount + competition[4]
                    wc = ('SELECT name FROM weight_category WHERE id = ?')
                    c.execute(wc, (athlete[4],))
                    weight_category = c.fetchone()
                    tp = ('SELECT *, sessions_per_week FROM training_plan WHERE id = ?')
                    c.execute(tp, (athlete[3],))
                    training_plan = c.fetchone()
                    tp_name = training_plan[1]
                    sessions_per_week = training_plan[4]
                    cost_per_month = training_plan[2]
                    ps = ('SELECT * FROM training_plan WHERE id = 0')
                    c.execute(ps)
                    ps = c.fetchone()
                    cost_per_hour = ps[3]
                    private_session_total = sessions * cost_per_hour
                    competition_cost = competition[4]
                    month = x.strftime("%B")
                    year = x.strftime("%Y")
                    c.execute('INSERT INTO invoice (athlete_id, name, weight, weight_category, training_plan, sessions_per_week, training_plan_cost, private_sessions, private_session_cost, private_session_total, competition_id, competition_cost, total, month, year) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (athlete[0], athlete[1], athlete[2], weight_category[0], tp_name, sessions_per_week, cost_per_month, sessions, cost_per_hour, private_session_total, competition[0], competition_cost, amount, month, year))
                    conn.commit()
                    c.execute('SELECT * FROM invoice WHERE id = ?', (c.lastrowid,))
                    invoice = c.fetchone()
                    print(x.strftime("%B") + "'s" + ' invoice has been created for ' + str(athlete[1]) + '.')
                    print(' ')
                    Invoice.view_invoice(athlete, invoice)
                    print(' ')
                    print('Please select an option from the menu below:')
                    print('M. Main Menu')
                    print(' ')
                    option = input('Please enter your option: ')
                    print(' ')
                    if option == 'M':
                        start()
                elif option == '2':
                    wc = ('SELECT name FROM weight_category WHERE id = ?')
                    c.execute(wc, (athlete[4],))
                    weight_category = c.fetchone()
                    tp = ('SELECT *, sessions_per_week FROM training_plan WHERE id = ?')
                    c.execute(tp, (athlete[3],))
                    training_plan = c.fetchone()
                    tp_name = training_plan[1]
                    sessions_per_week = training_plan[4]
                    cost_per_month = training_plan[2]
                    ps = ('SELECT * FROM training_plan WHERE id = 0')
                    c.execute(ps)
                    ps = c.fetchone()
                    cost_per_hour = ps[3]
                    private_session_total = sessions * cost_per_hour
                    month = x.strftime("%B")
                    year = x.strftime("%Y")
                    c.execute('INSERT INTO invoice (athlete_id, name, weight, weight_category, training_plan, sessions_per_week, training_plan_cost, private_sessions, private_session_cost, private_session_total, total, month, year) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (athlete[0], athlete[1], athlete[2], weight_category[0], tp_name, sessions_per_week, cost_per_month, sessions, cost_per_hour, private_session_total, amount, month, year))                    
                    conn.commit()
                    c.execute('SELECT * FROM invoice WHERE id = ?', (c.lastrowid,))
                    invoice = c.fetchone()
                    print(x.strftime("%B") + "'s" + ' invoice has been created for ' + str(athlete[1]) + '.')
                    print(' ')
                    Invoice.view_invoice(athlete, invoice)
                    print(' ')
                    print('Please select an option from the menu below:')
                    print('M. Main Menu')
                    print(' ')
                    option = input('Please enter your option: ')
                    print(' ')
                    if option == 'M':
                        start()
                    else:
                        print('Invalid option selected')
                        Invoice.view_invoice(athlete, invoice)
                else:
                    print('Invalid option selected')
                    Invoice.create_invoice(athlete)
            else:
                wc = ('SELECT name FROM weight_category WHERE id = ?')
                c.execute(wc, (athlete[4],))
                weight_category = c.fetchone()
                tp = ('SELECT *, sessions_per_week FROM training_plan WHERE id = ?')
                c.execute(tp, (athlete[3],))
                training_plan = c.fetchone()
                tp_name = training_plan[1]
                sessions_per_week = training_plan[4]
                cost_per_month = training_plan[2]
                ps = ('SELECT * FROM training_plan WHERE id = 0')
                c.execute(ps)
                ps = c.fetchone()
                cost_per_hour = ps[3]
                private_session_total = sessions * cost_per_hour
                month = x.strftime("%B")
                year = x.strftime("%Y")
                c.execute('INSERT INTO invoice (athlete_id, name, weight, weight_category, training_plan, sessions_per_week, training_plan_cost, private_sessions, private_session_cost, private_session_total, total, month, year) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (athlete[0], athlete[1], athlete[2], weight_category[0], tp_name, sessions_per_week, cost_per_month, sessions, cost_per_hour, private_session_total, amount, month, year))
                conn.commit()
                c.execute('SELECT * FROM invoice WHERE id = ?', (c.lastrowid,))
                invoice = c.fetchone()
                print(x.strftime("%B") + "'s" + ' invoice has been created for ' + str(athlete[1]) + '.')
                print(' ')
                Invoice.view_invoice(athlete, invoice)
                print(' ')
                print('Please select an option from the menu below:')
                print('M. Main Menu')
                print(' ')
                option = input('Please enter your option: ')
                print(' ')
                if option == 'M':
                    start()
                else:
                    print('Invalid option selected')
                    Invoice.view_invoice(athlete, invoice)
        else:
            print('Invalid number of sessions entered, Please try again.')
            print(' ')
            Invoice.create_invoice(athlete)
    elif option == '2':
        Invoice.create_invoice(athlete)
    else:
        print('Invalid option selected')
        Invoice.create_invoice(athlete)
        
   def view_invoice(athlete, invoice):
    print('------------------------------------------------')
    print('Invoice ID: ' + str(invoice[0]))
    print('Invoice Date: ' + str(invoice[14]) + ' ' + str(invoice[15]))
    print('Athlete ID: ' + str(invoice[1]))
    print('Name: ' + str(invoice[2]))
    print('Weight(kg): ' + str(invoice[3]))
    print('Weight Category: ' + str(invoice[4]))
    print('Training Plan: ' + str(invoice[5]))
    print('Sessions per week: ' + str(invoice[6]))
    print('Traing Plan Cost(per month): ' + u'\u00a3' + str(format(invoice[7],".2f")))
    print('Private Session(hours): ' + str(invoice[8]))
    print('Private Session Cost(per hour): ' + u'\u00a3' + str(format(invoice[9],".2f")))
    print('Private Session Total: ' + u'\u00a3' + str(format(invoice[8] * invoice[9],".2f")))
    
    if invoice[11] != 0:
     print('Competition ID: ' + str(invoice[11]))
     c.execute('SELECT * FROM competition WHERE id = ?', (invoice[11],))
     competition = c.fetchone()
     print('Competition Date: ' + str(competition[1]) + '/' + str(competition[2]) + '/' + str(competition[3]))
     print('Competition Cost: ' + u'\u00a3' + str(format(invoice[12],".2f")))
     
    print('Invoice Total: ' + u'\u00a3' + str(format(invoice[13],".2f")))
    print('------------------------------------------------')
    
    start()

def start():
    if c.execute('SELECT * FROM athlete').fetchone() is None:
        count = 0
        name = ['Luke Littler', 'John Smith', 'Jane Doe', 'Bob Jones', 'Sally Smith', 'Jack Doe', 'Jill Jones', 'Tom Smith', 'Tina', 'Lucy', 'Peter Jones', 'Keelee Burke', 'Casey Holland', 'Teighan Donnely']
        weight = [60, 66, 71, 73, 78, 81, 85, 90, 93, 100, 635]
        training_plan_id = [1, 2, 3]
        weight_category_id = [1, 2, 3, 4, 5, 6]

        while count < 100:
            count = count + 1
            name.append(random.choice(name))
            weight.append(random.randint(66, 635))
            training_plan_id.append(random.randint(1, 3))
            weight_category_id.append(random.randint(1, 6))
            c.execute('INSERT INTO athlete (name, weight, training_plan_id, weight_category_id) VALUES (?, ?, ?, ?)', (name[count], weight[count], training_plan_id[count], weight_category_id[count]))
            conn.commit()

    option = 0
    athlete = None

    print('North Sussex Judo Club')
    print(' ')
    print('Please select an option from the menu below:')
    print('1. Athlete Menu')
    print('2. Training Plan Menu')
    print('3. Weight Category Menu')
    print('4. Competition Menu')
    print('5. Invoice Menu')
    print(' ')
    print('E. Exit')
    print(' ')

    option = input('Please enter your option: ')

    if option == '1':
        Athlete.athlete_menu()
    elif option == '2':
        TrainingPlan.training_plan_menu()
    elif option == '3':
        WeightCategory.weight_category_menu()
    elif option == '4':
        Competition.competition_menu()
    elif option == '5':
        Invoice.invoice_menu()
    elif option == 'E':
        print(' ')
        print('Thank you for using North Sussex Judo Club')
        print(' ')
        exit()
    else:
        print('Invalid option selected')
        print(' ')
        start()

if c.execute('SELECT * FROM competition').fetchone() is None:
    year = int(x.strftime("%Y"))
    Competition.create_competitions(year)
    start()

start()