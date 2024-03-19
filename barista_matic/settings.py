import os


RESTOCK_QUANTITY = int(os.getenv("RESTOCK_QUANTITY", 10))
DB = os.getenv("DB", "sqlite://")
