import logging
from os import path
from sys import argv

LOGFILE = "./log/%s.log" % path.splitext(path.split(argv[0])[1])[0]

logger = logging.getLogger('GCF_logger')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(LOGFILE,'w')
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

class ErrorCode(object):
    E_MISSING_VM = "MISSING_VM"
    E_MISSING_REPLICA = "MISSING_REPLICA"
    E_WRONG_CLUSTER = "WRONG_CLUSTER"

    

