import logging
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

LOGGING_DIR = Path(os.getenv("LOGGING_DIR","logs"))
LOGGING_DIR.mkdir(parents=True, exist_ok=True)
LOGGING_FILE = LOGGING_DIR / "store.log"

logging.basicConfig(
    filename=LOGGING_FILE, 
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    
logger = logging.getLogger("key_val_museum")

# rotating logs usage later