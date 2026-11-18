import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
sys.path.append(str(ROOT_DIR))

from storage.store import KVStore
from recovery.recovery import recovery


def main():
    parser = argparse.ArgumentParser(
        prog="key-val-museum",
        description="CLI to interact with key-value museum",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # put command
    put_parser = subparsers.add_parser("put", help="Insert or update a key-value pair")
    put_parser.add_argument("key", type=str, help="Key to insert")
    put_parser.add_argument("value", type=str, help="Value to insert")

    # get command
    get_parser = subparsers.add_parser("get", help="Get a value by key")
    get_parser.add_argument("key", type=str, help="Key to look up")

    # delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a key from the store")
    delete_parser.add_argument("key", type=str, help="Key to delete")

    # print / list command
    subparsers.add_parser("print", help="Print all key-value pairs in the store")

    # interactive command
    subparsers.add_parser("interactive", help="Start an interactive session (REPL)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Initialize store and recover state from append-only log
    store = KVStore()
    recovery(store)

    if args.command == "put":
        print(store.put(args.key, args.value))
    elif args.command == "get":
        print(store.get(args.key))
    elif args.command == "delete":
        print(store.delete(args.key))
    elif args.command == "print":
        print(store.store)
    elif args.command == "interactive":
        from main import run_interactive
        run_interactive(store)


if __name__ == "__main__":
    main()
