import os

import cv2
import csv
import datetime as dt
import re
import logging
import time

def get_logger(filename, verbosity=1, name=None):
    level_dict = {0: logging.DEBUG, 1: logging.INFO, 2: logging.WARNING}
    formatter = logging.Formatter(
        "[%(asctime)s][%(filename)s][line:%(lineno)d][%(levelname)s] %(message)s"
    )
    logger = logging.getLogger(name)
    logger.setLevel(level_dict[verbosity])

    fh = logging.FileHandler(filename, "w")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    return logger


def drewBlock(img_path, img_jpg):
    mat_jpg = cv2.imread(img_jpg)
    mat_img2 = cv2.imread(img_path, cv2.CV_8UC1)
    # 二值化
    # print(img_path,img_jpg)
    ret_otsu, binary_otsu = cv2.threshold(mat_img2, 100, 255, cv2.THRESH_BINARY)
    # 自适应分割
    # dst = cv2.adaptiveThreshold(mat_img2, 50, cv2.BORDER_REPLICATE, cv2.THRESH_BINARY_INV, 3, 10)
    # 提取轮廓
    contours, img = cv2.findContours(binary_otsu, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    index = 0
    if len(contours):
        for contour in contours:
            # if index == 0 or index == 1 or index == 4 or index == 3:
            #     index = index + 1
            #     continue
            M = cv2.moments(contour)
            if M["m00"] == 0:
                index = index + 1
                continue
            center_x = int(M["m10"] / M["m00"])
            center_y = int(M["m01"] / M["m00"])
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.circle(mat_jpg, (center_x, center_y), 2, 128, -1)  # 绘制中心点
            cv2.putText(mat_jpg, str(index+1), (center_x, center_y), font, 0.5, (240, 40, 255), 1)

            index = index + 1
    # 标记轮廓 __ 自标记
    img_contours = cv2.drawContours(mat_jpg, contours, -1, (0, 0, 255), -1)
    # 标记轮廓 —— 在原图像上
    # img_contours = cv2.drawContours(mat_img, contours, -1, (50, 0, 200), 10)     mat_img 替换为原图像
    # 图像show
    # cv2.namedWindow(img_path, 0)
    # cv2.resizeWindow(img_path, 1280, 960)
    # cv2.moveWindow(img_path, 500, 50)
    # cv2.imshow(img_path, img_contours)
    # cv2.waitKey(0)
    # 保存图片
    # print(img_path.split(".")[2].split("/")[3])
    # cv2.imwrite(
    #             r"../png/contours/{}/{}.png".format(img_path.split(".")[2].split("/")[2],
    #                                                 img_path.split(".")[2].split("/")[3]),
    #             img_contours)
    cv2.imwrite(r'../png/contours/0401/{}.png'.format(img_path.split('\\')[-1].split('.')[0]), img_contours)
    # 计算面积
    areas = []
    k = 0
    areas_total = 0
    for contour in contours:
        areas.extend([cv2.contourArea(contour)])
        k = k + 1
        areas_total = areas_total + cv2.contourArea(contour)
    # return
    return areas, areas_total


def list2csv(list_data):
    path = '../log/test.csv'
    with open(path, 'a+', newline='') as f:
        csv_write = csv.writer(f)
        csv_write.writerow(list_data)


def writelog(list_data):
    path = '../log/log.csv'
    # 获取当前时间
    now_time = dt.datetime.now().strftime('%F %T')
    with open(path, 'a+', newline='') as f:
        csv_write = csv.writer(f)
        csv_write.writerow([now_time])
        csv_write.writerow(list_data)


def showblock():
    img_detect_path = r'E:\model\U-2-Net-master\test_data\output_ten_d\\'
    img_jpg_path = r'E:\model\U-2-Net-master\test_data\image2\\'

    tuple_time = time.localtime()
    file_path = r'../log/%d%02d%02d_%02d%02d' \
                % (tuple_time.tm_year, tuple_time.tm_mon, tuple_time.tm_mday, tuple_time.tm_hour, tuple_time.tm_min) \
                + '.log'
    f = open(file_path, 'a')
    f.close()
    logger = get_logger(file_path)
    logger.info('start Drew!')

    # read png_detect
    print('----------------------detection--------------------------')
    for i in os.listdir(img_detect_path):
        img_path = img_detect_path + i
        img_jpg = img_jpg_path + i.split('.')[0] + '.tif'
        area_png, area_max = drewBlock(img_path, img_jpg)
        print(i, 'contouring finish')
        logger.info('\t file:[{}]\t area={:.5f}'.format(i, area_max))
        index = 1
        for area in area_png:
            logger.info('\t\t\t index:{}\t area={:.1f}'.format(index, area))
            index = index + 1
    logger.info('finish Drew!')


def cal(img_path, img_type):
    # mat_jpg = cv2.imread(img_jpg)
    mat_img2 = cv2.imread(img_path, cv2.CV_8UC1)
    # 二值化
    if img_type == 1:
        ret_otsu, binary_otsu = cv2.threshold(mat_img2, 100, 255, cv2.THRESH_BINARY)
    elif img_type == 2:
        ret_otsu, binary_otsu = cv2.threshold(mat_img2, 1, 255, cv2.THRESH_BINARY)
    else:
        ret_otsu, binary_otsu = cv2.threshold(mat_img2, 50, 255, cv2.THRESH_BINARY)
    # 自适应分割
    # dst = cv2.adaptiveThreshold(mat_img2, 50, cv2.BORDER_REPLICATE, cv2.THRESH_BINARY_INV, 3, 10)
    # 提取轮廓
    contours, img = cv2.findContours(binary_otsu, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # 标记轮廓 __ 自标记
    # img_contours = cv2.drawContours(mat_jpg, contours, -1, (0, 0, 240), 1)
    # 标记轮廓 —— 在原图像上
    # img_contours = cv2.drawContours(mat_img, contours, -1, (50, 0, 200), 10)     mat_img 替换为原图像
    # 图像show
    # cv2.namedWindow(img_path, 0)
    # cv2.resizeWindow(img_path, 1280, 960)
    # cv2.moveWindow(img_path, 500, 50)
    # cv2.imshow(img_path, img_contours)
    # cv2.waitKey(0)
    # 保存图片
    # print(img_path.split(".")[2].split("/")[3])
    # cv2.imwrite(
    #             r"../png/contours/{}/{}.png".format(img_path.split(".")[2].split("/")[2],
    #                                                 img_path.split(".")[2].split("/")[3]),
    #             img_contours)
    # cv2.imwrite(r'../png/contours/{}.png'.format(img_path.split('\\')[-1].split('.')[0]), img_contours)
    # 计算面积
    areas = []
    k = 0
    areas_total = 0
    for contour in contours:
        areas.extend([cv2.contourArea(contour)])
        k = k + 1
        areas_total = areas_total + cv2.contourArea(contour)
    areas.extend([areas_total])
    # return
    return areas, areas_total, cv2.countNonZero(binary_otsu)


def lossCal():
    img_detect_path = r'../png/lossCal/detect/'
    img_origin_path = r'../png/lossCal/origin/'

    tuple_time = time.localtime()
    file_path = r'../log/loss_%d%02d%02d_%02d%02d' \
                % (tuple_time.tm_year, tuple_time.tm_mon, tuple_time.tm_mday, tuple_time.tm_hour, tuple_time.tm_min) \
                + '.log'
    f = open(file_path, 'a')
    f.close()
    logger = get_logger(file_path)
    logger.info('start cal!')

    area_file = []
    area_det_file = []
    area_org_file = []
    area_name_file = []
    # read png_detect
    print('----------------------detection--------------------------')
    for i in os.listdir(img_detect_path):
        img_path = img_detect_path + i
        area_png, area_total, pix = cal(img_path, 1)
        logger.info('\t detection:{}\t areas:{}\t area_total:{}\t pix={}'.format(img_path, area_png, area_total, pix))
        print(i, 'contouring finish')

    # read png_origin
    for i in os.listdir(img_origin_path):
        img_path = img_origin_path + i
        area_png, area_total, pix = cal(img_path, 2)
        logger.info('\t original:{}\t areas:{}\t area_total:{}\t pix={}'.format(img_path, area_png, area_total, pix))
        print(i, 'contouring finish')

    print('calculate successful')
    # print(cell_data)
    # writelog(area_file)
    # print('writeln successful')


if __name__ == '__main__':
    # lossCal()
    showblock()
