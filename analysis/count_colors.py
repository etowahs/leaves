import json
import cv2
import numpy as np


def cvt_bgr(rgb):
    """
Converts an rgb list [R, G, B] into a bgr nparray
    :param rgb:
    :return:
    """
    rgb.reverse()
    return np.float32([[rgb]])


def is_fall_color(color):
    """
Determines if hsv value is a fall color
    :param color: hvs color
    :return: bool, true if call color
    """
    bgr = cvt_bgr(color)
    bgr_img = np.full((50, 50, 3), bgr, dtype='uint8')
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    hsv = hsv.tolist()
    hue = hsv[0][0][0]
    sat = hsv[0][0][1]
    val = hsv[0][0][2]
    '''
    if (hue > 300 or hue < 60) and val > 150 and sat > 0.09:
        print(hsv[0][0])
        cv2.imshow("grabbed", bgr_img)
        cv2.waitKey(0)
        '''
    return (hue > 300 or hue < 60) and val > 150 and sat > 0.09


def fall_by_week(observations, save_file):
    """
Generate a csv of the number of "fall" color observations in each week of the observation period
    :param observations: list of observations generated by gen_final.py
    :param save_file: file name of csv
    """
    observations.reverse()  # make chronological
    current_week = 1
    fall_count = 0
    with open(save_file, 'w+') as sf:
        for obv in observations:
            if obv['week'] == current_week:
                if is_fall_color(obv['color']):
                    fall_count += 1
            else:
                # print('write')
                sf.write(str(current_week) + ',' + str(fall_count) + '\n')
                fall_count = 0
                current_week = obv['week']
                if is_fall_color(obv['color']):
                    fall_count += 1

if (__name__ == '__main__'):
    SAVE_FILE = 'output9.csv'
    with open('2019final.json', 'r') as fp:  # final observation file, generated by <LeafColors>.observation_colors()
        obvs = json.load(fp)
    fall_by_week(obvs, SAVE_FILE)
