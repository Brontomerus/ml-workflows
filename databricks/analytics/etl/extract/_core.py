import datetime
import pyspark
from pytz import timezone


class Helpers:
    def __init__(self):
        self.mappers = {}
    
    @staticmethod
    def today_yyyymmdd(day = datetime.datetime.now(), dt_timezone: str = 'EST'):
        tz = timezone(dt_timezone)
        today_yyyymmdd = datetime.datetime.now(tz).strftime('%Y%m%d')
        return today_yyyymmdd
    

class Metadata():
    def __init__(self, table: str):
        self.table = table
        self.schema = table
        
    @property
    def table(self):
        return self._table

    @table.setter
    def table(self, value: str):
        self._table = value

    @property
    def schema(self):
        return self._schema

    @schema.setter
    def schema(self, value: str):
        self._schema = pyspark.sql(f"select * from {self.table} limit 0;").schema


      
    
class FileTools:
    def __init__(self, 
                 spark,
                 table: str,
                 year_month_partition_column: str,
                 bucket: str = "btd-db-archive", 
                 root_folder: str = f"db-table-backup-{Helpers.today_yyyymmdd()}", 
                 stem: str = f"extracts/extracts", 
                 file_format: str = "parquet", 
                 path_override: str = ""):
        format_options = {
            "parquet": {
                    "copy_into": "PARQUET",
                    "ext": ".parquet"
                },
            "csv": {
                    "copy_into": "CSV",
                    "ext": ".csv"
                },
            "txt": {
                    "copy_into": "TEXT",
                    "ext": ".text"
                },
            "json": {
                    "copy_into": "JSON",
                    "ext": ".json"
                }
        }
        dbutils = None
      
        if spark.conf.get("spark.databricks.service.client.enabled") == "true":
            from pyspark.dbutils import DBUtils
            self.dbutils = DBUtils(spark)
        else:
            import IPython
            self.dbutils = IPython.get_ipython().user_ns["dbutils"]
    
        self.table= table
        self.partition_column = year_month_partition_column
        self.bucket = bucket
        self.root_folder = root_folder
        self.stem = stem
        self.path = ''
        self.files = format_options[file_format].get("ext")
        self.copy_stmt = format_options[file_format].get("copy_into")
        
    
    @property
    def path(self):
        return self._path
    
    @path.setter
    def path(self, value: str):
        self._path = f"s3://{self.bucket}/{self.root_folder}/{self.stem}.{self.table}/1/"

    @property
    def files(self):
        return self._files
    
    @files.setter
    def files(self, value: str):
        ls = self.dbutils.fs.ls(self.path)
        self._files = []
        for file in ls:
            if file.path.endswith(value):
                self._files.append(file.path.replace(self.path, ''))
    
    @property
    def copy_stmt(self):
        return self._copy_stmt
    
    @copy_stmt.setter
    def copy_stmt(self, value: str):
        self._copy_stmt = f"""
        COPY INTO wrangled.raw.{self.table}
        FROM (
            SELECT
                *,
                date_format({self.partition_column}, 'yMM') as {self.partition_column}_yrmnth
            FROM '{self.path}'
        )
        FILES = ('{",'".join(self.files)})
        FILEFORMAT = {value};
        """.strip()
        
        # PATTERN '{self.paths}' or FILES = ('{",'".join(self.paths)})
