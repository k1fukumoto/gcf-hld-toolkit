import logging

LOGFILE = './log/verify_vm_inventory.log'

logger = logging.getLogger('GCF_logger')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(LOGFILE,'w')
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


