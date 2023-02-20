q = {'INDEX': 1, 'IS': 2, 'AGGR': 3}
base_sum = 'select SUM (text_size) from OBJECT_QUEUE_OBJ where OBJECT_QUEUE_ID = '
base_count = 'select COUNT(*) from OBJECT_QUEUE_OBJ where OBJECT_QUEUE_ID = '
q_sum = {k: base_sum + str(v) for k, v in q.items()}
q_count = {k: base_count + str(v) for k, v in q.items()}
oracle_err_count = "select count(*) from v_sys_log where SEVERITY in ('error') and INSERT_DATE > TO_TIMESTAMP (to_char(TRUNC(sysdate - {minutes}*1/(24*60) , 'HH'),'DD-MM-RR HH24:MI:SS'), 'DD-MM-RR HH24:MI:SS.FF')"