from backend.settings import *  # noqa: F401,F403,F405

DATABASES = {"default": env.db("DATABASE_URI")}
