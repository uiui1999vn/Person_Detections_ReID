from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from env import *
import time
class Tracker(object):
    def __init__(self):
        self.id = None
        self.start_locations = None
        self.end_locations = None
        self.current_locations = None
        self.start_time =  None
        self.end_time = None
        self.is_enter = False
        self.is_exit = False
        self.is_completed = False

class Track_manager(object):
    def __init__(self):
        self.indoor = Polygon(INDOOR)
        self.outdoor = Polygon(OUTDOOR)
        self.match_ID = dict()
        self.dict_area = dict()
        self.dict_timestemp = dict()
        self.dict_area["indoor"] = []
        self.dict_area["outdoor"] = []

    def in_area(self,box, entrance):
        x_min = box[0]
        y_min = box[1]
        x_max = box[2]
        y_max = box[3]
        # box_Plolygon = Polygon([(x_min, y_min), (x_max, y_min), (x_max, y_max),(x_min,y_max)])
        #         # intersec = box_Plolygon.intersection(entrance).area
        #         # if intersec >= intersec_thresshold*box_Plolygon.area:
        #         #     return True
        #         # else:return False
        center = Point((x_max + x_min) / 2, (y_max + y_min) / 2)
        if Polygon(I).contains(center):
            foot = Point(x_min, y_max)
        elif Polygon(IV).contains(center):
            foot = Point(x_min, y_min)
        else:
            foot = center
        if entrance.contains(foot):
            return True
        else:
            return False
    def centroid(self,box):
        x_min = box[0]
        y_min = box[1]
        x_max = box[2]
        y_max = box[3]
        box_Plolygon = Polygon([(x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max)])
        return box_Plolygon.centroid

    def create_info(self, trackers, dead_track):
        "____________-Check enter exit________________"
        self.local_ID_enter = []
        self.local_ID_exit = []
        self.local_ID_completed = []

        for trk in trackers:
            if trk[-1] not in self.dict_timestemp.keys():
                track = Tracker()
                track.id = trk[-1]
                track.start_time = time.clock()
                track.start_locations = trk[:4]
                track.current_locations = trk[:4]
                track.end_time = 1e10
                self.dict_timestemp[trk[-1]] = track
                if self.in_area(trk, self.indoor):
                    if trk[-1] not in self.dict_area["indoor"]:
                        self.dict_area["indoor"].append(trk[-1])
                    if trk[-1] in self.dict_area.get("outdoor"):
                        self.local_ID_enter.append(trk[-1])
                        self.dict_timestemp[trk[-1]].is_enter = True
                        self.dict_area["indoor"].remove(trk[-1])
                        self.dict_area["outdoor"].remove(trk[-1])
                elif self.in_area(trk, self.outdoor):
                    if trk[-1] not in self.dict_area["outdoor"]:
                        self.dict_area["outdoor"].append(trk[-1])
                    if trk[-1] in self.dict_area.get("indoor"):
                        self.local_ID_exit.append(trk[-1])
                        self.dict_timestemp[trk[-1]].is_exit = True
                        self.dict_area["indoor"].remove(trk[-1])
                        self.dict_area["outdoor"].remove(trk[-1])
                # if self.in_area(trk,self.indoor) and self.dict_timestemp[trk[-1]].is_enter == False or self.dict_timestemp[trk[-1]].is_exit == False:
                if self.dict_timestemp[trk[-1]].is_completed == False or self.in_area(trk,self.indoor):
                    self.ReID_by_locations(track)

            self.dict_timestemp[trk[-1]].current_locations = trk[:4]
            if self.dict_timestemp[trk[-1]].is_enter == True and self.dict_timestemp[trk[-1]].is_exit == True:
                self.dict_timestemp[trk[-1]].is_completed = True
                self.local_ID_completed.append(self.dict_timestemp[trk[-1]].id)
                # self.dict_timestemp.pop(trk[-1])

        for trk in dead_track:
            if trk[0][-1] in self.dict_timestemp.keys():
                self.dict_timestemp[trk[0][-1]].end_time = time.clock()
                self.dict_timestemp[trk[0][-1]].end_locations = trk[0][:4]



    def find_candidate_ID(self, track):
        cadidate_ID = []
        #fine candidate_ID by time stamp
        for id in self.dict_timestemp.keys():
            if self.dict_timestemp[id].end_time < track.start_time:
                cadidate_ID.append(id)
        return cadidate_ID


    def ReID_by_timestemp(self,track):
        "_____ReID by time stemp_________"

        candidate_IDs = self.find_candidate_ID(track)
        candidate_ID = track.id
        min_distance_time = 1e10
        for id in candidate_IDs:
            time_distance = track.end_time -  self.dict_timestemp[id].end_time
            if abs(time_distance) < min_distance_time:
                min_distance_time = time_distance
                candidate_ID = id
        self.match_ID[track.id] = candidate_ID
        self.dict_timestemp[candidate_ID].end_time = 1e10


    def ReID_by_locations(self,track):
        "_____ReID by locations_________"
        candidate_IDs = self.find_candidate_ID(track)
        candidate_ID = track.id
        min_distance_locations = 1e10
        for id in candidate_IDs:
            distance_locations = self.centroid(track.current_locations).distance(self.centroid(self.dict_timestemp[id].end_locations))
            if abs(distance_locations) < min_distance_locations:
                min_distance_locations = distance_locations
                candidate_ID = id
        self.match_ID[track.id] = candidate_ID
        self.dict_timestemp[candidate_ID].end_time = 1e10

    def update_ID(self,trackers,dead_track):
        self.create_info(trackers, dead_track)
        return self.match_ID,self.local_ID_enter,self.local_ID_exit,self.local_ID_completed










