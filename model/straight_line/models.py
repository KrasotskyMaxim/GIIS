from collections import defaultdict
import math


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
    
    @property
    def _c(self):
        return []
    

class CDAManager(GraphicManager):
    def _calc_coords(self):
        x1, y1, x2, y2 = self.raw_coords
        length = max([abs(x2 - x1), abs(y2 - y1)])
        if length != 0:
            dx, dy = (x2 - x1) / length, (y2 - y1) / length
        else:
            dx, dy = 0, 0
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
    
    def _round(self, x):
        return math.floor(x + 0.5)
    
    def _fpart(self, x):
        return x - math.floor(x)

    def _rfpart(self, x):
        return 1 - self._fpart(x)
    
    def _calc_coords(self):
        if self._can_be_CDA():
            self.by_cda = True
            cda_manager = CDAManager(self.raw_coords)
            self.res_table = cda_manager.res_table
            return

        x1, y1, x2, y2 = self.raw_coords
        steep = abs(y2 - y1) > abs(x2 - x1)
        
        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2 
        
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        
        dx, dy = x2 - x1, y2 - y1
        
        if dx == 0.0:
            grad = 1.0
        else:
            grad = dy / dx
        
        # process start point
        xend = self._round(x1)
        yend = y1 + grad * (xend - x1)
        xgap = self._rfpart(x1 + 0.5)
        xpxl1 = xend  # will use in loop
        ypxl1 = math.floor(yend)

        if steep:
            c = round(self._rfpart(yend) * xgap, 2) or 1.0
            self.res_table[0] = {'x': ypxl1, 'y': xpxl1, 'c': c, 'plot': (ypxl1, xpxl1)}
            c = round(self._fpart(yend) * xgap, 2)  or 1.0
            self.res_table[1]= {'x': ypxl1 + 1, 'y': xpxl1, 'c': c, 'plot': (ypxl1 + 1, xpxl1)}        
        else:
            c = round(self._rfpart(yend) * xgap, 2) or 1.0
            self.res_table[0] = {'x': xpxl1, 'y': ypxl1, 'c': c, 'plot': (xpxl1, ypxl1)}
            c = round(self._fpart(yend) * xgap, 2) or 1.0
            self.res_table[1] = {'x': xpxl1, 'y': ypxl1 + 1, 'c': c, 'plot': (xpxl1, ypxl1 + 1)}        
        
        intery = yend + grad # first y-intersection for loop

        # process end point
        xend = self._round(x2)
        yend = y2 + grad * (xend - x2)
        xgap = self._fpart(x2 + 0.5)
        xpxl2 = xend  # will use in loop
        ypxl2 = math.floor(yend)
        
        i = 2
        if steep:
            for z in range(xpxl1 + 1, xpxl2):
                c = round(self._rfpart(intery), 2) or 1.0
                self.res_table[i] = {'x': math.floor(intery), 'y': z, 'c': c, 'plot': (math.floor(intery), z)}        
                i += 1
                c = round(self._fpart(yend) * xgap, 2)  or 1.0
                self.res_table[i] = {'x': math.floor(intery) + 1, 'y': z, 'c': c, 'plot': (math.floor(intery) + 1, z)}        
                intery += grad
                i += 1
        else:
            for z in range(xpxl1 + 1, xpxl2):
                c = round(self._rfpart(intery), 2) or 1.0
                self.res_table[i] = {'x': z, 'y': math.floor(intery), 'c': c, 'plot': (z, math.floor(intery))}        
                i += 1
                c = round(self._fpart(yend), 2)  or 1.0
                self.res_table[i] = {'x': z, 'y': math.floor(intery) + 1, 'c': c, 'plot': (z, math.floor(intery) + 1)}        
                intery += grad
                i += 1
        
        if steep:
            c = round(self._rfpart(yend) * xgap, 2) or 1.0
            self.res_table[i] = {'x': ypxl2, 'y': xpxl2, 'c': c, 'plot': (ypxl2, xpxl2)}
            c = round(self._fpart(yend) * xgap, 2)  or 1.0
            self.res_table[i+1]= {'x': ypxl2 + 1, 'y': xpxl2, 'c': c, 'plot': (ypxl2 + 1, xpxl2)}        
        else:
            c = round(self._rfpart(yend) * xgap, 2) or 1.0
            self.res_table[i] = {'x': xpxl2, 'y': ypxl2, 'c': c, 'plot': (xpxl2, ypxl2)}
            c = round(self._fpart(yend) * xgap, 2)  or 1.0
            self.res_table[i+1] = {'x': xpxl2, 'y': ypxl2 + 1, 'c': c, 'plot': (xpxl2, ypxl2 + 1)}        
        
    @property
    def _c(self):
        return [coords.get('c') for coords in self.res_table.values()]
    
    def __str__(self):
        return 'By'