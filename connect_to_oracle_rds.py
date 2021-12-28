Download Oracle Instant Client https://www.oracle.com/database/technologies/instant-client/macos-intel-x86-downloads.html
sudo pip3 install cx-Oracle 


# importing module
import cx_Oracle
import os

# Create a table in Oracle database
try:
    lib_dir = os.path.join(os.environ.get("HOME"), "Downloads","instantclient_19_8")
    cx_Oracle.init_oracle_client(lib_dir=lib_dir)

    con = cx_Oracle.connect("dev/dev@dev.c1pbxqc.us-east-1.rds.amazonaws.com/DEV")
    print(con.version)

except cx_Oracle.DatabaseError as e:
    print("There is a problem with Oracle", e)
