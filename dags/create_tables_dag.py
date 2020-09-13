from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator

import os


default_args = {
    'owner': 'udacity',
    'start_date': datetime(2019, 1, 12),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),  
    'email_on_failure': False,
    'email_on_retry': False,    
}

dag = DAG('create_tables_dag',
          default_args=default_args,
          description='Create Staging, Fact and Dimension Tables in Redshift',
          schedule_interval='@once',
          catchup=False)

create_tables_task = PostgresOperator(
  task_id="create_tables",
  dag=dag,
  sql='create_tables.sql',
  postgres_conn_id="redshift"
)

create_tables_task
