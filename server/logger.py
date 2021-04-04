import sys
import logging

file_log = logging.FileHandler('debug.log')
console_out = logging.StreamHandler(sys.stdout)

logging.basicConfig(level=logging.INFO,
                    handlers=(file_log, console_out),
                    format=r'%(asctime)s - %(name)s - '
                           '%(pathname)s:%(lineno)d - '
                           '%(levelname)s\n%(message)s\n')

logger = logging.getLogger()
