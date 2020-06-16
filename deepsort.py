from deep_sort import nn_matching
from deep_sort.tracker import Tracker
class Deep_sort(object):
    def __init__(self):
        self.max_cosine_distance = 0.2
        self.nn_budget = 100
        self.metric = nn_matching.NearestNeighborDistanceMetric(
            "cosine", self.max_cosine_distance, self.nn_budget)
        self.tracker = Tracker(self.metric)
        self.feature = None

    def predict(self,detections):
        results = []
        self.tracker.predict()
        self.tracker.update(detections)

        # Store results.
        for track in self.tracker.tracks:
            if not track.is_confirmed() or track.time_since_update > 1:
                continue
            bbox = track.to_tlbr()
            results.append([bbox[0], bbox[1], bbox[2], bbox[3], track.track_id])
        return results

