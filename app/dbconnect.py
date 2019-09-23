import psycopg2


def connection():
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="10.0.200.68",
                                port="5432",
                                database="planthealthcare")

        c = conn.cursor()
        # Print PostgreSQL Connection properties
        print( conn.get_dsn_parameters(),"\n")

        # Print PostgreSQL version
        c.execute("SELECT version();")
        record = c.fetchone()
        print("You are connected to - ", record,"\n")

    except (Exception, psycopg2.Error) as error :
        print("Error while connecting to PostgreSQL", error)
    finally:
        #returning database connection
        if(conn):
            return c, conn
