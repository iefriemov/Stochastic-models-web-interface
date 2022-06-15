import datetime
import pendulum
from dateutil.relativedelta import relativedelta

import requests
import pandas as pd
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.edgemodifier import Label

@dag(
    schedule_interval="@monthly",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
)
def Etl():
    
    truncate_meta = PostgresOperator(
        task_id="truncate_meta",
        postgres_conn_id="main_pg_conn",
        sql="""
            DELETE FROM last_update_treasury;
            """,
    )
    
    truncate_staging = PostgresOperator(
        task_id="truncate_staging",
        postgres_conn_id="main_pg_conn",
        sql="""
            DELETE FROM Treasury_Staging;
            """,
    )
    update_meta = PostgresOperator(
        task_id="update_meta",
        postgres_conn_id="main_pg_conn",
        sql="""
            INSERT INTO last_update_treasury(record_date)
            SELECT MAX(record_date) 
            FROM Treasury_Staging;
            """,
    )
    
    insert_into_Treasury = PostgresOperator(
        task_id="insert_into_Treasury",
        postgres_conn_id="main_pg_conn",
        sql="""
            INSERT INTO Treasury_Bills(record_date, avg_interest_rate_amt)
            SELECT record_date, avg_interest_rate_amt
            FROM Treasury_Staging
            ORDER BY record_date ASC;
            """,
    )
    @task
    def get_last_update(**context):
        postgres_hook = PostgresHook(postgres_conn_id="main_pg_conn")
        conn = postgres_hook.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT record_date FROM last_update_treasury;")
        conn.commit()        

        reference_date = cur.fetchone()
        task_instance = context['task_instance']
        task_instance.xcom_push(key="my_value", value=str(reference_date[0]))
        
    @task
    def get_data(**context):
        postgres_hook = PostgresHook(postgres_conn_id="main_pg_conn")
        conn = postgres_hook.get_conn()
        cur = conn.cursor()
                
        reference_date = context['task_instance'].xcom_pull(key='my_value', task_ids='get_last_update')

        
        url = f'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/avg_interest_rates?fields=avg_interest_rate_amt,%20record_date&filter=record_date:gte:{reference_date},security_type_desc:eq:Marketable,security_desc:eq:Treasury%20Bills'

        response = requests.request("GET", url).json()
        
        insert_sql = """INSERT INTO Treasury_Staging (avg_interest_rate_amt, record_date) VALUES(%s, %s)"""

        for record in response['data']:
            cur.execute(insert_sql, [record["avg_interest_rate_amt"], record["record_date"]])
        
        conn.commit()  
        task_instance = context['task_instance']
        task_instance.xcom_push(key="updated", value=(response['data'] == []))
        
    @task
    def updated(**context):
        updated = context['task_instance'].xcom_pull(key='updated', task_ids='get_data')
        if not updated:
            return 'yes'
        return 'End'
    
    yes = DummyOperator(task_id='yes')

    End = DummyOperator(task_id='End')

    get_last_update() >> get_data() >> updated() >> [yes, End]
    yes >> [truncate_meta, insert_into_Treasury] >> update_meta >> truncate_staging >> End

dag = Etl()