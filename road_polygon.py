#! /usr/bin/python
# Takes a list of (x, y) points, assuming ordering similar to and osm or rectangular
# point cloud with close pairs of points.
# Returns points ordered counter-clockwise

# METHOD: Sorts all points from left to right, starts at leftmost point,
# looks 3 points ahead and picks point with least angle. Jumps to that point
# and repeats the process until the leftmost point, then reverses the process

# NOTE: Need to create a visualization for verification


import operator
import math

    # Fuse all points closer than d
    def fuse(self, points, d):
        def dist2(p1, p2):
            return ((p1[0] - p2[0])**2 +  (p1[1] - p2[1])**2)
        ret = []
        d2 = d * d
        n = len(points)
        taken = [False] * n
        for i in range(n):
            if not taken[i]:
                count = 1
                point = [points[i][0], points[i][1]]
                taken[i] = True
                for j in range(i + 1, n):
                    if dist2(points[i], points[j]) < d2:
                        point[0] += points[j][0]
                        point[1] += points[j][1]
                        count += 1
                        taken[j] = True
                point[0] /= count
                point[1] /= count
                ret.append((point[0], point[1]))
        return ret

    def road_polygon(self, points):
        i = 0
        pts_dict = {}
        ccw_ord_pts = []
        x_sorted_non_fused = sorted(points, key=operator.itemgetter(0))
        x_sorted = self.fuse(x_sorted_non_fused, 0.5)
        xmin = x_sorted[0][0]
        xmax = x_sorted[-1][0]
        origin = x_sorted[0]
        ccw_ord_pts.append(origin)
        # Traversing left to right
        while origin[0] != xmax:
            try:
                next_pts = x_sorted[i+1:i+4]
            except IndexError:
                try:
                    next_pts = [x_sorted[i+1:i+3]]
                except IndexError:
                    # This should be max and loop should exit
                    ccw_ord_pts.append(x_sorted[i+1])
                    origin = x_sorted[i+1]
            angles = [math.atan2(pt[1] - origin[1], pt[0] - origin[0])\
                    for pt in next_pts]
            # Converting 0 to left side
            angles = map(math.degrees, angles)
            pts_dict = {angles[j]: next_pts[j] for j in range(len(angles))}
            origin = pts_dict[min(angles)]
            i += next_pts.index(origin) + 1
            ccw_ord_pts.append(origin)

        x_sorted = sorted(x_sorted, key=operator.itemgetter(0), reverse=True)
        origin = x_sorted[0]
        i = 0
        # Traversing right to left
        while origin[0] != xmin:
            try:
                next_pts = x_sorted[i+1:i+4]
            except IndexError:
                try:
                    next_pts = [x_sorted[i+1:i+3]]
                except IndexError:
                    # This should be max and loop should exit
                    origin = x_sorted[i+1]

            angles = [math.atan2(pt[1] - origin[1], pt[0] - origin[0])\
                    for pt in next_pts]
            angles = map(math.degrees, angles)
            angles = [ang + 360 if ang < 0 else ang for ang in angles]
            pts_dict = {angles[j]: next_pts[j] for j in range(len(angles))}
            origin = pts_dict[min(angles)]
            i += next_pts.index(origin) + 1
            ccw_ord_pts.append(origin)

        print("Returning: %s" % ccw_ord_pts)
        return ccw_ord_pts
