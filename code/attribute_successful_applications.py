from typing import List
from dataclasses import dataclass, field, asdict

from jinja2 import Environment, FileSystemLoader

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment

REQUIRED_JARS = [
    "file:///opt/flink/lib/flink-sql-connector-kafka_2.11-1.12.0.jar",
    "file:///opt/flink/lib/flink-connector-jdbc_2.11-1.12.0.jar",
    "file:///opt/flink/lib/postgresql-42.2.19.jar"
]

@dataclass(frozen=True)
class FlinkJobConfig:
    job_name: str = 'successful-job-applications'
    jars: List[str] = field(default_factory=lambda: REQUIRED_JARS)


@dataclass(frozen=True)
class KafkaConfig:
    connector: str = 'kafka'
    bootstrap_servers: str = 'kafka:9094'
    consumer_group_id: str = 'flink-consumer-group-1'

@dataclass(frozen=True)
class ClickTopicConfig(KafkaConfig):
    topic: str = 'clicks'
    format: str = 'json'

@dataclass(frozen=True)
class ApplicationTopicConfig(KafkaConfig):
    topic: str = 'applications'
    format: str = 'json'


@dataclass(frozen=True)
class PostgresConfig:
    connector: str = 'jdbc'
    url: str = 'jdbc:postgreqsl://postgres:5432/postgres'
    username: str = 'postgres'
    password: str = 'postgres'
    driver: str = 'org.postgreql.Driver'


@dataclass(frozen=True)
class PostgresUsersTableConfig(PostgresConfig):
    table_name:str = 'job_board.users'

@dataclass(frozen=True)
class PostgresSuccesfulApplicationsTableConfig(PostgresConfig):
    table_name :str = 'job_board.attributed_successful_applications'


def get_exec_env(config: FlinkJobConfig) -> tuple:
    s_env = StreamExecutionEnvironment.get_execution_environment()
    for jar in config.jars:
        s_env.add_jars(jar)
    
    execution_config = s_env.get_config()
    execution_config.set_parallelism(5000)
    t_env = StreamTableEnvironment.create(s_env)
    return s_env, t_env


def map_sql_query(table: str, type: str = 'source', template_env: Environment = Environment(loader=FileSystemLoader('code/'))) -> str:
    config_map = {
        'clicks': ClickTopicConfig(),
        'applications': ApplicationTopicConfig(),
        'users' : PostgresUsersTableConfig(),
        'successful_applications' : PostgresSuccesfulApplicationsTableConfig
    }

    return template_env.get_template(f'{type}/{table}.sql').render(
        asdict(config_map.get(table))
    )

def run_successful_applications_job(
        table_env: StreamTableEnvironment,
        map_sql_query=map_sql_query
) -> None:
    table_env.execute_sql(map_sql_query('clicks'))
    table_env.execute_sql(map_sql_query('applications'))
    table_env.execute_sql(map_sql_query('users'))

    table_env.execute_sql(map_sql_query('attributed_successful_applications','sink'))
    
    


    


