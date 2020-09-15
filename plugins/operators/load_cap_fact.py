from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from helpers import SqlQueries

class LoadFactOperatorCAP(BaseOperator):

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
