# -*- coding: utf-8 -*-
from loguru import logger
from sys import stderr

#### LOGGER SETTING ####
logger.remove()
logger.add(sink=stderr, backtrace=True, diagnose=True,
           format="<white>{time:HH:mm:ss}</white>"
                  " | <level>{level: <8}</level>"
                  " - <white>{message}</white>")
