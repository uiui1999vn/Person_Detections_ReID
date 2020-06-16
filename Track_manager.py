from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from env import *
import time

class Track_manager(object):
    def __init__(self):
        self.indoor = Polygon(INDOOR)
        self.outdoor = Polygon(OUTDOOR)
        self.match_ID = dict()
        self.dict_area = dict()
        self.dict_timestemp = dict()
        self.dict_area["indoor"] = []
        self.dict_area["outdoor"] = []


    def in_area(self,box, area):
        x_min = box[0]
        y_min = box[1]
        x_max = box[2]
        y_max = box[3]

        center = Point((x_max + x_min) / 2, (y_max + y_min) / 2)
        if Polygon(I).contains(center):
            foot = Point(x_min,y_max)
        elif Polygon(IV).contains(center):
            foot = Point(x_min, y_min)
        else: foot = center
        if area.contains(foot):
            return True
        else:
            return False
    def add_localID_to_dict(self,trackers, dead_track):
        localID_dead = []
        dict_time = dict()
        for trk in dead_track:
            localID_dead.append(trk[0][-1])
        for trk in trackers:
            if self.in_area(trk, self.indoor):
                if trk[-1] not in self.dict_area["indoor"]:
                    self.dict_area["indoor"].append(trk[-1])
            elif self.in_area(trk, self.outdoor):
                if trk[-1] not in self.dict_area["outdoor"]:
                    self.dict_area["outdoor"].append(trk[-1])
            if trk[-1] not in self.dict_timestemp.keys() and self.in_area(trk,self.outdoor):
                dict_time["start_time"] = time.clock()
                dict_time["end_time"] = 1000000
                self.dict_timestemp[trk[-1]] = dict_time
            elif trk[-1] not in self.dict_timestemp.keys() and self.in_area(trk,self.indoor):
                dict_time["start_time"] = time.clock()
                dict_time["end_time"] = 1000000
                self.dict_timestemp[trk[-1]] = dict_time
                self.ReID(trk[-1])
            if len(localID_dead)> 0:
                for id in localID_dead:
                    self.dict_timestemp[id]["end_time"] = time.clock()
        # print(self.dict_timestemp)
    def ReID(self,id):
        min_time_distance = 1000000
        candidate_id = id
        for i in self.dict_timestemp:
            current_time = time.clock()
            time_distance = current_time - self.dict_timestemp[i]["end_time"]
            if abs(time_distance) < min_time_distance:
                min_time_distance = time_distance
                candidate_id = i
        self.match_ID[id] = candidate_id

    def update_ID(self,trackers,dead_track):
        self.add_localID_to_dict(trackers, dead_track)
        return self.match_ID

    def check_enter_exit(self,trackers,dead_track):
        self.local_ID_enter = []
        self.local_ID_exit = []
        self.add_localID_to_dict(trackers,dead_track)

        for trk in trackers:
            if self.in_area(trk,self.indoor) and trk[-1] in self.dict_area.get("outdoor"):
                self.local_ID_enter.append(trk[-1])
            if self.in_area(trk, self.outdoor) and trk[-1] in self.dict_area.get("indoor"):
                self.local_ID_exit.append(trk[-1])
        return self.local_ID_enter,self.local_ID_exit, self.match_ID










