from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    model_config=SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

    keycloak_base_url: str
    keycloak_realm: str
    keycloak_client_id: str
    keycloak_client_secret: str
    keycloak_audience: str


settings = Settings()


