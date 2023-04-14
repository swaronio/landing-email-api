def get_environment_variables(variable:str):
    from dotenv import load_dotenv
    import os
    load_dotenv()
    return os.getenv(variable)