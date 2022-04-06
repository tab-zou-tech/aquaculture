import os
import shutil
import numpy as np
import cv2
import PIL.Image as Image
import imageio
import sys

def classify(path,ten):
    year_dir = "year"
    for img in os.listdir(path):
        year = img[5:9]
        if year_dir not in year:
            year_dir = year
        if  not os.path.exists(os.path.join(path,year_dir)): 
            os.makedirs(os.path.join(path,year_dir))
        if  not os.path.exists(path+"\\"+year_dir+"_ten"): 
            os.makedirs(path+"\\"+year_dir+"_ten")
        if any(index in img for index in ten):
            dst = os.path.join(path,year_dir+"_ten",img)
        else:
            dst = os.path.join(path,year_dir,img)
        src = os.path.join(path,img)
        shutil.move(src, dst)
    for d in ten:
        if  not os.path.exists(os.path.join(path,d)): 
            os.makedirs(os.path.join(path,"merge_"+d))
    for dir_path in os.listdir(path):
        if "ten" in dir_path:
            for img in os.listdir(os.path.join(path,dir_path)):
                img_name = img.split(".")[0]
                img_year , img_location = img_name.split("_")[1],img_name.split("_")[-1]
                old_img = os.path.join(path,dir_path,img)
                new_path = os.path.join(path,"merge_"+img_location,img_year+"_"+img_location+".png")
                shutil.move(old_img,new_path) 
            
    

def merge(path):
    if  not os.path.exists(os.path.join(path,"merge")): 
            os.makedirs(os.path.join(path,"merge"))
    for img in os.listdir(path):
        if ("ten" in img) or ("merge" in img): 
            continue
        if os.path.isdir(os.path.join(path,img)):
            IMAGES_PATH = os.path.join(path,img) 
            IMAGES_FORMAT = '.png'  
            IMAGE_SIZE = 528  
            IMAGE_ROW = 9 
            IMAGE_COLUMN = 8  
            IMAGE_SAVE_PATH = os.path.join(path,"merge",img+r'_merge.png')

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

            mat_jpg = cv2.imread(IMAGE_SAVE_PATH)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(mat_jpg, img, (50, 500), font, 20, (0, 40, 255), 10)
            cv2.imwrite(IMAGE_SAVE_PATH, mat_jpg)
            print(IMAGE_SAVE_PATH+" is finished!")
            print()
            
def draw_year(path):
    for dir_path in os.listdir(path):
        if "merge_" in dir_path:
            for img in os.listdir(os.path.join(path,dir_path)):
                IMAGE_SAVE_PATH = os.path.join(path,dir_path,img)
                mat_jpg = cv2.imread(IMAGE_SAVE_PATH)
                font = cv2.FONT_HERSHEY_SIMPLEX
                word = img.split("_")[0]
                cv2.putText(mat_jpg, word, (20, 80), font, 3, (0, 40, 255), 3)
                cv2.imwrite(IMAGE_SAVE_PATH, mat_jpg)         
                
def png_gif(path):
    for dir_path in os.listdir(path):
        if "merge" in dir_path:
            png_lst = os.listdir(os.path.join(path,dir_path))
            frames = []
            for i in png_lst:
                frames.append(imageio.imread(path + "\\" + dir_path + "\\" + i))
            # for i in range(0, 51):
            #     i = i*4 + 1
            #     k = str(i)
            #     z = k.zfill(4)
                # frames.append(imageio.imread(path + "/pten" + z + ".png"))
            imageio.mimsave(dir_path+"_result.gif", frames, 'GIF', duration=1.5)
            print(dir_path+" gif finish")
    
def close_dir(path):
    for dir_path in os.listdir(path):
        if "ten" in dir_path:
            if os.path.exists(dir_path):
                # removing the file using the os.remove() method
                os.remove(dir_path)
                print("dir_path have been remove")
            else:
                # file not found message
                print("File not found in the directory")
    
# read contours 
path = r"E:\model\drew_constrat\png\contours\0330"

#图片分类
test_ten = ["daishan","liuheng","jintang","qushan","sijiao","taohua","tushan","xiushan","zhoushan","zhujiajian"]
train_ten = ["index","liuheng","subset","zhujiajian"]

classify(path,test_ten)
merge(path)
draw_year(path)
png_gif(path)
close_dir(path)