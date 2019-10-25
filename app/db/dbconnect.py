import psycopg2
import inspect
import patterns.circuit_breaker as cbreaker
from loadconfig import load_config


def connection():
    config = load_config('config/config.yml')
    cb = cbreaker.check_breaker()

    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])
    if mod.__name__ != 'patterns.circuit_breaker' and cb.getFlagReconnection():
        return {'msg': 'Circuit breaker is open, reconnection in porgress'}, '500'

    print('Module name is: ' + mod.__name__)

    try:
        conn = psycopg2.connect(user=config['postgres']['user'],
                                password=config['postgres']['password'],
                                host=config['postgres']['host'],
                                port=config['postgres']['port'],
                                database=config['postgres']['database'])

        print('\n\nConnection successful\n\n')

        c = conn.cursor()

        # Print PostgreSQL version
        c.execute("SELECT version();")
        record = c.fetchone()
        print("You are connected to - ", record, "\n")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        conn = ''
        if not cb.getFlagReconnection():
            cb.check_state(error, connection)

    finally:
        # returning database connection
        if conn:
            return c, conn
