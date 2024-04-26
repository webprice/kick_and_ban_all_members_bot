import dotenv
class Settings():
    env = dotenv.dotenv_values()


    BOT_TOKEN: str = env.get('BOT_TOKEN')
    BOT_NAME: str = env.get('BOT_NAME')
    APP_API_ID: str = env.get('APP_API_ID')
    APP_API_HASH: str = env.get('APP_API_HASH')

settings = Settings()