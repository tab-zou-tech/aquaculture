import cv2
import os
def merge_picture(merge_path,num_of_cols,num_of_rows):
    for subimg in os.listdir(merge_path)
    filename=file_name(subimg)
    shape=cv2.imread(filename[0],1).shape    #三通道的影像需把-1改成1
    cols=shape[1]
    rows=shape[0]
    channels=shape[2]
    dst=np.zeros((rows*num_of_rows,cols*num_of_cols,channels),np.uint8)
    for i in range(len(filename)):
        img=cv2.imread(filename[i],-1)
        cols_th=int(filename[i].split("_")[-1].split('.')[0])
        rows_th=int(filename[i].split("_")[-2])
        roi=img[0:rows,0:cols,:]
        dst[rows_th*rows:(rows_th+1)*rows,cols_th*cols:(cols_th+1)*cols,:]=roi
    cv2.imwrite(merge_path+"merge.tif",dst)
 
"""遍历文件夹下某格式图片"""
def file_name(root_path,picturetype):
    filename=[]
    for root,dirs,files in os.walk(root_path):
        for file in files:
            if os.path.splitext(file)[1]==picturetype:
                filename.append(os.path.join(root,file))
    return filename
 
 
"""调用合并图片的代码"""
merge_path=r"E:\2020"   #要合并的小图片所在的文件夹
num_of_cols=9    #列数
num_of_rows=8     #行数

merge_picture(merge_path,num_of_cols,num_of_rows)