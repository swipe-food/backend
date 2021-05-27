from __future__ import annotations

from pathlib import Path

from dotenv import dotenv_values

from infrastructure.config.types import ConfigComponent, LogLevelField, ConfigField

PROJECT_ROOT_DIR = Path(__file__).parent.parent.parent


class CrawlerConfig(ConfigComponent):
    PREFIX = 'CRAWLER_'
    fetch_batch_size: int
    log_file_name: str
    log_level_console: str = LogLevelField()
    log_level_file: str = LogLevelField()


class ApiConfig(ConfigComponent):
    PREFIX = "API_"
    name: str
    host: str
    port: int
    debug: bool
    log_file_name: str
    log_level_console: str = LogLevelField()
    log_level_file: str = LogLevelField()


class DatabaseConfig(ConfigComponent):
    PREFIX = 'DATABASE_'
    dialect: str
    driver: str
    host: str
    port: int
    name: str
    user: str
    password: str
    max_idle_connections: int
    max_open_connections: int
    logging_enabled: bool

    def get_dsn(self, sanitize: bool = False):
        print(self.password)
        return '{dialect}{driver}://{user}:{password}@{host}{port}/{name}'.format(
            dialect=self.dialect,
            driver=f'+{self.driver}' if self.driver is not None else '',
            user=self.user,
            password=self.password if not sanitize else '*' * 3,
            host=self.host,
            port=f':{self.port}' if self.port is not None else '',
            name=self.name
        )


class AppConfig(ConfigComponent):
    PREFIX = 'SF_'
    environment: str
    build_commit: str = ConfigField(optional=True, default='unknown')
    build_time: str = ConfigField(optional=True, default='unknown')
    api: ApiConfig
    crawler: CrawlerConfig
    database: DatabaseConfig


def create_new_config(env_file_path: str = f'{PROJECT_ROOT_DIR}/local.env') -> AppConfig:
    config = dotenv_values(env_file_path)
    return AppConfig.load_and_parse(config)
