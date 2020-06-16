from random import randrange

from config import config as net_config
from detector import Detector
from resnet import ResNet
import tensorflow as tf
from PIL import Image
import numpy as np
from env import *
from sort import *
from deepsort import Deep_sort
from deep_sort import nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
import time
import cv2
import os
from Track_manager_v1 import Track_manager
from glob import glob
VOC_CATS = ['__background__','person','non-person','basket']

class Loader():
    def __init__(self):
        cats = VOC_CATS
        self.cats_to_ids = dict(map(reversed, enumerate(cats)))
        self.ids_to_cats = dict(enumerate(cats))
        self.num_classes = len(cats)
        self.categories = cats[1:]

class Bliznet_detector():
    def __init__(self):
        self.net = ResNet(config=net_config, depth=50, training=False)
        self.loader = Loader()
        self.model = MODEL_PATH
        self.no_seg_gt = NO_SEG_GT
        self.sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
                                                log_device_placement=True))
        self.detector = Detector(self.sess, self.net, self.loader, net_config, no_gt=self.no_seg_gt)
        self.detector.restore_from_ckpt(self.model)
        self.metric = nn_matching.NearestNeighborDistanceMetric(
            "cosine", 0.2, 100)
        self.tracker = Tracker(self.metric)



    def detect(self,img):
        pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        pil_img = np.array(pil_img) / 255.0
        pil_img = pil_img.astype(np.float32)
        h, w = pil_img.shape[:2]
        result,feature_full = self.detector.feed_forward(img=pil_img, name=None, w=w, h=h, draw=False,
                                            seg_gt=None, gt_bboxes=None, gt_cats=None)

        bboxes = result[0]
        score = result[1]
        cats = result[2]
        dets = []
        basket = []
        detections = []
        for i in range(len(bboxes)):
            if cats[i] == 2:
                continue
            if cats[i] == 3:
                x_min = bboxes[i][0]
                y_min = bboxes[i][1]
                x_max = x_min + bboxes[i][2]
                y_max = y_min + bboxes[i][3]
                basket.append([x_min, y_min, x_max, y_max, score[i]])
            else:
                x_min = bboxes[i][0]
                y_min = bboxes[i][1]
                x_max = x_min + bboxes[i][2]
                y_max = y_min + bboxes[i][3]
                dets.append([x_min, y_min, x_max, y_max, score[i]])
                if not sort:
                    pil_img_box = img[int(y_min):int(y_max), int(x_min):int(x_max), :]
                    pil_img_box = Image.fromarray(cv2.cvtColor(pil_img_box, cv2.COLOR_BGR2RGB))
                    pil_img_box = np.array(pil_img_box) / 255.0
                    pil_img_box = pil_img_box.astype(np.float32)
                    h_box, w_box = pil_img_box.shape[:2]
                    result_box, feature = self.detector.feed_forward(img=pil_img_box, name=None, w=w_box, h=h_box, draw=False,
                                                                      seg_gt=None, gt_bboxes=None, gt_cats=None)
                    feature = feature[0, 0, 0, :]
                    feature = np.reshape(feature, (-1, 16))
                    feature = feature.mean(1)
                    detection = Detection(bboxes[i], score[i], feature)
                    detections.append(detection)
        dets = np.asarray(dets)
        if sort:
            return dets,basket
        else:
            return detections,basket
def get_video_input():
    base_path = video_folder
    files = []
    for r, d, f in os.walk(base_path):
        for file in f:
            if 'CAM_360.mp4' in file:
                files.append(os.path.join(r, file))
    return files

def main():
    detector = Bliznet_detector()
    track_manager = Track_manager()
    # all_videos = get_video_input()

    for _ in range(1):
        deepsort = Deep_sort()
        mot_tracker = Sort()
        video = cv2.VideoCapture(video_input)
        # name_video = os.path.basename(video_input)
        name_video = video_input.split("/")[-2]
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frames_per_second = video.get(cv2.CAP_PROP_FPS)
        num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        fourcc = cv2.VideoWriter_fourcc(*'MPEG')

        ROI_thresshold = 0.08665
        ROI = [int(ROI_thresshold * width), 0, int(width * (1 - ROI_thresshold)), height]
        # videoWriter = cv2.VideoWriter('{}_result.mp4'.format(name_video), fourcc, frames_per_second, (ROI[2] - ROI[0], height))
        videoWriter = cv2.VideoWriter('{}_result.mp4'.format(name_video), fourcc, frames_per_second, (512, 512))
        #videoWriter = cv2.VideoWriter('video_result.mp4', fourcc, frames_per_second, (width, height))
        total_time = 0
        colours = np.random.randint(0, 256, size=(32, 3))
        for frame_index in range(num_frames):
            frame_index += 1
            start_time = time.time()
            ret, img = video.read()
            img = cv2.resize(img,(512,512))
            # x_min = ROI[0]
            # y_min = ROI[1]
            # x_max = ROI[2]
            # y_max = ROI[3]
            # img = img[y_min:y_max, x_min:x_max, :]
            dets,basket = detector.detect(img)
            if sort:
                trackers,local_ID_enter,local_ID_exit,local_ID_completed = mot_tracker.update(dets)
            else:
                trackers = deepsort.predict(dets)

            # cv2.polylines(img, np.array([INDOOR], np.int32), True, (0, 0, 255), thickness=2)
            # cv2.polylines(img, np.array([OUTDOOR], np.int32), True, (0, 0, 255), thickness=2)
            #Draw result
            # if len(local_ID_enter) > 0:
            #     cv2.putText(img, 'Entered: {}'.format(local_ID_enter), (150, 482), 0, fontScale=1, color=(0, 255, 0),
            #                 thickness=2)
            # if len(local_ID_exit) > 0:
            #     cv2.putText(img, 'Exited: {}'.format(local_ID_exit), (150, 300), 0, fontScale=1, color=(255, 0, 0),
            #                 thickness=2)
            # if len(local_ID_completed) > 0:
            #     cv2.putText(img, 'Completed: {}'.format(local_ID_completed), (150, 150), 0, fontScale=1,
            #                 color=(255, 255, 255),
            #                 thickness=2)
            #Draw person
            with open(os.path.join(test_tracking_folder,'%s.txt' % (name_video)), 'a+') as out_file:
                for d in trackers:
                    # print('%d,%d,%.2f,%.2f,%.2f,%.2f,1,-1,-1,-1' % (frame_index, d[4], d[0], d[1], d[2] - d[0], d[3] - d[1]),
                    #       file=out_file)
                    tl = 2
                    c1, c2 = (int(d[0]), int(d[1])), (int(d[2]), int(d[3]))
                    color = colours[int(d[4]) % 32].tolist()
                    cv2.rectangle(img, c1, c2, color, thickness=tl)
                    # Plot score
                    thickness = max(tl - 1, 1)  # font thickness
                    label = '%d' % int(d[4])
                    t_size = cv2.getTextSize(label, 0, fontScale=tl / 4, thickness=thickness)[0]
                    c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
                    cv2.rectangle(img, c1, c2, color, -1)  # filled
                    cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 4, [0, 0, 0], thickness=thickness,
                                        lineType=cv2.LINE_AA)
            #Draw basket
            for b in basket:
                tl = 1
                c1, c2 = (int(b[0]), int(b[1])), (int(b[2]), int(b[3]))
                # color_basket = colours[randrange(100) % 32].tolist()
                color_basket = [255,255,255]
                cv2.rectangle(img, c1, c2, color_basket, thickness=tl)
                # Plot score
                thickness = max(tl - 1, 1)  # font thickness
                label = 'basket: %.2f %%' % (100*b[4])
                t_size = cv2.getTextSize(label, 0, fontScale=tl / 4, thickness=thickness)[0]
                c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
                cv2.rectangle(img, c1, c2, color_basket, -1)  # filled
                cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 4, [0, 0, 0], thickness=thickness,
                            lineType=cv2.LINE_AA)

            videoWriter.write(img)
            print('FPS: {:.2f} ___________Follow___________ Frame: {:d}'.format(1 / (time.time() - start_time),
                                                                                        frame_index + 1))
            cycle_time = time.time() - start_time
            total_time += cycle_time
            cv2.putText(img, 'Frame {:d} - {:.2f}ms'.format(frame_index + 1, (time.time() - start_time) * 1000),
                        (30, 30), 0,
                        fontScale=1, color=(0, 255, 0), thickness=2)

        print("Total Time_systems took: %.3f for %d frames or %.1f FPS" % (
            total_time, num_frames, num_frames / total_time))
        print('Done')
if __name__ == '__main__':
    main()