#!/bin/bash
promote_slave() {
    mysql - u root - proot - e "stop slave io_thread";
    mysql - u root - proot - e "show processlist;" | grep " waiting for the slave I/O thread to update it"
    if [$? -ne 0]
    then
    echo "Slave IO was not stopped"
    exit 1
    fi
    mysql - u root - proot - e "stop slave";
    mysql - u root - proot - e "reset slave";
    mysql - u root - proot - e "reset master";
    sed - i '/^\s*read_only/c\read_only = 0' / etc / mysql / mysql.conf.d / mysqld.cnf
    service mysqld restart
    mysql - u root - proot - e "show variables like 'read_only'" | grep OFF
    if [$? -ne 0]
    then
    echo "Server is running in read only mode"
    exit 1
    fi
}


mysql -u root -proot -e 'SHOW SLAVE STATUS\G;' > /tmp/replication.txt
replication_lag=`cat /tmp/replication.txt |grep Seconds_Behind_Master|cut -d ":" -f2|sed -e 's/^[ \t]*//'`
Slave_IO_Status=`cat /tmp/replication.txt |grep Slave_IO_Running | cut -d ":" -f2|sed -e 's/^[ \t]*//'`
Slave_SQL_Status=`cat /tmp/replication.txt |grep Slave_SQL_Running | cut -d ":" -f2|sed -e 's/^[ \t]*//'`
if [ $Slave_IO_Status == "No" ] || [ $Slave_SQL_Status == "No" ] || [ $replication_lag == NULL ] || [ $replication_lag -gt 60 ]; then
promote_slave
fi
