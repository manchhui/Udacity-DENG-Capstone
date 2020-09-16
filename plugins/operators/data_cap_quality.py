from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperatorCAP(BaseOperator):
    
    """ 
    Summary: Check tables contain data.
    
    Description: The MAIN DAG calls this operator after loading the FACT and DIMENSION tables to check that data had actually been transferred 
    
    Parameters: 
    MAIN DAG passes the tables names to this custom operator.
    
    Returns: 
    Logs the results of the check.
    """

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 tables="",
                 redshift_conn_id="",
                 *args, **kwargs):

        super(DataQualityOperatorCAP, self).__init__(*args, **kwargs)
        self.tables=tables
        self.redshift_conn_id=redshift_conn_id
       
    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        self.log.info('DataQualityOperatorCAP not implemented yet')
        
        for table in self.tables:
            self.log.info("Show {} in for loop".format(table))
            
            records = redshift.get_records("SELECT COUNT(*) FROM {}".format(table))
            num_records = records[0][0]
            
            if len(records) < 1 or len(records[0]) < 1:
                logging.error("Data quality check failed. {} returned no results".format(table))
                raise ValueError("Data quality check failed. {} returned no results".format(table))
                
            if num_records == 0:
                logging.error("No records present in destination table {}".format(table))
                raise ValueError("No records present in destination table {}".format(table))
            
            self.log.info("Data quality on table {} check passed with {} records".format(table, num_records))
