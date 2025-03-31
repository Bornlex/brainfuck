from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_prefix='LLM_', extra='ignore')

    API_KEY: str = ''
    MODEL: str = 'local'
    URL: str = ''
