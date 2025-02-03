import os

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    RABBITMQ_LOGIN: str = os.getenv('RABBITMQ_LOGIN')
    RABBITMQ_PASSWORD: str = os.getenv('RABBITMQ_PASSWORD')
    RABBITMQ_HOST: str = os.getenv('RABBITMQ_HOST')
    RABBITMQ_PORT: int = int(os.getenv('RABBITMQ_PORT'))

    @property
    def SCOPES(self) -> dict:
        scopes_dict = {}
        scopes_from_env_variables = os.getenv("SCOPES", "")
        for scope in scopes_from_env_variables.split(','):
            scope_name, scope_description = scope.split(':')
            scopes_dict[scope_name.strip()] = scope_description.strip()

        return scopes_dict

    @property
    def RABBITMQ_URL(self) -> str:
        return f'amqp://{self.RABBITMQ_LOGIN}:{self.RABBITMQ_PASSWORD}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/'


settings = Settings()
