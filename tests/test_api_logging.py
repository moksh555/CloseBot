import pytest
from src.app.logs.logs import APIlogger

def test_api_logging():

    APIlogger.info("This is an info message (will show in console)")
    APIlogger.debug("This is a debug message (won't show in console due to handler level)")