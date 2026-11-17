from storage.store import KVStore

store = KVStore()

print("""
    'get': Get a value from key
    'put': Put a key value pair
    'delete': Delete a key from store
""")
while(True):
    choice = input("Enter choice ")

    if choice == "get":
        key_req = input("Pls enter key to look for ")
        print(store.get(key_req))

    elif choice == "put":
        key_req = input("Pls enter key to insert ")
        value_req = input("Pls enter value to insert ")
        print(store.put(key_req,value_req))

    elif choice == "delete":
        key_req = input("Pls enter key to delete ")
        print(store.delete(key_req))

    elif choice == "print":
        print(store.store)