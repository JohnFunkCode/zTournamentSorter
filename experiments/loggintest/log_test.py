import logging

import log_test2

def main():
    # Configure the logging system
    # logging.basicConfig(filename='app.log',
    #                     level=logging.ERROR)
    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(format='%(asctime)s %(levelname)s - %(message)s',level=logging.DEBUG,datefmt='%H:%M:%S')
    # Variables (to make the calls that follow work)
    hostname = 'www.python.org'
    item = 'spam'
    filename = 'data.csv'
    mode = 'r'

    # Example logging calls (insert into your program)
    logging.critical('Host %s unknown', hostname)
    logging.error("Couldn't find %r", item)
    logging.warning('Feature is deprecated')
    logging.info('Opening file %r, mode = %r', filename, mode)
    logging.debug('Got here')
    foo()
    log_test2.bar()


def foo():
    logging.info('this is from foo')

if __name__ == '__main__':
    main()
