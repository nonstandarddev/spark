"""
Outlines the approach to utilising Delta Lake *in general* (purely as a storage format).

With this workflow, 

* You have full control over *how* your data is processed (e.g. Polars, DuckDB and so on). You are 
simply using Delta Lake as your storage format.

* This is achieved via the Python package `deltalake` which is merely an interface into the 
underlying Rust bindings for manipulating delta tables - on most standard systems, the pre-compiled
binary wheels are provisioned via `pip install deltalake` (so you don't need a Rust compiler).

* Once you've installed `deltalake`, this script can be administered wherever you desire with 
ordinary Python i.e. `python delta-lake-example-rs.py`.
"""
import pandas as pd

from deltalake.writer import write_deltalake
from deltalake import DeltaTable

# ---- 1: Configuration ----

df1 = pd.DataFrame(range(5), columns=["id"])
df2 = pd.DataFrame(range(6, 11), columns=["id"])

# ---- 2: Runtime ----

# Write a delta tables to local storage

# 2a: Overwrite mode
write_deltalake("./spark_data/delta-table-rs", df1, mode="overwrite")

# 2b: Append mode
write_deltalake("./spark_data/delta-table-rs", df2, mode="append")

# Read the delta table into memory
dt = DeltaTable("./spark_data/delta-table-rs")

dt.to_pandas()
