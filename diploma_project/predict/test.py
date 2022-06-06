import configparser
import psycopg2

config = configparser.ConfigParser()
config.read('configurations_database.ini')

conn = psycopg2.connect(
                        dbname=config['PostgreSettings']['database'], 
                        user=config['PostgreSettings']['user'], 
                        password=config['PostgreSettings']['password'],
                        host='127.0.0.1'
                        )
#0.0.0.0:5432->5432/tcp
cursor = conn.cursor()
#cursor.execute('SELECT * FROM airport LIMIT 10')
#records = cursor.fetchall()

cursor.close()
conn.close()