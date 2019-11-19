import psycopg2
import inspect
import patterns.circuit_breaker as cbreaker
from loadconfig import load_config


def connection():
    # Connection to use when deploying in local
    # config = load_config('../config/config.yml')

    # Connection to use when deploying on docker
    config = load_config('config/config.yml')

    # Check if the breaker already exist and if not, initialize new one
    cb = cbreaker.check_breaker()

    # Check from where the connection is coming in case of open circuit breaker
    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])
    if mod.__name__ != 'patterns.circuit_breaker' and cb.getFlagReconnection():
        return {'msg': 'Circuit breaker is open, reconnection in porgress'}, '500'

    try:
        conn = psycopg2.connect(user=config['postgres']['user'],
                                password=config['postgres']['password'],
                                host=config['postgres']['host'],
                                port=config['postgres']['port'],
                                database=config['postgres']['database'])

        c = conn.cursor()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        conn = ''
        # If exception is raised while connecting, check circuit breaker
        if not cb.getFlagReconnection():
            cb.check_state(error, connection)

    finally:
        # Returning database connection and cursor
        if conn:
            return c, conn
