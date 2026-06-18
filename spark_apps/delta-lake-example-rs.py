import pandas as pd

from deltalake.writer import write_deltalake
from deltalake import DeltaTable
from config import (
    SPARK_DATA_ROOT
)

df = pd.DataFrame(range(5), columns=["id"])

write_deltalake(f"{SPARK_DATA_ROOT}/delta-table-rs", df, mode="overwrite")

df = pd.DataFrame(range(6, 11), columns=["id"])

write_deltalake(f"{SPARK_DATA_ROOT}/delta-table-rs", df, mode="append")

dt = DeltaTable(f"{SPARK_DATA_ROOT}/delta-table-rs")

dt.to_pandas()
