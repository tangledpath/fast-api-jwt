import os
environment = os.getenv('FAST_API_ENV', 'development')
if environment != 'production':
    from dotenv import load_dotenv
    env_path = f".env.{environment}"
    load_dotenv(env_path)
    print(f"Loading environment variables from {env_path}", os.environ)

