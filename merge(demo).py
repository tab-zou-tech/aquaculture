#-* coding -utf-8 -*
#这个脚本用来切割和拼接图片
#运行程序输入1则为切割图片模式
#输入其他数字则为拼接图片模式
import numpy as np
import os
import cv2
import PIL.Image as Image

#切图
def cut():
    img = cv2.imread('./img/1792/org.tif', cv2.IMREAD_COLOR)
    h = img.shape[0]
    w = img.shape[1]
    print(h)
    print(w)
    cv2.imshow('test',img)
    cv2.waitKey()
    cv2.destroyAllWindows()

    size = 1792

    # 开始切图 cut
    h_step = img.shape[0] // size
    w_step = img.shape[1] // size

    h_rest = -(img.shape[0] - size * h_step)
    w_rest = -(img.shape[1] - size * w_step)################256变64,size

    image_list = []
    predict_list = []
    count = 0
    # 循环切图
    for h in range(h_step):
        for w in range(w_step):
            # 划窗采样
            img_cut = img[h*size:(h+1)*size, w*size:(w+1)*size, :]
            image_list.append(img_cut[:,:,1])
            cv2.imwrite(('./img/cut/' + '%3d_sat.jpg' % count), img_cut)
            count += 1

#拼接
def splice():
    IMAGES_PATH = r'E:\2020'  
    IMAGES_FORMAT = '.png'  
    IMAGE_SIZE = 528  
    IMAGE_ROW = 9 
    IMAGE_COLUMN = 8  
    IMAGE_SAVE_PATH = r'E:\merge.png'  

    # 获取图片集地址下的所有图片名称
    filelist = os.listdir(IMAGES_PATH)
    image_names = np.array([file for file in filelist if file.endswith('.png')], dtype=object)

    # 简单的对于参数的设定和实际图片集的大小进行数量判断
    if len(image_names) != IMAGE_ROW * IMAGE_COLUMN:
        raise ValueError("合成图片的参数和要求的数量不能匹配！")

    # 定义图像拼接函数
    def image_compose():
        to_image = Image.new('RGB', (IMAGE_COLUMN * IMAGE_SIZE, IMAGE_ROW * IMAGE_SIZE)) #创建一个新图
        # 循环遍历，把每张图片按顺序粘贴到对应位置上
        for y in range(0, IMAGE_ROW ):
            for x in range(0, IMAGE_COLUMN ):
                from_image = Image.open(IMAGES_PATH + "\\" + image_names[IMAGE_COLUMN * y + x ]).resize(
                    (IMAGE_SIZE, IMAGE_SIZE),Image.ANTIALIAS)
                to_image.paste(from_image, (x  * IMAGE_SIZE, y  * IMAGE_SIZE))
        return to_image.save(IMAGE_SAVE_PATH)
    image_compose() #调用函数

model = int(input())
if model == 0:
    cut()
else:
    splice()
