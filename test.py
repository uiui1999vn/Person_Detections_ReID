import time
# import cv2
# import numpy as np
# INDOOR = [(0, 0), (512, 0), (343, 168), (319, 342),(512,512),(0,512)]
# img = cv2.imread(r"E:\Pycharm project\tools\negativexample_10_1ppl_0004.jpg")
# cv2.polylines(img, np.array([INDOOR], np.int32), True, (0, 0, 255), thickness=2)
# cv2.imshow("result",img)
# cv2.waitKey(50000)
# A = dict()
# B = dict()
# dict_timestemp = dict()
# A["start_time"] = 10
# dict_timestemp[2] = A
# dict_timestemp[3] = B
# print(dict_timestemp)
# A["end_time"] = 20
# dict_timestemp[3] = A
# for i in dict_timestemp:
#     print(dict_timestemp[i])

# {4.0: 1.0, 5.0: 4.0, 6.0: 5.0, 7.0: 6.0, 8.0: 7.0, 9.0: 8.0, 10.0: 9.0, 11.0: 10.0, 12.0: 3.0, 13.0: 11.0, 14.0: 2.0, 15.0: 14.0}
from shapely.geometry import Polygon
x_min = 164
y_min = 114
x_max = 247
y_max = 223
a = Polygon([(x_min, y_min), (x_max, y_min), (x_max, y_max),(x_min,y_max)])

b = Polygon([(0, 0), (512, 0), (343, 168), (319, 342),(512,512),(0,512)])

print(a.centroid)

A = [1,8,7,8,5,9]
A.remove(5)
print(A)