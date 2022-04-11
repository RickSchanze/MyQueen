
import nonebot
import json

class TwoMessage:
    first_msg = ''
    second_msg = ''
    async def check_if_matched(first, second, third):
        return first.first_msg == second.first_msg == third.first_msg and first.second_msg == second.second_msg == third.second_msg

class GlobalDialog:
    global_msg = ''
    def __init__(self):
        try:
            with open("globalDialog.json", encoding='utf-8') as f:
                self.global_msg = json.load(f)
                f.close()
        except FileNotFoundError as e:
            with open("globalDialog.json", "a+", encoding='utf-8') as f:
                pass





