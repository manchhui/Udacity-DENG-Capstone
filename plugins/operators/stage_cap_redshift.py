from datetime import datetime, timedelta
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperatorCAP(BaseOperator):
    ui_color = '#358140'
    copy_sql_csv = """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        FORMAT AS {}
        DELIMITER ';'
        IGNOREHEADER 1
        REGION '{}';
    """
    
    copy_sql_json = """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        FORMAT AS JSON '{}'
        REGION '{}';
    """
    
    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 aws_credentials_id="",
                 table="",
                 s3_bucket="",
                 s3_key="",
                 region="",
                 format_type="",
                 *args, **kwargs):

        super(StageToRedshiftOperatorCAP, self).__init__(*args, **kwargs)
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.format_type = format_type
        self.region = region
        self.aws_credentials_id = aws_credentials_id
        
    def execute(self, context):
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        self.log.info('StageToRedshiftOperatorCAP not implemented yet')
        redshift.run("DELETE FROM {}".format(self.table))
        rendered_key = self.s3_key.format(**context)
        
        #code to determine if backfill on specifc timestamps is being requested
        if self.format_type == "csv":
            s3_path = "s3://{}/{}".format(self.s3_bucket, rendered_key)
            self.log.info("Copying data from S3 '{}' to '{}' table on Redshift".format(s3_path, self.table))
            
            #code to determine S3 file path and the destination table on Redshift
            formatted_sql = StageToRedshiftOperatorCAP.copy_sql_csv.format(
                self.table,
                s3_path,
                credentials.access_key,
                credentials.secret_key,
                self.format_type,
                self.region
            )
            redshift.run(formatted_sql)
        else:
            s3_path = "s3://{}/{}".format(self.s3_bucket, rendered_key)
            self.log.info("Copying data from S3 '{}' to '{}' table on Redshift".format(s3_path, self.table))
         
            #code to determine S3 file path and the destination table on Redshift
            formatted_sql = StageToRedshiftOperatorCAP.copy_sql_json.format(
                self.table,
                s3_path,
                credentials.access_key,
                credentials.secret_key,
                self.format_type,
                self.region
            )
            redshift.run(formatted_sql)
        
        #clean up data to remove NULL values
        if self.table == "staging_ratings":
            redshift.run("DELETE FROM {} WHERE iduser IS NULL;".format(self.table))
            redshift.run("DELETE FROM {} WHERE isbn IS NULL;".format(self.table))
            redshift.run("DELETE FROM {} WHERE bookrating IS NULL;".format(self.table))
        elif self.table == "staging_users":
            redshift.run("DELETE FROM {} WHERE iduser IS NULL;".format(self.table))
        elif self.table == "staging_books":
            redshift.run("DELETE FROM {} WHERE isbn IS NULL;".format(self.table))
