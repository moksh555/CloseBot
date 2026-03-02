import logging

SERVICE_LOG_FILE_PATH = "./allLogs/serviceLogs.log"
API_LOG_FILE_PATH =  "./allLogs/apiLogs.log"


# LOGS CALLER FOR API SIDE
APIlogger = logging.getLogger("api_logger")
APIlogger.setLevel(logging.DEBUG)
format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

## This is file handler for real logs 
apiFileHandler = logging.FileHandler(API_LOG_FILE_PATH)
apiFileHandler.setLevel(logging.INFO)
apiFileHandler.setFormatter(format)
APIlogger.addHandler(apiFileHandler)

# ## This will be my stream handler
# apiStreamHandler = logging.StreamHandler()
# apiStreamHandler.setFormatter(format)
# apiStreamHandler.setLevel(logging.DEBUG)
# APIlogger.addHandler(apiStreamHandler)


#LOGS CALLER FOR SERVICE SIDE
ServiceLogger = logging.getLogger("service_logger")
ServiceLogger.setLevel(logging.INFO)
format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

## Settings File Handler Service Logger
serviceFileHandler = logging.FileHandler(SERVICE_LOG_FILE_PATH)
serviceFileHandler.setLevel(logging.INFO)
ServiceLogger.addHandler(serviceFileHandler)

# ## Settings Stream Handler Service Logger
# serviceStreamHandler = logging.StreamHandler()
# serviceFileHandler.setLevel(logging.DEBUG)
# ServiceLogger.addHandler(serviceStreamHandler)
