from typing import Optional, Dict
from logging import Logger

from pyspark.sql import SQLContext, DataFrame
from pyspark import SparkContext


def read_from_ch(config: Dict,
                 sql: str,
                 sc: SparkContext,
                 logger: Optional[Logger]=None
                 ) -> DataFrame:
    """ Read DF from ClickHouse SQL

    Args:
        config: config
        sql: sql
            it may be one of these format:
            - 'table_name'
            - 'schema_name.table_name'
            - '(select a, b, c from t1 join t2 ...) as foo'
        sc: spark context
        logger: logger

    Returns:
        DataFrame
    """
    if logger:
        logger.info('read_from_ch: {}'.format(sql))
    spark = SQLContext(sc)
    df = spark.read.format("jdbc").options(
        url=config['CH_JDBC_URL'],
        dbtable=sql,
        **config['CH_JDBC_PROPERTIES']
    ).load().cache()
    return df
