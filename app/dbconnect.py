import psycopg2
import inspect
import circuit_breaker as cbreaker

def connection():
    cb = check_breaker()

    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])
    if mod.__name__ != 'circuit_breaker' and cb.getFlagReconnection():
        return {'msg': 'Circuit breaker is open, reconnection in porgress'}, '500'

    print('Module name is: ' + mod.__name__)

    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="10.0.200.68",
                                port="5432",
                                database="planthealthcare")

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


def check_breaker():
    global cb
    print('starting cb check: \n')
    try:
        cb
        print('Found cb in try block\n')
    except:
        cb = None
    if cb is None:
        print('cb is None\n')
        cb = cbreaker.CircuitBreaker(2, 0, 10, 5, ['OperationalError'])
        print('Created new circuit breaker\n')
    else:
        print('cb is not none. Displaying values on entry to connect method')
        cb.display()

    return cb