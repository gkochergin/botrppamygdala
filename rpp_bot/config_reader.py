from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    # Вложенный класс с дополнительными указаниями для настроек конфиденциальных данных
    tg_token: SecretStr
    db_pass: SecretStr
    db_user: SecretStr
    db_host: SecretStr
    db_name: SecretStr
    sentry_dsn: SecretStr
    django_secret_key: SecretStr
    django_debug: bool
    django_allowed_hosts: list

    class Config:
        # Имя файла, откуда будут прочитаны данные
        # (относительно текущей рабочей директории)
        env_file = '.env'
        # Кодировка читаемого файла
        env_file_encoding = 'utf-8'

    # При импорте файла сразу создастся
    # и провалидируется объект конфига,
    # который можно далее импортировать из разных мест


config = Settings()
