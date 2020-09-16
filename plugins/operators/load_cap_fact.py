from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from helpers import SqlCAPQueries

class LoadFactOperatorCAP(BaseOperator):
    
    """ 
    Summary: Loads fact table
    
    Description: The MAIN DAG calls this operator to load the FACT table.
    
    Parameters: 
    MAIN DAG passes the table name and the name of the SQL code to lift from "SqlCAPQueries" to allow this custom operator to insert data.
    
    Returns: 
    Nil.
    """

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 table="",
                 redshift_conn_id="",
                 sql="",
                 *args, **kwargs):

        super(LoadFactOperatorCAP, self).__init__(*args, **kwargs)
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.sql = sql
        
    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        self.log.info('LoadFactOperatorCAP not implemented yet')
        formatted_sql = getattr(SqlCAPQueries,self.sql)
        
        self.log.info('Loading Fact Table')
        redshift.run(formatted_sql)
