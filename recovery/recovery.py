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


def recovery(store: KVStore):
    if not LOGGING_FILE.exists():
        return

    store.store.clear()
    logger.disabled = True
    try:
        with open(LOGGING_FILE, "r") as file:
            for log_line in file:
                log_line = log_line.strip()
                if not log_line or "key_val_museum: " not in log_line:
                    continue

                msg = log_line.split("key_val_museum: ", 1)[1]
                tokens = shlex.split(msg)
                if not tokens:
                    continue

                action = tokens[0]
                if action in ("PUT", "REPLACE") and len(tokens) >= 3:
                    store.put(tokens[1], tokens[2])
                elif action == "DELETE" and len(tokens) >= 2:
                    store.delete(tokens[1])
    finally:
        logger.disabled = False
