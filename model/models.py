from collections import defaultdict


class GraphicManager:
    def __init__(self, coords: tuple):
        self.raw_coords = coords
        self.res_table = {}
        self._calc_coords()
    
    def _calc_coords(self):
        pass
    
    @staticmethod
    def _sign(x: int|float):
        return 1 if x > 0 else (-1 if x < 0 else 0)
    
    @property
    def coords(self):
        return [coords['plot'] for coords in self.res_table.values()]
    

class CDAManager(GraphicManager):
    def _calc_coords(self):
        x1, y1, x2, y2 = self.raw_coords
        length = max([abs(x2 - x1), abs(y2 - y1)])
        dx, dy = (x2 - x1) / length, (y2 - y1) / length
        x = round(x1 + 0.5 * self._sign(dx), 2)
        y = round(y1 + 0.5 * self._sign(dy), 2)
        self.res_table[0] = {'x': x, 'y': y, 'plot': (int(x), int(y))}
        for i in range(1, length+1):
            x = round(x + dx, 2)
            y = round(y + dy, 2)
            self.res_table[i] = {'x': x, 'y': y, 'plot': (int(x), int(y))}
 
    def __str__(self):
        return 'CDA'

    
class BrazenhemManager(GraphicManager):
    def _calc_coords(self):
        x1, y1, x2, y2 = self.raw_coords
        dx = x2 - x1
        dy = y2 - y1
        sign_x = self._sign(dx)
        sign_y = self._sign(dy)
        
        if dx < 0: dx = -dx
        if dy < 0: dy = -dy
        
        if dx > dy:
            pdx, pdy = sign_x, 0
            es, el = dy, dx
        else:
            pdx, pdy = 0, sign_y
            es, el = dx, dy
        
        x, y = x1, y1
        error, t = el/2, 0        
        self.res_table[0] = {'x': x, 'y': y, 'e': error, 'plot': (int(x), int(y))}
        
        i = 1
        while t < el:
            error -= es
            if error < 0:
                error += el
                x += sign_x
                y += sign_y
            else:
                x += pdx
                y += pdy
            self.res_table[i] = {'x': x, 'y': y, 'e': error, 'plot': (int(x), int(y))}
            t += 1
            i += 1
        
    def __str__(self):
        return 'Brazenhem'

    
class ByManager(GraphicManager):
    def __init__(self, coords: dict):
        self.raw_coords = coords
        self.res_table = defaultdict(dict)
        self.by_cda = False
        self._calc_coords()
    
    def _can_be_CDA(self):
        x1, y1, x2, y2 = self.raw_coords
        if x1 == x2 or y1 == y2 or abs(x2 - x1) == abs(y2 - y1):
            return True
        return False
    
    def _calc_coords(self):
        if self._can_be_CDA():
            self.by_cda = True
            cda_manager = CDAManager(self.raw_coords)
            self.res_table = cda_manager.res_table
            return

        x1, y1, x2, y2 = self.raw_coords
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
    
    def __str__(self):
        return 'By'