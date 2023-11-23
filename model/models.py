import math


class GraphicManager:
    def __init__(self, values: tuple):
        self.raw_values = values
        self.points = []
        self.saturation = []
        self._calc_points()

    def _calc_points(self):
        raise NotImplementedError

    @staticmethod
    def _sign(x: int|float):
        return 1 if x > 0 else (-1 if x < 0 else 0)


class CDAManager(GraphicManager):
    def _calc_points(self):
        x1, y1, x2, y2 = self.raw_values
        length = max([abs(x2 - x1), abs(y2 - y1)])
        if length != 0:
            dx, dy = (x2 - x1) / length, (y2 - y1) / length
        else:
            dx, dy = 0, 0
        x = round(x1 + 0.5 * self._sign(dx), 2)
        y = round(y1 + 0.5 * self._sign(dy), 2)
        self.points.append((int(x), int(y)))
        for i in range(1, length+1):
            x = round(x + dx, 2)
            y = round(y + dy, 2)
            self.points.append((int(x), int(y)))
 
    def __str__(self):
        return 'CDA'


class BrazenhemManager(GraphicManager):
    def _calc_points(self):
        x1, y1, x2, y2 = self.raw_values
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
        self.points.append((int(x), int(y)))
        
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
            self.points.append((int(x), int(y)))
            t += 1
            i += 1
        
    def __str__(self):
        return 'Brazenhem'


class ByManager(GraphicManager):
    def _can_be_cda(self):
        x1, y1, x2, y2 = self.raw_values
        return x1 == x2 or y1 == y2 or abs(x2 - x1) == abs(y2 - y1)

    @staticmethod
    def _round(x):
        return math.floor(x + 0.5)
    
    @staticmethod
    def _fpart(x):
        return x - math.floor(x)

    def _rfpart(self, x):
        return 1 - self._fpart(x)

    def _calc_points(self):
        if self._can_be_cda():
            cda_manager = CDAManager(self.raw_values)
            self.points = cda_manager.points
            return

        x1, y1, x2, y2 = self.raw_values
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
            self.points.append((ypxl1, xpxl1))
            self.saturation.append(c)
            c = round(self._fpart(yend) * xgap, 2)  or 1.0
            self.points.append((ypxl1 + 1, xpxl1))  
            self.saturation.append(c)      
        else:
            c = round(self._rfpart(yend) * xgap, 2) or 1.0
            self.points.append((xpxl1, ypxl1))
            self.saturation.append(c)
            c = round(self._fpart(yend) * xgap, 2) or 1.0
            self.points.append((xpxl1, ypxl1 + 1))
            self.saturation.append(c)        
        
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
                self.points.append((math.floor(intery), z))
                self.saturation.append(c)        
                i += 1
                c = round(self._fpart(yend) * xgap, 2)  or 1.0
                self.points.append((math.floor(intery) + 1, z))
                self.saturation.append(c)        
                intery += grad
                i += 1
        else:
            for z in range(xpxl1 + 1, xpxl2):
                c = round(self._rfpart(intery), 2) or 1.0
                self.points.append((z, math.floor(intery)))
                self.saturation.append(c)        
                i += 1
                c = round(self._fpart(yend), 2)  or 1.0
                self.points.append((z, math.floor(intery) + 1))
                self.saturation.append(c)        
                intery += grad
                i += 1
        
        if steep:
            c = round(self._rfpart(yend) * xgap, 2) or 1.0
            self.points.append((ypxl2, xpxl2))
            self.saturation.append(c)
            c = round(self._fpart(yend) * xgap, 2)  or 1.0
            self.points.append((ypxl2 + 1, xpxl2))
            self.saturation.append(c)        
        else:
            c = round(self._rfpart(yend) * xgap, 2) or 1.0
            self.points.append((xpxl2, ypxl2))
            self.saturation.append(c)
            c = round(self._fpart(yend) * xgap, 2)  or 1.0
            self.points.append((xpxl2, ypxl2 + 1))
            self.saturation.append(c)        

    def __str__(self):
        return 'By'
    

class CircleManager(GraphicManager):
    def _calc_points(self):
        x, y, r = self.raw_values[:3]
        
        if not r:
            return

        dx = 0
        dy = r
        inf = 0
        D = 2 - 2 * r
        
        while dy >= inf:
            self.points.append((x + dx, y + dy))
            self.points.append((x - dx, y + dy))
            self.points.append((x + dx, y - dy))
            self.points.append((x - dx, y - dy))

            if D > 0:
                DD = 2*D - 2*dx - 1
                if DD <= 0:
                    dx += 1
                    dy -= 1
                    D = D + 2*dx - 2*dy + 2
                elif DD > 0:
                    dy -= 1
                    D = D - 2*dy + 1
            elif D == 0:
                dx += 1
                dy =- 1
                D = D + 2*dx - 2*dy + 2
            elif D < 0:
                DD = 2*D + 2*dy - 1
                if DD > 0:
                    dx += 1
                    dy -= 1
                    D = D + 2*dx - 2*dy + 2
                elif DD <= 0:
                    dx += 1
                    D = D + 2*dx + 1


class EllipseManager(GraphicManager):
    def _calc_points(self):
        x, y, a, b = self.raw_values
    
        if not a or not b:
            return
        
        dx = 0
        dy = b
        a_sqr = a * a
        b_sqr = b * b
        D = 4 * b_sqr - 4 * a_sqr * b + a_sqr

        while a_sqr * (2 * dy - 1) > 2 * b_sqr * (dx + 1):
            self.points.append((x + dx, y + dy))
            self.points.append((x - dx, y + dy))
            self.points.append((x + dx, y - dy))
            self.points.append((x - dx, y - dy))

            if D < 0:
                D += 4 * b_sqr * (2 * dx + 3)
            else:
                D += 4 * b_sqr * (2 * dx + 3) - 4 * a_sqr * (2 * dy - 2)
                dy -= 1
            dx += 1

        D = b_sqr * (2 * dx + 1) * (2 * dx + 1) + 4 * a_sqr * (dy - 1) * (dy - 1) - 4 * a_sqr * b_sqr

        while dy >= 0:
            self.points.append((x + dx, y + dy))
            self.points.append((x - dx, y + dy))
            self.points.append((x + dx, y - dy))
            self.points.append((x - dx, y - dy))

            if D < 0:
                D += 4 * b_sqr * (2 * dx + 2) + a_sqr * (3 - 4 * dy)
                dx += 1
            else:
                D += 4 * a_sqr * (3 - 2 * dy)
            dy -= 1


class HyperballManager(GraphicManager):
    def _calc_points(self):
        x, y, a, b = self.raw_values
        ppoints = []
        mpoints = []
        for i in range(-x, x + 1):
            j = y + int(b * math.sqrt(1 + (i/a)**2))
            tj = j
            ppoints.append((i, j))
            mpoints.append((i, -j))
        ppoints = self.calc_skipped_points(ppoints)
        mpoints = self.calc_skipped_points(mpoints)
        self.points = ppoints + mpoints
            
    def calc_skipped_points(self, points):
        plen = len(points)
        i = 0
        for _ in range(plen):
            if i >= len(points) - 1:
                continue

            maxy = max([points[i][1], points[i+1][1]])
            miny = min([points[i][1], points[i+1][1]])
            
            ni = i + 1
            while miny < maxy - 1:
                miny += 1
                points.insert(ni, (points[i][0]+1, miny))
                ni += 1
                 
            i = ni
        return points


class ParaballManager(GraphicManager):
    def _calc_points(self):
        x, a, b, c = self.raw_values
        for i in range(-x, x + 1):
            y = int(a * i**2 + b*i + c)
            self.points.append((i, y))
        self.calc_skipped_points()
    
    def calc_skipped_points(self):
        plen = len(self.points)
        i = 0
        for _ in range(plen):
            if i >= len(self.points) - 1:
                continue

            maxy = max([self.points[i][1], self.points[i+1][1]])
            miny = min([self.points[i][1], self.points[i+1][1]])
            
            ni = i + 1
            while miny < maxy - 1:
                miny += 1
                self.points.insert(ni, (self.points[i][0]+1, miny))
                ni += 1
                 
            i = ni
