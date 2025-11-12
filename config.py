class Config:
    SECRET_KEY = "hola123" 


class DevelopmentConfig(Config):
    DEBUG=True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'proyecto_comba_final'

config={
    'development': DevelopmentConfig
}