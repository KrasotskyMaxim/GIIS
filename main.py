import sys
import logging

from utils import (
    save_result,
    CDAManager,
    BrazenhemManager,
    ByManager,
)


logging.basicConfig(filename='./logs/mylog.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main(coords: tuple):
    logger.debug('coordinates is %s', coords)
    
    graphic_manager = ByManager(coords=coords)    
    save_result(graphic_manager.res_table)

    
if __name__ == '__main__':
    args = sys.argv[1:5]
    coords = tuple(map(lambda x: int(x), args))
    main(coords)
