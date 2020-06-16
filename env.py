MODEL_PATH = '/home/anhtran/blitznet/archive/BlitzNet512_x8_VOC07_det/model.ckpt-174000'
video_input = '/mnt/hdd10tb/Downloads/Fisheye/PJ9/Toppan_15_05_20/test_cases/case25/07_center_fisheye_2020_05_15_10_42_31.mp4'
video_folder =  '/mnt/hdd10tb/Downloads/Fisheye/PJ5/PJ5_raw_data/poc_room_10_01_20'
test_tracking_folder = '/mnt/hdd10tb/Downloads/Fisheye/PJ9/PJ9_tracking/images/train/TRACKING_pymotmetric/tracking_deepsort'
# INDOOR = [(0, 0), (512, 0), (343, 168), (319, 342),(512,512),(0,512)]
# OUTDOOR = [(343, 168),(512, 0), (512, 512), (319, 342)]
I = [(256,0),(512,0),(512,256),(256,256)]
IV = [(256,256),(512,256),(512,512),(256,512)]
# Top pan - Nhat Anh
INDOOR = [[330, 149], [323, 211], [338, 219], [333, 280], [315, 282], [303, 361], [282, 350], [309, 151]]
OUTDOOR = [[337, 147], [328, 211], [342, 217], [336, 285], [319, 286], [307, 368], [358, 394], [388, 133]]
#Tokyo
# INDOOR=[[387, 160], [484, 183], [487, 224], [377, 196]]
# OUTDOOR=[[406, 121], [394, 157], [477, 177], [482, 141]]
# INDOOR = [[3, 1], [284, 152], [399, 147], [455, 168], [571, 2], [701, 4], [699, 570], [8, 568], [5, 3]]
# I = [(352,0),(704,0),(704,288),(352,288)]
# IV = [(352,288),(704,288),(704,576),(352,576)]
intersec_thresshold = 0.8
CONF_THRESH = 0.01      # The threshold of confidence above which a bboxes is considered as a class example
EVAL_MIN_CONF = 0.7     # Filter candidate boxes by thresholding the score.
                        # Needed to make clean final detection results.
TOP_K_NMS = 400         # How many top scoring bboxes per category are passed to nms
TOP_K_AFTER_NMS = 50    # How many top scoring bboxes per category are left after nms
TOP_K_POST_NMS = 200    # How many top scoring bboxes in total are left after nms for an image
NMS_THRESH = 0.4
DETECT = True            # if you want a net to perform detection
SEGMENT = False         # if you want a network to perform segmentation
NO_SEG_GT = False
sort = True



# TRAINING FLAGS
MEAN_COLOR = [103.062623801, 115.902882574, 123.151630838]
bn_decay = 0.9
learning_rate = 1e-4
TOP_FM = 512            # The number of feature maps in the layers appended to a base network
image_size = 512
# image_size = 512
x4 = True
head = 'nonshared'      #choices=['shared', 'nonshared']
det_kernel = 3          #The size of conv kernel in classification/localization mapping for bboxes
seg_filter_size = 1     # The size of the conv filter used to map feature maps to intermediate representations before segmentation
n_base_channels = 64    # The size of intermediate representations before concatenating and segmenting
resize = 'bilinear'     #choices=['bilinear', 'nearest']
zoomout_prob =  0.5     # To what ratio of images apply zoomout data augmentation
trunk = 'resnet50'      #choices=['resnet50', 'vgg16']      The network you use as a base network (backbone)


