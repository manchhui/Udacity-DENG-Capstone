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

load_ratings_table = LoadFactOperatorCAP(
    task_id='Load_ratings_fact_table',
    dag=dag,
    redshift_conn_id="redshift",
    sql="ratings_table_insert"
)

load_users_table = LoadDimensionOperatorCAP(
    task_id='Load_users_dim_table',
    dag=dag,
    table="users",
    redshift_conn_id="redshift",
    sql="users_table_insert",
    append_mode="False"
)

load_yearofpub_table = LoadDimensionOperatorCAP(
    task_id='Load_yearofpub_dim_table',
    dag=dag,
    table="yearofpub",
    redshift_conn_id="redshift",
    sql="yearofpub_table_insert",
    append_mode="False"
)

load_authors_table = LoadDimensionOperatorCAP(
    task_id='Load_authors_dim_table',
    dag=dag,
    table="authors",
    redshift_conn_id="redshift",
    sql="authors_table_insert",
    append_mode="False"
)

load_books_author_table = LoadDimensionOperatorCAP(
    task_id='Load_books_author_dim_table',
    dag=dag,
    table="books_author",
    redshift_conn_id="redshift",
    sql="books_author_table_insert",
    append_mode="False"
)

load_titles_table = LoadDimensionOperatorCAP(
    task_id='Load_titles_dim_table',
    dag=dag,
    table="titles",
    redshift_conn_id="redshift",
    sql="titles_table_insert",
    append_mode="False"
)

load_books_title_table = LoadDimensionOperatorCAP(
    task_id='Load_books_title_dim_table',
    dag=dag,
    table="books_title",
    redshift_conn_id="redshift",
    sql="books_title_table_insert",
    append_mode="False"
)

load_publishers_table = LoadDimensionOperatorCAP(
    task_id='Load_publishers_dim_table',
    dag=dag,
    table="publishers",
    redshift_conn_id="redshift",
    sql="publishers_table_insert",
    append_mode="False"
)

load_books_publisher_table = LoadDimensionOperatorCAP(
    task_id='Load_books_publisher_dim_table',
    dag=dag,
    table="books_publisher",
    redshift_conn_id="redshift",
    sql="books_publisher_table_insert",
    append_mode="False"
)

run_quality_checks = DataQualityOperatorCAP(
    task_id='Run_data_quality_checks',
    dag=dag,
    tables=["ratings", "users", "yearofpub", "authors", "books_author", 
            "titles", "books_title", "publishers", "books_publisher"],
    redshift_conn_id="redshift"
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator >> [stage_users_to_redshift,
                  stage_books_to_redshift,
                  stage_ratings_to_redshift] >> load_ratings_table

load_ratings_table >> [load_users_table,
                       load_yearofpub_table,
                       load_authors_table,
                       load_books_author_table,
                       load_titles_table,
                       load_books_title_table,
                       load_publishers_table,
                       load_books_publisher_table] >> run_quality_checks

run_quality_checks >> end_operator
