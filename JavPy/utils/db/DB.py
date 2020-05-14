from unqlite import UnQLite
import json
from pathlib import Path


class Namespace:
    def __init__(self, father, name):
        self.father = father
        self.namespace = name

    def __getitem__(self, key):
        print("%s::%s" % (self.namespace, key))
        return self.father["%s::%s" % (self.namespace, key)]

    def __setitem__(self, key, value):
        self.father["%s::%s" % (self.namespace, key)] = value


class DB:
    def __init__(self, path):
        self.__db = UnQLite(path)

        self.Global = Namespace(self.__db, "Global")
        self.User = Namespace(self.__db, "User")

    def migrate_from_json(self, path):
        with open(path) as fp:
            obj = json.load(fp)

        with self.__db.transaction():
            self.Global["version"] = obj["version"]
            self.Global["proxy"] = {
                "http": obj["proxy"],
                "https": obj["proxy"]
            }
            self.Global["ip-blacklist"] = obj["ip-blacklist"]
            self.Global["ip-whitelist"] = obj["ip-whitelist"]

            self.User["default"] = {
                "password": obj["password"]
            }

    def close(self):
        self.__db.close()
