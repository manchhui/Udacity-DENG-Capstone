from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperatorCAP, LoadFactOperatorCAP,
                               LoadDimensionOperatorCAP, DataQualityOperatorCAP)
from helpers import SqlQueries

default_args = {
    'owner': 'udacity',
    'start_date': datetime(2019, 1, 12),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),  
    'email_on_failure': False,
    'email_on_retry': False
}

dag = DAG('udac_capstone_dag',
          default_args=default_args,
          description='Extract, Load and Tranfer data with Spark Cluster with Airflow',
          schedule_interval='0 7 * * *',
          catchup=False)

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

stage_users_to_redshift = StageToRedshiftOperatorCAP(
    task_id='Stage_users',
    dag=dag,
    table="staging_users",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="udacity-capstone-project-828",
    s3_key="users",
    region="us-west-2",
    format_type="csv"
)

stage_books_to_redshift = StageToRedshiftOperatorCAP(
    task_id='Stage_books',
    dag=dag,
    table="staging_books",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="udacity-capstone-project-828",
    s3_key="books",
    region="us-west-2",
    format_type="csv"
)

stage_ratings_to_redshift = StageToRedshiftOperatorCAP(
    task_id='Stage_ratings',
    dag=dag,
    table="staging_ratings",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="udacity-capstone-project-828",
    s3_key="ratings",
    region="us-west-2",
    format_type="s3://udacity-capstone-project-828/jsonpaths.json"
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator >> [stage_users_to_redshift,
                  stage_books_to_redshift,
                  stage_ratings_to_redshift] >> end_operator
