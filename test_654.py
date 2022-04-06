
import time
import os
from osgeo import gdal
import numpy

def DoesDriverHandleExtension(drv, ext):
    exts = drv.GetMetadataItem(gdal.DMD_EXTENSIONS)
    return exts is not None and exts.lower().find(ext.lower()) >= 0
    
def GetExtension(filename):
    # 取得文件扩展名
    ext = os.path.splitext(filename)[1]
    # 输出不含'.'的扩展名
    if ext.startswith('.'):
        ext = ext[1:]
    return ext

def GetOutputDriversFor(filename):
    drv_list = []
    ext = GetExtension(filename)
    # 遍历每种驱动
    for i in range(gdal.GetDriverCount()):
        drv = gdal.GetDriver(i)
        # GetMetadataItem用于获取元数据的域
        # (drv.GetMetadataItem(gdal.DCAP_CREATE) is not None or \
        # 上述判断用于判断该驱动是否支持创建文件或者拷贝创建文件（传递一个需要拷贝的源数据集参数）
        # 所有驱动支持CREATE
        if (drv.GetMetadataItem(gdal.DCAP_CREATE) is not None or \
            drv.GetMetadataItem(gdal.DCAP_CREATECOPY) is not None) and \
           drv.GetMetadataItem(gdal.DCAP_RASTER) is not None:
            # 判断：如果该驱动能够处理ext拓展名的文件，则将该驱动的简称加入drv_list中
            if len(ext) > 0 and DoesDriverHandleExtension(drv, ext):
                drv_list.append( drv.ShortName )
            else:
                prefix = drv.GetMetadataItem(gdal.DMD_CONNECTION_PREFIX)
                if prefix is not None and filename.lower().startswith(prefix.lower()):
                    drv_list.append( drv.ShortName )
    # GMT is registered before netCDF for opening reasons, but we want
    # netCDF to be used by default for output.
    # NetCDF(network Common Data Form)网络通用数据格式
    if ext.lower() == 'nc' and len(drv_list) == 0 and \
       drv_list[0].upper() == 'GMT' and drv_list[1].upper() == 'NETCDF':
           drv_list = [ 'NETCDF', 'GMT' ]

    return drv_list

def GetOutputDriverFor(filename):
    drv_list = GetOutputDriversFor(filename)
    # 返回对于创建目标扩展名可用的驱动
    if len(drv_list) == 0:
        ext = GetExtension(filename)
        if len(ext) == 0:
            # 默认输出GTiff
            return 'GTiff'
        else:
            # raise:出现异常，停止后面的代码
            raise Exception("Cannot guess driver for %s" % filename)
    elif len(drv_list) > 1:
        print("Several drivers matching %s extension. Using %s" % (ext, drv_list[0]))
    return drv_list[0]

def trasferfile(inputfile, outputfile, lookup):
    # 在这里设置while的目的是下面可以直接跳过文件
    while True:
        format = None
        dirname, filename = os.path.split(inputfile)
        filename = filename.split('.')
        src_filename = inputfile
        dst_filename = outputfile + "//" + filename[0] + '_grey2rbg.' + filename[1]
        out_bands = 3
        band_number = 12

        # 初始化
        gdal.AllRegister()

        # ----------------------------------------------------------------------------
        # Open source file
        # 如果GDAL无法打开该文件，则跳过该文件
        try:
            src_ds = gdal.Open(src_filename)
        except:
            break
        if src_ds is None:
            print('Unable to open %s ' % src_filename)
            break

        src_band = src_ds.GetRasterBand(band_number)

        # ----------------------------------------------------------------------------
        # Ensure we recognise the driver.
        if format is None:
            format = GetOutputDriverFor(dst_filename)
        dst_driver = gdal.GetDriverByName(format)
        if dst_driver is None:
            print('"%s" driver not registered.' % format)
            sys.exit(1)

        # ----------------------------------------------------------------------------
        # Create the working file.

        if format == 'GTiff':
            tif_filename = dst_filename
        else:
            tif_filename = 'temp.tif'

        gtiff_driver = gdal.GetDriverByName('GTiff')
        tif_ds = gtiff_driver.Create(tif_filename,
                                     src_ds.RasterXSize, src_ds.RasterYSize, out_bands)

        # ----------------------------------------------------------------------------
        # We should copy projection information and so forth at this point.
        # 复制图片的基本信息到目标文件
        tif_ds.SetProjection(src_ds.GetProjection())
        tif_ds.SetGeoTransform(src_ds.GetGeoTransform())
        if src_ds.GetGCPCount() > 0:
            tif_ds.SetGCPs(src_ds.GetGCPs(), src_ds.GetGCPProjection())

        # ----------------------------------------------------------------------------
        # Do the processing one scanline at a time.
        # 按每一行的像素扫描
        for iY in range(src_ds.RasterYSize):
            # 取出每一行的像素行
            # ***这里取出的是一个二维数组，但是该数组比较特别
            # ***.shape返回（1，n）表示一个二维数组，但是该数组只有一行
            src_data = src_band.ReadAsArray(0, iY, src_ds.RasterXSize, 1)
            # 如果灰度值是uint16，需要将其拉伸到对应的uint8中对对应unit8的RGB值
            if src_data.dtype == 'uint16':
                src_data = src_data.astype(Numeric.float)
                src_data[0] = src_data[0] * 255
                src_data[0] = src_data[0] / 65535
                src_data = src_data.astype(Numeric.uint8)
            # 按Band
            for iBand in range(out_bands):
                # 复制该Band的表给band_lookup
                band_lookup = lookup[iBand]
                # src_data记录了该像素点的灰度的值
                # band_lookup记录了该通道下：每个灰度值所对应的该通道的值
                # 例如：band(1)记录了该灰度值所对应的green band的系数
                # 下面几行注释是原文件pct2rgb处将8bit的调色板映射到3*8bit的三通道rgb的方法
                    # ***numpy.take的作用：取出src_data中的每一个值（一个0-225的数值）
                    # ***将该数作为序号，去寻找band_lookup中对应位置的值
                    # for a in range(src_data):
                    #     dst_data[a) = Numeric.take(band_lookup,int(a/5300))
                dst_data = Numeric.take(band_lookup, src_data)
                tif_ds.GetRasterBand(iBand + 1).WriteArray(dst_data, 0, iY)
        tif_ds = None

        # ----------------------------------------------------------------------------
        # Translate intermediate file to output format if desired format is not TIFF.
        if tif_filename != dst_filename:
            tif_ds = gdal.Open(tif_filename)
            dst_driver.CreateCopy(dst_filename, tif_ds)
            tif_ds = None
            gtiff_driver.Delete(tif_filename)
        print('finish writting: ' + dst_filename)
        break

def lut(bar):
    # 思路：将256的灰度值中的每个数值，找到RGBA中的RGB对应的参数，写在lookup对照表中
    # 初始化对应表（256调色盘 ——> RGBA）
    # lookup[1:3]对应RGB
    if bar[0] == '1':
        data = Numeric.loadtxt("lut\\NDVI_VGYRM-lut.txt", dtype='uint8')
        data = data[:, 1:4]
    elif bar[0] == '2':
        data = Numeric.loadtxt("lut\\PET Color Palette.txt", dtype='uint8')
    r = data[:, 0]
    g = data[:, 1]
    b = data[:, 2]
    if bar[1] == 'r':
        lookup = [r[::-1],
                  g[::-1],
                  b[::-1]]
    elif bar[1] == 'p':
        lookup = [r[::1],
                  g[::1],
                  b[::1]]
    return lookup

# mian
class grey2rgb:
    '''这里输入的分别为：1.模式:模式1表示输入路径为单个文件；模式2表示输入路径为文件夹
                         2.imgtype:在文件夹模式下，如果文件夹存在多种格式的文件，处理哪种格式的文件。all表示全部处理
                         3.bar:选用哪种lookuptable，1和2两种。带r表示翻转lookup table
                         4&5.in/outputfile：输入输出路径（输出路径一定是文件夹。”'''
    def transfomation(self, mode, imgtype, bar, inputfile, outputfile):
        # calculate the time costed
        time_start = time.time()
        lookup = lut(bar)
        if mode == [1]:
            trasferfile(inputfile, outputfile,lookup)
        elif mode == [2]:
            for file in os.listdir(inputfile):
                singlefileName = inputfile+"\\"+file
                singlefileForm = os.path.splitext(singlefileName)[1][1:]
                if(singlefileForm == imgtype):
                    trasferfile(singlefileName, outputfile, lookup)
                elif(imgtype == 'all'):
                    trasferfile(singlefileName, outputfile, lookup)
        time_end = time.time()
        return time_end-time_start


inputfile = r'C:\Users\dell\Desktop\J data\mosaic\LC08_2014.tif'
outputfile = r'C:\Users\dell\Desktop\J data\mosaic'
grey2rgb().transfomation(1,"tif","1p",inputfile,outputfile)