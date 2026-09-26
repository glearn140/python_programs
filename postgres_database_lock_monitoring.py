import time
class AppError(Exception):
    pass
def main():
   while True:
        try:
           database_check()
        except AppError as e:
            print (f'Issue found while running the app, please reach out to Gaurav. Details are: {e}')
        time.sleep(30)


def database_check(): 
    conn = None
    try:
        import os
        import psycopg2
        os.environ["hostname"]="localhost"
        os.environ["passwd"]="pass123"
        os.environ["username"]="postgres"
        os.environ["dbname"]="pgdb"
        conn=psycopg2.connect(host=os.getenv("hostname"),dbname=os.getenv("dbname"),user=os.getenv("username"),port=5432,password=os.getenv("passwd"))
        cur=conn.cursor()
        cur.execute("SELECT pid, query_start, query, state, wait_event FROM pg_stat_activity WHERE pid <> pg_backend_pid() AND state <> 'idle' AND query_start IS NOT NULL AND now() - query_start >  '2 min';")
        result=cur.fetchall()
        for i in result:
           #cur.execute("insert into reportlrq values %s", (i,))
           #cur.execute("insert into reportlrq (pid, query, state, wait_event) values (%s,%s,%s,%s)",i)
            cur.execute("insert into reportlrq_v2 (pid, query_start, query, state, wait_event, frequency) values (%s,%s,%s,%s,%s,1) on conflict(pid, query_start) do update set frequency = reportlrq_v2.frequency+1",i)
        conn.commit()
    except Exception as e:
        raise AppError(e) from e
    finally:
        if conn is not None:
            conn.close()
main()