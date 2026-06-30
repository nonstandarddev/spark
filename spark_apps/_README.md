# Notes on Spark

## Useful Concepts

* Use _broadcasters_ to broadcast smaller reference read-only datasets across a cluster (e.g. for join purposes)
* Use _accumulators_ to centralise a write-only variables across a cluster (e.g. for monitoring purposes)
* Use _cache_ to cache repeatedly accessed dataframes _in memory_; use _persist_ for disk caching

## Spark SQL

You can provision an entire database server over JDBC / ODBC.

* Start it with `./sbin/start-thriftserver.sh` (listens on port `10000` by default)
* Connect using `./bin/beeline -u jdbc:hive2://localhost:10000`
* You now have shell access to Spark SQL - you can perform DDL and DML just like any 
database server instance