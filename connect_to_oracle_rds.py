Download Oracle Instant Client https://www.oracle.com/database/technologies/instant-client/macos-intel-x86-downloads.html
sudo pip3 install cx-Oracle 


# importing module
import cx_Oracle
import os


try:
    lib_dir = os.path.join(os.environ.get("HOME"), "Downloads","instantclient_19_8")
    cx_Oracle.init_oracle_client(lib_dir=lib_dir)

    con = cx_Oracle.connect("dev/dev@dev.c1pbxqc.us-east-1.rds.amazonaws.com/DEV")
    print(con.version)

except cx_Oracle.DatabaseError as e:
    print("There is a problem with Oracle", e)
    
else:
	try:
		print("Temporary Space Usage")
		with con.cursor() as cur:
			query_statement="SELECT   A.tablespace_name tablespace, D.mb_total,SUM (A.used_blocks * D.block_size) / 1024 / 1024 mb_used,D.mb_total - SUM (A.used_blocks * D.block_size) / 1024 / 1024 mb_free FROM v$sort_segment A,(SELECT  B.name, C.block_size, SUM (C.bytes) / 1024 / 1024 mb_total FROM     v$tablespace B, v$tempfile C WHERE    B.ts#= C.ts# GROUP BY B.name, C.block_size) D WHERE    A.tablespace_name = D.name GROUP by A.tablespace_name, D.mb_total"
			cur.execute(query_statement)
			result = cur.fetchall()
			print(result)

		print("TEMP usage by session")
		with con.cursor() as cur:
			query_statement="SELECT b.TABLESPACE, ROUND (  (  ( b.blocks * p.VALUE ) / 1024 / 1024 ), 2 ) size_mb, a.SID, a.serial#, a.username, a.osuser, a.machine FROM v$session a, v$sort_usage b, v$process c, v$parameter p WHERE p.NAME = 'db_block_size' AND a.saddr = b.session_addr AND a.paddr = c.addr ORDER BY SIZE_MB desc"
			cur.execute(query_statement)
			result = cur.fetchall()
			print(result)

		print("Temp sort space currently in use by users")
		with con.cursor() as cur:
			query_statement="""SELECT b.tablespace,ROUND(((b.blocks*p.value)/1024/1024),2)||'M' AS temp_size,a.inst_id as Instance,a.sid||','||a.serial# AS sid_serial,NVL(a.username, '(oracle)') AS username,a.program,a.status,a.sql_id
FROM gv$session a,gv$sort_usage b,gv$parameter p WHERE  p.name  = 'db_block_size' AND a.saddr = b.session_addr AND a.inst_id=b.inst_id AND a.inst_id=p.inst_id ORDER BY b.tablespace, b.blocks"""
			cur.execute(query_statement)
			result = cur.fetchall()
			print(result)

		print("Sort Space Usage by Session ")
		with con.cursor() as cur:
			query_statement="SELECT   S.sid || ',' || S.serial# sid_serial, S.username, S.osuser, P.spid, S.module,S.program, SUM (T.blocks) * TBS.block_size / 1024 / 1024 mb_used, T.tablespace,COUNT(*) sort_ops FROM v$sort_usage T, v$session S, dba_tablespaces TBS, v$process P WHERE    T.session_addr = S.saddr AND      S.paddr = P.addr AND      T.tablespace = TBS.tablespace_name GROUP BY S.sid, S.serial#, S.username, S.osuser, P.spid, S.module, S.program, TBS.block_size, T.tablespace ORDER BY sid_serial"
			cur.execute(query_statement)
			result = cur.fetchall()
			print(result)

		print("Sort Space Usage by Statement")
		with con.cursor() as cur:
        		query_statement="SELECT S.sid || ',' || S.serial# sid_serial, S.username,T.blocks * TBS.block_size / 1024 / 1024 mb_used, T.tablespace,T.sqladdr address, Q.hash_value, Q.sql_text FROM     v$sort_usage T, v$session S, v$sqlarea Q, dba_tablespaces TBS WHERE    T.session_addr = S.saddr AND      T.sqladdr = Q.address (+) AND      T.tablespace = TBS.tablespace_name ORDER BY S.sid"
        		cur.execute(query_statement)
        		result = cur.fetchall()
        		print(result)
		print("Temp tablespace temp file check.")
		with con.cursor() as cur:
			query_statement="select file_id ,  tablespace_name, bytes/1024/1024/1024, maxbytes/1024/1024/1024 from dba_temp_files"
			cur.execute(query_statement)
			result = cur.fetchall()
			print(result)
	except cx_Oracle.DatabaseError as er:
		print('There is an error in the Oracle database:', er)
 
	except Exception as er:
		print('Error:'+str(er))
finally:
	if con:
		con.close()
