from log.logging import logger

class KVStore:
    store = {}

    def put(self,key,val):
        key = key.strip()
        val = val.strip()
        if key in self.store:
            logger.info(f"Replaced key:{key}, value:{val}")
            self.store[key] = val
        else:
            logger.info(f"Put key:{key}, value:{val}")
            self.store[key] = val

    def get(self,key):
        key = key.strip()
        logger.info(f"Get key:{key}")
        return self.store.get(key,"Not Found")

    def delete(self,key):
        key = key.strip()
        if key in self.store:
            logger.info(f"Deleted key:{key}")
            return self.store.pop(key)
        else:
            logger.error(f"Did not find key:{key}")
            return "Not Found"
    