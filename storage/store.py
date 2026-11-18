from logger.logger import logger


class KVStore:
    def __init__(self):
        self.store = {}

    def put(self, key, val):
        key = key.strip()
        val = val.strip()
        if key in self.store:
            logger.info(f"REPLACE '{key}' '{val}'")
        else:
            logger.info(f"PUT '{key}' '{val}'")
        self.store[key] = val
        return "OK"

    def get(self, key):
        key = key.strip()
        if key in self.store:
            logger.info(f"GET '{key}'")
            return self.store.get(key)
        else:
            logger.error(f"GET_NF '{key}'")
            return "NF"

    def delete(self,key):
        key = key.strip()
        if key in self.store:
            logger.info(f"DELETE \'{key}\'")
            return self.store.pop(key)
        else:
            logger.error(f"DELETE_NF \'{key}\'")
            return "NF"