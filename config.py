from environs import Env


env = Env()
env.read_env()

secret_key = env.str('SECRET_KEY', 'REPLACE_ME')
database_uri = env.str('DATABASE_URI', 'sqlite:///db.sqlite3?check_same_thread=False')