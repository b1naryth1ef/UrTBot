import logging, sys
import thread
#from init import config

log = logging.getLogger('global')
FH, SH = (None, None)
logLevels = {
    'DEBUG':logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

#Debug level classifications:
#DEBUG: Lines added in for development
#INFO: Anything you want to put in a print, but not everyone should see
#WARNING: Any small issues, or little problems (not for try/except)
#ERROR: Use in try/except. Large problems that will cause criticals down the road
#CRITICAL: The bot should close after throwing this.

logs = {
    
}
class LoggingError(Exception): pass

def disableLog():
    global log, SH, FH
    log.removeHandler(SH)
    log.removeHandler(FH)

def init(config):
    global log, SH, FH
    try:
        developerConfig = config.developerConfig
        level = logLevels[developerConfig['loglevel'].upper()]
        logfile = developerConfig['logfile']
        status = developerConfig['logging']
        mode = 'w'
    except Exception, e:
        raise Exception("Error in loading logging config... Can't continue on! [%s]" % e)
    
    logging.basicConfig(filename=logfile, level=level, filemode=mode, format='%(asctime)s %(levelname)s [%(module)s #%(lineno)d in %(funcName)s]: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    SH = logging.StreamHandler(sys.stdout)
    FH = logging.FileHandler(logfile)
    log = logging.getLogger('global')
    if status is True:
        log.addHandler(SH)
        log.addHandler(FH)
    log.info('SETUP DONE: Logging')
    return log