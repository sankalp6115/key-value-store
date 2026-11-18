import os
from pathlib import Path
import shlex
import sys
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from storage.store import KVStore
from logger.logger import logger

load_dotenv(ROOT_DIR / ".env")

LOGGING_DIR = Path(os.getenv("LOGGING_DIR", "logs"))
LOGGING_DIR.mkdir(parents=True, exist_ok=True)
LOGGING_FILE = LOGGING_DIR / "store.log"

MUTATION_OPS = {"PUT", "REPLACE", "DELETE"}
READ_OPS = {"GET", "GET_NF", "DELETE_NF"}


def recovery(store: KVStore) -> list[str]:
    if not LOGGING_FILE.exists():
        return []

    store.store.clear()
    logger.disabled = True
    corrupted_records = []

    try:
        with open(LOGGING_FILE, "r") as file:
            for line_num, log_line in enumerate(file, start=1):
                log_line = log_line.strip()
                if not log_line:
                    continue

                if "key_val_museum: " not in log_line:
                    msg = f"Line {line_num}: Malformed record (missing logger prefix) -> '{log_line}'"
                    print(f"[RECOVERY WARNING] {msg}")
                    corrupted_records.append(msg)
                    continue

                msg_part = log_line.split("key_val_museum: ", 1)[1].strip()

                try:
                    tokens = shlex.split(msg_part)
                except ValueError as err:
                    msg = f"Line {line_num}: Syntax error in record ({err}) -> '{msg_part}'"
                    print(f"[RECOVERY WARNING] {msg}")
                    corrupted_records.append(msg)
                    continue

                if not tokens:
                    continue

                operation = tokens[0]

                # Skip read-only ops (GET, GET_NF, DELETE_NF)
                if operation in READ_OPS:
                    continue

                # Flag unknown operations
                if operation not in MUTATION_OPS:
                    msg = f"Line {line_num}: Unknown operation type '{operation}' -> '{msg_part}'"
                    print(f"[RECOVERY WARNING] {msg}")
                    corrupted_records.append(msg)
                    continue

                # Handle PUT and REPLACE (needs key and value)
                if operation in ("PUT", "REPLACE"):
                    if len(tokens) < 3:
                        msg = f"Line {line_num}: Missing key or value for {operation} (expected 2 args, got {len(tokens) - 1}) -> '{msg_part}'"
                        print(f"[RECOVERY WARNING] {msg}")
                        corrupted_records.append(msg)
                        continue
                    store.put(tokens[1], tokens[2])

                # Handle DELETE (needs key)
                elif operation == "DELETE":
                    if len(tokens) < 2:
                        msg = f"Line {line_num}: Missing key for DELETE (expected 1 arg, got 0) -> '{msg_part}'"
                        print(f"[RECOVERY WARNING] {msg}")
                        corrupted_records.append(msg)
                        continue
                    store.delete(tokens[1])

    finally:
        logger.disabled = False

    return corrupted_records
