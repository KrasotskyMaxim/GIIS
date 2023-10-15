import json
from collections import defaultdict


def save_result(result: dict, filename='result'):
    with open(filename+'.json', 'w') as f:
        json.dump(result, f, indent=4)


class GraphicManager:
    def __init__(self, coords: tuple):
        self.coords = coords
        self.res_table = {}
        self._calc_coords()
    
    def _calc_coords(self):
        pass


class CDAManager(GraphicManager):
    def _calc_coords(self):
        x1, y1, x2, y2 = self.coords
        length = max([x2 - x1, y2 - y1])
        dx, dy = x2 / length, y2 / length
        x = x1 + 0.5 * self._sign(dx)
        y = y1 + 0.5 * self._sign(dy)
        self.res_table[0] = {'x': x, 'y': y, 'plot': (int(x), int(y))}
        for i in range(1, length+1):
            x = x + dx
            y = y + dy
            self.res_table[i] = {'x': x, 'y': y, 'plot': (int(x), int(y))}
 
    @staticmethod
    def _sign(x: int|float):
        return 1 if x > 0 else (-1 if x < 0 else 0)
    
    
class BrazenhemManager(GraphicManager):
    def _calc_coords(self):
        x1, y1, x2, y2 = self.coords
        dx, dy = x2 - x1, y2 - y1
        e, de = None, 2 * dy - dx
        x, y = x1, y1
        self.res_table[0] = {'e': e, 'x': x, 'y': y, 'e`': de, 'plot': (int(x), int(y))}
        for i in range(1, dx+1):
            e = de
            if de >= 0:
                y = y + 1
                de = de - 2 * dx
            
            x = x + 1
            de = de + 2 * dy
            self.res_table[i] = {'e': e, 'x': x, 'y': y, 'e`': de, 'plot': (int(x), int(y))}

    
class ByManager(GraphicManager):
    def __init__(self, coords: dict):
        self.coords = coords
        self.res_table = defaultdict(dict)
        self._calc_coords()
        
    def _calc_coords(self):
        x1, y1, x2, y2 = self.coords
        if x2 < x1:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        dx, dy = x2 - x1, y2 - y1
        grad = dy / dx
        
        # process start point
        xstart = int(x1)
        yend = y1 + grad * (xstart - x1)
        xgap = 1 - (x1 + 0.5) % 1
        xpxl1 = xstart  # will use in loop
        ypxl1 = int(yend // 1)
        c = 1 - (yend % 1 * xgap)
        self.res_table[0]['main'] = {'x': xpxl1, 'y': ypxl1, 'c': c, 'plot': (xpxl1, ypxl1, c)}
        
        c = yend % 1 * xgap
        self.res_table[0]['cx'] = {'x': xpxl1, 'y': ypxl1, 'c': c, 'plot': (xpxl1, ypxl1 + 1, c)}
        self.res_table[0]['cy'] = None        
        
        intery = yend + grad # first y-intersection for loop

        # process end point
        xend = int(x2)
        yend = y2 + grad * (xend - x2)
        xgap = (x2 + 0.5) % 1
        xpxl2 = xend  # will use in loop
        ypxl2 = int(yend // 1)
        
        for i, x in enumerate(range(xstart + 1, xend - 1), start=1):
            c = 1 - intery % 1
            self.res_table[i]['main'] = {'x': x, 'y': intery, 'c': c, 'plot': (x, int(intery // 1), c)}    
            
            c = intery % 1
            self.res_table[i]['cx'] = {'x': x, 'y': intery, 'c': c, 'plot': (x, int(intery // 1) + 1, c)}  
            self.res_table[i]['cy'] = None  
            intery = intery + grad
            
        xrange = xend - xstart
        c = 1 - (yend % 1 * xgap)
        self.res_table[xrange - 1]['main'] = {'x': xpxl2, 'y': ypxl2, 'c': c, 'plot': (xpxl2, ypxl2, c)}
        
        c = yend % 1 * xgap
        self.res_table[xrange - 1]['cx'] = {'x': xpxl2, 'y': ypxl2, 'c': c, 'plot': (xpxl2, ypxl2 + 1, c)}
        self.res_table[xrange - 1]['cy'] = None
