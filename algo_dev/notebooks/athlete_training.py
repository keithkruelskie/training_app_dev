import pandas as pd
import numpy as np
from sqlalchemy import create_engine, insert, update, MetaData
import os
from dotenv import load_dotenv
import json
import datetime

def get_next_workout_id():
    '''
    Returns the next workout id from the database
    '''
    
    if not db:
        print("No db connection.")
    
    query = '''
    SELECT MAX (workout_id)
    FROM athlete.workouts
    '''
    
    return int(pd.read_sql(query, db)['max']+1)

def get_table_columns(schema, table_name):
    '''
    Returns the columns for a given schema and table name from the attached
    postgresql server.
    '''
    
    table_query = f"""
    SELECT *
    FROM {schema}.{table_name}
    WHERE 1 = 0
    ;
    """
    return list(pd.read_sql(table_query, db).columns)

def create_workout(athlete_id, date, params):
    '''
    This creates a single workout for a single date for an athlete, with the 
    characteristics defined in the params. 
    Params can be a dict type for ease of reference 
    '''
    
    #First define the insert string:
    ins = workouts_table.insert().values(get_table_columns('athlete', 'workouts'))
    
    #Starting point for a workout:
    this_workout = {'workout_id': -1,
                 'int_workout': False,
                 'workout_dur': 0.0,
                 'workout_itv_dur': 0.0,
                 'workout_prop_dur': 0.0,
                 'steps': {0},
                 'FK_athlete_id': -1,
                 'workout_date': '01/01/1901'}
    
    #Map the params values to the columns inserting into, that match:
    this_workout = {key: params.get(key, this_workout[key]) for key in this_workout}
    this_workout['FK_athlete_id'] = athlete_id
    this_workout['workout_date'] = date
    this_workout['workout_id'] = get_next_workout_id()
    
    db.execute(ins, this_workout)
    
def update_workout(workout_id, new_params):
    
    stmt = (
    update(workouts_table).
    where(workouts_table.c.workout_id == workout_id).
    values(new_params)
    )
    
    #And execute:
    db.execute(stmt)
    
#Import environment variables:
user = os.getenv('TEST_DB_USER')
password = os.getenv('TEST_DB_PW')

#Create a connection to the PostgreSQL db:
db = create_engine(f"postgresql://{user}:{password}@localhost:5432/postgres")

#Attaching to meta data
athlete_meta = MetaData(db)

#access the athlete schema, where our table is stored:
athlete_meta.reflect(bind=db, schema='athlete')

workouts_table = athlete_meta.tables['athlete.workouts']