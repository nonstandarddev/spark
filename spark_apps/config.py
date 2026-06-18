import os


SPARK_MASTER: str = os.getenv("SPARK_MASTER_URL", "local")
SPARK_HOME: str = os.getenv("SPARK_HOME", "/opt/spark")
SPARK_DATA_ROOT: str = f"{SPARK_HOME}/data"


def path_to(filename: str):
    return f"file://{SPARK_DATA_ROOT}/{filename}"
