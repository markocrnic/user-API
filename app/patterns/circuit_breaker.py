import threading
import time


class CircuitBreaker:
    # Parameters with default values
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

    # Check if the error is in expected exception types and if error threshold is reached
    def check_state(self, error, methodToRun):
        if error.__class__.__name__ in self.exception_types:
            if self.error_occurrence < self.error_threshold:
                # If error threshold not yet reached, increment error occurrence
                self.error_occurrence += 1
            else:
                # Error threshold reached, setting flag to False meaning open circuit breaker
                self.flag = False

                if not self.flag_reconnection_started:
                    # If reconnection flag is False, set it to True and start new Thread for reconnection
                    self.flag_reconnection_started = True
                    thread = threading.Thread(target=self.try_reconnection, args=(methodToRun, ))
                    thread.start()
            return str(self.flag)
        else:
            return 'Error not caught in breaker'

    def try_reconnection(self, methodToRun):
        # Wait for set reconnection time and start reconnection
        self.flag_reconnection_started = True
        time.sleep(self.reconnection_time)

        while not self.flag:

            if methodToRun():
                print('\nReconnection is successful. Resetting values.\n')
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


def check_breaker():
    # Check if instance of CB is already created
    global cb
    try:
        cb
    except:
        cb = None
    if cb is None:
        # CB not found, creating new circuit breaker
        cb = CircuitBreaker(2, 0, 10, 5, ['OperationalError'])
    else:
        cb.display()

    return cb
