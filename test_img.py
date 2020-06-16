from sort import *
import cv2
from env import *
from Track_manager import Track_manager
from  Track_manager_v1 import  Track_manager

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='SORT demo')
    parser.add_argument('--display', dest='display', help='Display online tracker output (slow) [False]',
                        action='store_true')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    # all train


    sequences = ['tracking_Toppan_15_05_20_cuts_sce09']
    args = parse_args()
    display = args.display
    phase = 'train'
    total_time = 0.0
    total_frames = 0
    colours = np.random.rand(32, 3)  # used only for display
    videoWriter = cv2.VideoWriter('result.mp4', cv2.VideoWriter_fourcc(*'MPEG'), 50, (512, 512))
    for seq in sequences:
        mot_tracker = Sort()  # create instance of the SORT tracker
        track_manager = Track_manager()
        seq_dets = np.loadtxt(r'E:\Pycharm project\blitznet\Results\tracking_Toppan_15_05_20_case_24\gt\gt.txt', delimiter=',')  # load detections
        frames = seq_dets[:,0].astype(int)
        with open('output/%s.txt' % (seq), 'w') as out_file:
            print("Processing %s." % (seq))
            for frame in frames:
                dets = seq_dets[seq_dets[:, 0] == frame, 2:7]
                dets[:, 2:4] += dets[:, 0:2]  # convert  [x1,y1,w,h] to [x1,y1,x2,y2]
                total_frames += 1
                start_time = time.time()
                trackers,local_ID_enter,local_ID_exit,local_ID_completed = mot_tracker.update(dets)
                cycle_time = time.time() - start_time
                total_time += cycle_time
                # local_ID_enter, local_ID_exit,match_ID = track_manager.check_enter_exit(trackers,dead_track)
                # match_ID = track_manager.update_ID(trackers, dead_track)
                # if(len(match_ID) > 0):
                #    print(match_ID)
                # flag = True
                # while flag:
                #     flag = False
                #     for d in trackers:
                #         if d[4] in match_ID.keys():
                #             flag = True
                #             d[4] = match_ID[d[4]]
                #             break
                img = cv2.imread(
                    r'E:\Pycharm project\blitznet\Results\tracking_Toppan_15_05_20_case_24\img1\tracking_Toppan_15_05_20_case_24_{:04n}.jpg'.format(
                        frame))
                if len(local_ID_enter) > 0:
                    cv2.putText(img, 'Entered: {}'.format(local_ID_enter), (150, 482), 0, fontScale=1, color=(0, 255, 0),
                                thickness=2)
                    print("enter",local_ID_enter)
                if len(local_ID_exit) > 0:
                    cv2.putText(img, 'Exited: {}'.format(local_ID_exit), (150, 300), 0, fontScale=1, color=(255, 0, 0),
                                thickness=2)

                if len(local_ID_completed) > 0:
                    cv2.putText(img, 'Completed: {}'.format(local_ID_completed), (150, 150), 0, fontScale=1, color=(255, 255, 255),
                                thickness=2)
                    print("completed",local_ID_completed)

                cv2.polylines(img, np.array([INDOOR], np.int32), True, (0, 0, 255), thickness=2)
                cv2.polylines(img, np.array([OUTDOOR], np.int32), True, (0, 0, 255), thickness=2)
                for d in trackers:
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
                    cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 4, [255, 255, 255], thickness=thickness,
                                lineType=cv2.LINE_AA)
                cv2.putText(img, 'Frame {:d} - {:.2f}ms'.format(frame + 1, (time.time() - start_time) * 1000),
                            (30, 30), 0,
                            fontScale=1, color=(0, 255, 0), thickness=2)
                cv2.imshow("result",img)
                videoWriter.write(img)

                cv2.waitKey(5)

    print("Total Tracking took: %.3f for %d frames or %.1f FPS" % (total_time, total_frames, total_frames / total_time))
    if (display):
        print("Note: to get real runtime results run without the option: --display")


