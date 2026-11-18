from storage.store import KVStore
from recovery.recovery import recovery


def run_interactive(store=None):
    if store is None:
        store = KVStore()
        recovery(store)

    print("""
Commands:
    'get'    : Get a value by key
    'put'    : Put a key-value pair
    'delete' : Delete a key from store
    'print'  : Print the entire in-memory store
    'recover': Re-sync store from logs
    'exit'   : Exit
""")

    while True:
        try:
            choice = input("Enter choice: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break

        if choice == "get":
            key_req = input("Pls enter key to look for: ")
            print(store.get(key_req))

        elif choice == "put":
            key_req = input("Pls enter key to insert: ")
            value_req = input("Pls enter value to insert: ")
            print(store.put(key_req, value_req))

        elif choice == "delete":
            key_req = input("Pls enter key to delete: ")
            print(store.delete(key_req))

        elif choice == "print":
            print(store.store)

        elif choice == "recover":
            recovery(store)
            print("Recovered store from logs.")

        elif choice in ("exit", "quit"):
            print("Goodbye!")
            break

        elif not choice:
            continue

        else:
            print(f"Unknown command: '{choice}'. Available commands: get, put, delete, print, recover, exit")


if __name__ == "__main__":
    run_interactive()
