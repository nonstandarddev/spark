# Notes on Spark

## Spark SQL

You can provision an entire database server over JDBC / ODBC.

* Start it with `./sbin/start-thriftserver.sh` (listens on port `10000` by default)
* Connect using `./bin/beeline -u jdbc:hive2://localhost:10000`
* You now have shell access to Spark SQL - you can perform DDL and DML just like any 
database server instance