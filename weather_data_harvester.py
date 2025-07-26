"""

    Weather-Data-Harvester
    
    # Python-Version: 3.10.12

"""
import os, time, logging
#
from src.config import *
import src.utils as utils
from src.db_handler import *

def main() -> None:
    _start:float = time.time()
    logging.debug(f"Started at {_start}")
    
    
    
    _delta:float = time.time() - _start
    logging.debug(f"Closed. (Runtime={_delta} seconds)")
    

if __name__ == '__main__':
    main()