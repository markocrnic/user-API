import threading
import time


class CircuitBreaker:
    flag = True
    flag_reconnection_started = False
    error_threshold = 3
    error_occurrence = 0
    reconnection_time = 10
    reconnection_interval = 3
    exception_types = []

    def __init__(self, error_threshold, error_occurrence, reconnection_time, reconnection_interval, exception_types):
        self.error_threshold = error_threshold
        self.error_occurrence = error_occurrence
        self.reconnection_time = reconnection_time
        self.reconnection_interval = reconnection_interval
        self.exception_types = exception_types

    def check_state(self, error, methodToRun):
        if error.__class__.__name__ in self.exception_types:
            print('Error caught inside given exception types. Starting breaker check.\n')
            if self.error_occurrence < self.error_threshold:
                print('Error threshold not yet reached, incrementing occurrence. \n')
                self.error_occurrence += 1
                print('Error occurrence after incrementing: ' + str(self.error_occurrence) + '\n')
            else:
                print('Error threshold is reached. \n')
                self.flag = False

                if not self.flag_reconnection_started:
                    print('Starting new thread for reconnecting.\n')
                    self.flag_reconnection_started = True
                    print('Set flag for reconnection to :' + str(self.flag_reconnection_started) + ' --- should be True\n')
                    thread = threading.Thread(target=self.try_reconnection, args=(methodToRun, ))
                    thread.start()
            return str(self.flag)
        else:
            return 'Error not caught in breaker'

    def try_reconnection(self, methodToRun):

        self.flag_reconnection_started = True

        print('Commencing reconnection in ' + str(self.reconnection_time) + ' seconds.\n')
        print('Value of Flag of reconnection started is: ' + str(self.flag_reconnection_started) + '\n')
        time.sleep(self.reconnection_time)
        print('Reconnection starting.\n')
        while not self.flag:
            print('Inside while loop. Trying to reconnect. Flag value is: ' + str(self.flag) + '\n')
            #self.display()
            print(methodToRun)
            if methodToRun():
                print('\nReconnection is successful. Resetting values.\n')
                self.display()
                self.reset_values()
                print('\nValues after reset: \n')
                self.display()
            else:
                print('Not reconnected. Trying again in ' + str(self.reconnection_interval) + ' seconds.\n')
                time.sleep(self.reconnection_interval)

    def display(self):
        print(
            'Flag: %s \nFlag_reconnection_started: %s \nError_threshold: %s \nError_occurence: %s \nReconnection_time: %s \nReconnection_interval: %s \nException_types: %s' % (
                str(self.flag), str(self.flag_reconnection_started), str(self.error_threshold),
                str(self.error_occurrence),
                str(self.reconnection_time), str(self.reconnection_interval), str(self.exception_types)))

    def getFlag(self):
        return self.flag

    def setFlag(self, flag):
        self.flag = flag

    def getFlagReconnection(self):
        return self.flag_reconnection_started

    def increment_error_occurrence(self):
        self.error_occurrence = self.error_occurrence + 1

    def reset_values(self):
        self.flag = True
        self.flag_reconnection_started = False
        self.error_occurrence = 0


# CHECK FOR CREATED CIRCUIT BREAKERS - PASTE INTO CONNECTION FUNCTION
'''
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
    
    # calling thread should be outside of check_breaker method
    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])
    if mod.__name__ != 'app.circuit_breaker' and cb.getFlagReconnection():
        return '500'

    print('Module name is: ' + mod.__name__)
    return cb
'''