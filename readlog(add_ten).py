file_path = r"E:\\20220401_0918.log"
fp = open(file_path)
print("open the file " + file_path)
year_area = 0
year_index = "year"
test_ten = ["daishan","liuheng","jintang","qushan","sijiao","taohua","changtu","xiushan","zhoushan","zhujiajian","index"]
train_ten = ["index","liuheng","subset","zhujiajian"]
contain = []
for i in range(10):
    contain.append([])
print(contain)
for line in fp.readlines():
    noread = 1
    for i in range(len(test_ten)-1):
        if test_ten[i] in line:
            noread = 0
            result = line[60:]
            year = result[7:16]
            area = float(result.split("=")[-1])
            contain[i].append([year,area])
            break
    if noread:
        continue
    elif "file" in line:
        result = line[60:]
        year = result[7:16]
        area = float(result.split("=")[-1])
        if year_index != year:
            with open("E:\\result4.txt","a") as fp2:
                areas = year_area
                fp2.write(year_index+" area="+str(areas)+"\n")
            print(year_index + " is finish!")
            print()
            year_index = year
            year_area = 0
        year_area = year_area + area
with open("E:\\result4.txt","a") as fp2:
    fp2.write(year_index+" area="+str(year_area)+"\n")       
print(year_index + " is finish!")    
# print(contain)
for i in contain:
    print(i)
with open("E:\\result4.txt", "a") as fp2:
    for i in range(len(contain)):
        fp2.write(test_ten[i]+" area=0"+"\n")
        for j in contain[i]:
            fp2.write(j[0]+" area="+str(j[1])+"\n")

fp.close()