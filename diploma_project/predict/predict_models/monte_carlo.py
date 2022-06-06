import configparser


config_file = configparser.ConfigParser()

# ADD SECTION
config_file.add_section("PostgreSettings")
# ADD SETTINGS TO SECTION
config_file.set("PostgreSettings", "database", "airflow")
config_file.set("PostgreSettings", "user", "airflow")
config_file.set("PostgreSettings", "password", "airflow")
config_file.set("PostgreSettings", "host", "5432")

# SAVE CONFIG FILE
with open(r"configurations_database.ini", 'w') as configfileObj:
    config_file.write(configfileObj)
    configfileObj.flush()
    configfileObj.close()


        
        
        
        
        

