import logging
import os


__all__ = ["logger"]


logger = logging.getLogger()

if not os.path.exists("log"):
    os.mkdir("log")
