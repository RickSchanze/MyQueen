import json
import os
permission_path = os.path.join(os.path.dirname(__file__), "permission.json")
with open(permission_path, "r") as per:
    permission = json.load(per)
    if "words_managers" not in permission.keys():
        permission["words_managers"] = []
    if "setu_managers" not in permission.keys():
        permission["setu_managers"] = []
    if "supermanager" not in permission.keys():
        permission["supermanager"] = []
    if "groupSetuAvailable" not in permission.keys():
        permission["groupSetuAvailable"] = {}
