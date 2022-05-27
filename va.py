import cv2
import numpy as np
import os
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
    
def va(png,lab,channel,th):
    if channel == 3:
        ### RGB  只能显示结果，不能计算FP
        img = cv2.imread(png)
        img2 = cv2.imread(lab)
        ret, binary_otsu = cv2.threshold(img, 10, 255, cv2.THRESH_BINARY)
        ret, binary_otsu2 = cv2.threshold(img2, 100, 255, cv2.THRESH_BINARY)
        imga=cv2.add(binary_otsu,binary_otsu2)
        imga_1=cv2.subtract(imga,binary_otsu)
        imgb=cv2.subtract(binary_otsu,binary_otsu2)
        imgb_1=cv2.subtract(imga,binary_otsu2)
        imgc=cv2.subtract(binary_otsu,imgb_1)
        weight, height, chanel = img.shape
        bg = np.zeros((weight, height, chanel),dtype=np.uint8)
        fn = 'NAN'
        fp = 'NAN'
        tp = 'NAN'
        
    elif channel == 1:
        ## grey      结果不可视
        img = cv2.imread(png, cv2.CV_8UC1)
        img2 = cv2.imread(lab, cv2.CV_8UC1)
        ret, binary_otsu = cv2.threshold(img, 10, 255, cv2.THRESH_BINARY)
        ret, binary_otsu2 = cv2.threshold(img2, th, 255, cv2.THRESH_BINARY)
        imgb_1=cv2.subtract(binary_otsu,binary_otsu2)
        imga_1=cv2.subtract(binary_otsu2,binary_otsu)
        imgc=cv2.subtract(binary_otsu,imgb_1)
        weight, height = img.shape
        bg = np.zeros((weight, height),dtype=np.uint8)

        fp = cv2.countNonZero(imga_1)
        fn = cv2.countNonZero(imgb_1)
        tp = cv2.countNonZero(imgc)
        
        # print("fn = ",fn)
        # print("fp = ",fp)
        # print("tp = ",tp)
    else:
        print("channel error: ",channel)
    
    # cv2.imshow('map_th',imga)
    # cv2.imshow('lab_th',imgb)
    # cv2.imshow('FN',imga_1)
    # cv2.imshow('FP',imgb_1)
    # cv2.imshow('TP',imgc)

    # vs1 = np.hstack((img,binary_otsu,img2, binary_otsu2))  # 水平堆叠
    # vs1 = np.hstack((img,img2,imga,imgb))
    # vs3 = np.hstack((imga_1, imgb_1,imgc,bg))  # 水平堆叠
    # result = np.vstack((vs1, vs3))  # 竖直堆叠
    # cv2.namedWindow('result',0)
    # cv2.resizeWindow( 'result',1280, 960)
    # cv2.moveWindow( 'result',500, 50)
    # cv2.moveWindow( 'result',500, 50)
    # cv2.imshow('result', result)
    
    year_index = png.split("\\")[-1]
    year = year_index[0:5]
    # cv2.imwrite('./{}_map_th.png'.format(year), imga)
    # cv2.imwrite('./{}_lab_th.png'.format(year), imgb)
    cv2.imwrite(r'C:\Users\dell\Desktop\VA\out\{}_{}_FP.png'.format(year, th), imga_1)
    cv2.imwrite(r'C:\Users\dell\Desktop\VA\out\{}_{}_FN.png'.format(year, th), imgb_1)
    cv2.imwrite(r'C:\Users\dell\Desktop\VA\out\{}_{}_TP.png'.format(year, th), imgc)
    return(fn,fp,tp)

if __name__ == '__main__':    
    png_dir = r'C:\Users\dell\Desktop\1\presentation_demo\lab\\'
    lab_dir = r'C:\Users\dell\Desktop\1\presentation_demo\dst\\'

    tuple_time = time.localtime()
    file_path = r'./log/%d%02d%02d_%02d%02d' \
                % (tuple_time.tm_year, tuple_time.tm_mon, tuple_time.tm_mday, tuple_time.tm_hour, tuple_time.tm_min) \
                + '.log'
    f = open(file_path, 'a')
    f.close()
    logger = get_logger(file_path)
    logger.info('start Drew!')
    
    for i in os.listdir(png_dir):
        lab = os.path.join(lab_dir,i)
        png = os.path.join(png_dir,i)
        for th in range(0,255,1):
            fn,fp,tp = va(png,lab,1,th)
            p = tp/(tp+fp)
            r = tp/(fn+tp)
            f = (2*p*r)/(p+r)
            logger.info('\t file:[{}]\t th:{}\t fn:{}\t fp:{}\t tp:{}\t p:{}\t r:{}\t f1:{}'.format(i, th, fn, fp, tp, p, r, f))
    print('finish')