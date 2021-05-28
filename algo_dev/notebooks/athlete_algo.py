from athlete_training import DATA_CRUD
import numpy as np
import pandas as pd

# class ALGO():

#     def __init__(self, athlete_id) -> None:

        

#         self.athlete_id = athlete_id
#         #self.hr = 
#         pass

#     def get_athlete_data(self, athlete_id):
#         #Do some work with the data to prepare it
#         print(get_athlete_info)
    
#     def create_workouts(self):
#         #Takes the athlete data, creates workouts
    
#My_Algo = ALGO(1)
#My_Algo.get_athlete_data()
print("Hello World")
my_crud = DATA_CRUD(1)

#Testing number 1
print(my_crud.athlete_id)
print(my_crud.get_athlete_info())

#Testing another
roberto_crud = DATA_CRUD(2)
print(roberto_crud.get_athlete_info()['first_name'][0])