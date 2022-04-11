from pydantic import BaseSettings

class Config(BaseSettings):
    global_reply = True
    class Config:
        extra = "ignore"
