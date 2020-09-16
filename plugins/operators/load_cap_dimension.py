from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from helpers import SqlCAPQueries

class LoadDimensionOperatorCAP(BaseOperator):
    
    """ 
    Summary: Loads dimension tables
    
    Description: The MAIN DAG calls this operator after loading the DIMENSION tables.
    
    Parameters: 
    MAIN DAG passes the table name and the name of the SQL code to lift from "SqlCAPQueries" to allow this custom operator to insert data.
    
    Returns: 
    Nil.
    """

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 table="",
                 redshift_conn_id="",
                 sql="",
                 append="",
                 *args, **kwargs):

        super(LoadDimensionOperatorCAP, self).__init__(*args, **kwargs)
        self.table=table
        self.redshift_conn_id=redshift_conn_id
        self.sql=sql
        self.append=append

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        self.log.info('LoadDimensionOperatorCAP not implemented yet')
        formatted_sql = getattr(SqlCAPQueries,self.sql)
        
        if self.append:
            self.log.info("APPEND MODE: Loading '{}' Dimension Table".format(self.table))
            redshift.run(formatted_sql)
        else:
            self.log.info("Deleting From '{}' Dimension Table".format(self.table))
            redshift.run("DELETE FROM {}".format(self.table))
            
            self.log.info("Loading '{}' Dimension Table".format(self.table))
            redshift.run(formatted_sql)
