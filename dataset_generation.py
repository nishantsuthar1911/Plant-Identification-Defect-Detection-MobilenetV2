from settings import BASE_DIR, INFECTION_DIR, IS_INFECTED_DIR, PLANT_DIR, EXCEL_PATH

import pandas as pd
import shutil
import os
df = pd.read_excel(EXCEL_PATH)

df.columns = ['base', 'Plant', 'Infection', 'new_infection', 'is_healthy']

plant_dict = dict(zip(list(df['base']),list(df['Plant'])))
infection_dict = dict(zip(list(df['base']),list(df['new_infection'])))
is_healthy_dict = dict(zip(list(df['base']),list(df['is_healthy'])))


for key in plant_dict.keys():
    target_path_plant = os.path.join(PLANT_DIR,str(plant_dict[key]))
    target_path_infection = os.path.join(INFECTION_DIR,str(infection_dict[key]))
    target_path_is_infection = os.path.join(IS_INFECTED_DIR,str(is_healthy_dict[key]))
    if not os.path.exists(target_path_infection):
        os.mkdir(target_path_infection)
    if not os.path.exists(target_path_plant):
        os.mkdir(target_path_plant)
    if not os.path.exists(target_path_is_infection):
        os.mkdir(target_path_is_infection)
    for file_name in os.listdir(os.path.join(BASE_DIR,key)):
        shutil.copyfile(os.path.join(BASE_DIR,key,file_name),os.path.join(target_path_plant,file_name))
        shutil.copyfile(os.path.join(BASE_DIR,key,file_name),os.path.join(target_path_infection,file_name))
        shutil.copyfile(os.path.join(BASE_DIR,key,file_name),os.path.join(target_path_is_infection,file_name))



