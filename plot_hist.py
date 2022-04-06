def plot_arch(title,old_data,xticks):
    print("draw the "+title+" now!")
    #调整data[2015,2020,1985,1990,1995,2000,2005,2010] -> [1985,1990,1995,2000,2005,2010,2015,2020]
    # print(old_data)
    data = []
    data = old_data[2:]
    data.append(old_data[0])
    data.append(old_data[1])
    print(data)
    plt.bar(xticks, 
            data, # 指定绘图数据
              # 指定直方图中条块的个数
             color = 'steelblue', # 指定直方图的填充色
             # edgecolor = 'black' # 指定直方图的边框色
             width=0.6
             )
    # data.plot(kind = 'hist', bins = 30, color = 'steelblue', edgecolor = 'black', label = '直方图')
    plt.xlabel('time')
    plt.ylabel('area')
    # plt.xticks(xticks)    #根据分布频率手动设置x轴的刻度
    # 添加标题
    plt.title(title)
    # 显示图例
    # plt.legend()
    # 显示图形
    plt.savefig(title+".png")
    plt.show()
    
    
    
import matplotlib.pyplot as plt
import pandas as pd
import os
# file need to draw hist
file_path = r"E:\\result2.txt"
fp = open(file_path)
print("open the file " + file_path)
test_ten = ["daishan","liuheng","jintang","qushan","sijiao","taohua","tushan","xiushan","zhoushan","zhujiajian","year"]
index_line = 0
title = "year"
data = []
xticks = ['1985','1990','1995','2000','2005','2010','2015','2020']
for line in fp.readlines():
    index_line = index_line + 1
    if index_line % 9 == 1:
        if data == []:
            continue
        plot_arch(title,data,xticks)
        title = line.split(" ")[0]
        data = []
    area = line.split("=")[-1]
    area = float(area)
    if area:
        data.append(area) 
plot_arch(title,data,xticks)        
fp.close()    