import logging
import sys


log_filename = "{}.log".format(sys.argv[0])
log_entry_format = '%(asctime)s ::: %(levelname)s ::: %(name)s ::: %(message)s'
output_message_format = '%(levelname)s ::: %(name)s ::: %(message)s'

logging.basicConfig(filename=log_filename, filemode='w',
                    format=log_entry_format,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)

console = logging.StreamHandler()
console.setLevel(logging.INFO)

formatter = logging.Formatter(output_message_format)
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

logging.debug("Started helpers.logger")
