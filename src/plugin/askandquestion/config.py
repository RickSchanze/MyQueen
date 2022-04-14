from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    global_reply = True

    class Config:
        extra = "ignore"