import numpy as np
import matplotlib.pyplot as plt
import json
import pyecharts
from pyecharts.charts import Radar
from pyecharts import options as opts


def radarNow(data):
    array = []
    array1 = []
    # array2=[]
    array = insert_array(array, data[0])
    array1 = insert_array_change(array1, data[0])
    # array2=insert_array(array2,data[2])
    c_schema = [{"name": "PaperNum", "max": 2, "min": 0},
                {"name": "CitationNum", "max": 2, "min": 0},
                {"name": "H-index", "max": 2, "min": 0},
                {"name": "P-index", "max": 2, "min": 0},
                {"name": "UP-index", "max": 2, "min": 0}]
    radar = Radar(init_opts=opts.InitOpts(width="600px", height="550px"))
    radar.add_schema(
        schema=c_schema, textstyle_opts=opts.TextStyleOpts(color="black"))
    # radar.config(c_schema=c_schema, radar_text_size=15, yaxis_line_width=1)
    radar.add(series_name="Now", data=array,
              areastyle_opts=opts.AreaStyleOpts(color="#fc3d03", opacity=0.1))

    # radar.add(series_name="Predict", data=array1, areastyle_opts=opts.AreaStyleOpts(color="#2E8B57",opacity=0.1))
    #
    # radar.add("G. Salton", array2, item_color="#2E8B57", symbol_size=10,
    #           symbol='rect', area_color="#2E8B57", area_opacity=0.4,
    #           legend_top='bottom', legend_text_size=15, line_width=3)

    # radar.render("Rader-mine.html")
    return radar


def radarPredict(data):
    array = []
    array1 = []
    # array2=[]
    array = insert_array(array, data[0])
    array1 = insert_array_change(array1, data[0])
    # array2=insert_array(array2,data[2])
    c_schema = [{"name": "PaperNum", "max": 2, "min": 0},
                {"name": "CitationNum", "max": 2, "min": 0},
                {"name": "H-index", "max": 2, "min": 0},
                {"name": "P-index", "max": 2, "min": 0},
                {"name": "UP-index", "max": 2, "min": 0}]
    radar = Radar(init_opts=opts.InitOpts(width="600px", height="550px"))
    radar.add_schema(
        c_schema, textstyle_opts=opts.TextStyleOpts(color="black"))
    # radar.config(c_schema=c_schema, radar_text_size=15, yaxis_line_width=1)
    radar.add(series_name="Now", data=array,
              areastyle_opts=opts.AreaStyleOpts(color="#fc3d03", opacity=0.1))

    radar.add(series_name="Predict", data=array1,
              areastyle_opts=opts.AreaStyleOpts(color="#2E8B57", opacity=0.1))
    #
    # radar.add("G. Salton", array2, item_color="#2E8B57", symbol_size=10,
    #           symbol='rect', area_color="#2E8B57", area_opacity=0.4,
    #           legend_top='bottom', legend_text_size=15, line_width=3)

    # radar.render("Rader-change.html")
    return radar


def insert_array(array, data):
    if(data["#pc"] == "157"):
        data["#pi"] = float(data["#pi"])/15
        data["#upi"] = float(data["#upi"])/15
    arr = []
    pc = int(data["#pc"]) / 300
    cn = int(data["#cn"]) / 10000
    hi = (int(data["#hi"])+10) / 50
    pi = float(data["#pi"]) / 200
    upi = float(data["#upi"]) / 200
    arr.append(pc)
    arr.append(cn)
    arr.append(hi)
    arr.append(pi)
    arr.append(upi)
    array.append(arr)
    return array


def insert_array_change(array, data):
    if(data["#pc"] == "157"):
        data["#pi"] = float(data["#pi"])/15
        data["#upi"] = float(data["#upi"])/15
    arr = []
    pc = (int(data["#pc"])+20) / 300
    cn = (int(data["#cn"])+1000) / 10000
    hi = (int(data["#hi"])+20) / 50
    pi = (float(data["#pi"])+20) / 200
    upi = (float(data["#upi"])+20) / 200
    arr.append(pc)
    arr.append(cn)
    arr.append(hi)
    arr.append(pi)
    arr.append(upi)
    array.append(arr)
    return array


def plot_radar(data):
    arr = []
    pc = int(data["#pc"])/300
    cn = int(data["#cn"])/10000
    hi = int(data["#hi"])/50
    pi = float(data["#pi"])/200
    upi = float(data["#upi"])/200
    arr.append(pc)
    arr.append(cn)
    arr.append(hi)
    arr.append(pi)
    arr.append(upi)
    arr.append(pc)
    criterion = [0, 0, 0, 0, 0, 0]  # 基准雷达图
    angles = np.linspace(0, 2 * np.pi, 5, endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))
    # print(criterion)
    # print(angles)
    fig = plt.figure(facecolor='#87CEEB')  # 创建画板并填充颜色
    ax = fig.add_subplot(111, polar=True,)  # 设置坐标为极坐标
    # 绘制三个五边形
    floor = 0
    ceil = 2
    labels = np.array(['x1', 'x2', 'x3', 'x4', 'x5'])
    # 绘制五边形的循环
    for i in np.arange(floor, ceil + 0.5, 0.5):
        ax.plot(angles, [i] * (6), '-', lw=0.5, color='black')
    for i in range(5):
        ax.plot([angles[i], angles[i]], [floor, ceil],
                '-', lw=0.5, color='black')
     # 绘制雷达图
    ax.plot(angles, criterion, 'b-', lw=2, alpha=0.4)
    ax.fill(angles, criterion, facecolor='b', alpha=0.3)  # 填充
    ax.plot(angles, arr, 'b-', lw=2, alpha=0.35)
    ax.fill(angles, arr, facecolor='b', alpha=0.25)

    ax.set_thetagrids(angles * 180 / np.pi, labels)
    ax.spines['polar'].set_visible(False)  # 不显示极坐标最外的圆形
    ax.set_theta_zero_location('N')  # 设置极坐标的起点（即0度）在正上方向
    ax.grid(False)  # 不显示分隔线
    ax.set_yticks([])  # 不显示坐标间隔
    ax.set_title('xxxxxxxxxxxx', va='bottom', fontproperties='SimHei')
    ax.set_facecolor('#87ceeb')  # 填充绘图区域的颜色
    # 保存文png图片
    # 保存文png图片
    plt.subplots_adjust(left=0.09, right=1, wspace=0.25,
                        hspace=0.25, bottom=0.13, top=0.91)
    plt.savefig('a_1.png')
    plt.show()


def extract_data():
    with open('D:\Python\BigCreate2020\Dataset\AMiner-Author.txt', 'r', encoding='UTF-8') as readfile:
        # file=""
        # for i in range(0,10):
        #     file=file+readfile.readline()
        #     print(file)
        readfile = readfile.readlines()
        result = {}
        arr = []
        fr = open('D:\Python\BigCreate2020\Dataset\Author_json.json', 'a')
        i = 0
        j = 0
        a = 0
        b = 0
        c = 0
        d = 0
        e = 0
        for eachrow in readfile:
            j = j+1

            if j == 818140:
                break
            eachrow = eachrow.strip('\n')
            # print(eachrow)
            # eachrow = [i for i in eachrow if i != '']
            eachrow = eachrow.split(' ', 1)
            # print(eachrow)
            i = i+1
            # print(i)
            if i < 10:
                result[eachrow[0]] = eachrow[1]
                if i == 4:
                    if(float(eachrow[1]) > a):
                        a = float(eachrow[1])
                if i == 5:
                    if (float(eachrow[1]) > b):
                        b = float(eachrow[1])
                if i == 6:
                    if (float(eachrow[1]) > c):
                        c = float(eachrow[1])
                if i == 7:
                    if (float(eachrow[1]) > d):
                        d = float(eachrow[1])
                if i == 8:
                    if (float(eachrow[1]) > e):
                        e = float(eachrow[1])
                if i == 9:
                    # model = json.dumps(result,indent=4, separators=(',', ':'))
                    arr.append(result)
                    # fr.close()
                    result = {}
            else:
                i = 0

        arr = json.dumps(arr, indent=4, separators=(',', ':'))
        fr.write(arr)
        fr.close()
        print(result)
        print(a)
        print(b)
        print(c)
        print(d)
        print(e)


def tang_jie():
    with open('D:\Python\BigCreate2020\Dataset\Part-AMiner-Author.txt', 'r', encoding='UTF-8') as readfile:
        # file=""
        # for i in range(0,10):
        #     file=file+readfile.readline()
        #     print(file)
        readfile = readfile.readlines()
        result = {}
        arr = []
        fr = open('D:\Python\BigCreate2020\Dataset\Part_Author_json.json', 'a')
        i = 0
        j = 0
        a = 0
        b = 0
        c = 0
        d = 0
        e = 0
        for eachrow in readfile:
            j = j+1
            if j % 100 == 0:
                print(j)
            if j == 818140:
                break
            eachrow = eachrow.strip('\n')
            # print(eachrow)
            # eachrow = [i for i in eachrow if i != '']
            eachrow = eachrow.split(' ', 1)
            # print(eachrow)
            i = i+1
            # print(i)
            if i < 10:
                result[eachrow[0]] = eachrow[1]
                if i == 4:
                    if(float(eachrow[1]) > a):
                        a = float(eachrow[1])
                if i == 5:
                    if (float(eachrow[1]) > b):
                        b = float(eachrow[1])
                if i == 6:
                    if (float(eachrow[1]) > c):
                        c = float(eachrow[1])
                if i == 7:
                    if (float(eachrow[1]) > d):
                        d = float(eachrow[1])
                if i == 8:
                    if (float(eachrow[1]) > e):
                        e = float(eachrow[1])
                if i == 9:
                    # model = json.dumps(result,indent=4, separators=(',', ':'))
                    arr.append(result)
                    # fr.close()
                    result = {}
            else:
                i = 0

        arr = json.dumps(arr, indent=4, separators=(',', ':'))
        fr.write(arr)
        fr.close()
        print(result)
        print(a)
        print(b)
        print(c)
        print(d)
        print(e)


def tell_info():
    with open('D:\Python\BigCreate2020\Dataset\Author_json.json', 'r', encoding='UTF-8') as readjsonfile:
        # readfile=readfile.readlines()
        file = json.load(readjsonfile)
        print(type(file))
        readjsonfile.close()
        with open('D:\Python\BigCreate2020\Dataset\Author_json.json', 'w', encoding='UTF-8') as writejsonfile:
            with open('D:\Python\BigCreate2020\Dataset\Tangjie.txt', 'r', encoding='UTF-8') as readfile:
                result = {}
                for eachrow in readfile:
                    eachrow = eachrow.strip('\n')
                    eachrow = eachrow.split(' ', 1)
                    result[eachrow[0]] = eachrow[1]
                file.append(result)
                file = json.dumps(file, indent=4, separators=(',', ':'))
                writejsonfile.write(file)
                writejsonfile.close()
                readfile.close()


def get_scholar(data):
    with open('Author_json.json', 'r', encoding='UTF-8') as readjsonfile:
        file = json.load(readjsonfile)
        print(type(file))
        for eachdict in file:
            # print(eachdict["#index"])
            if(eachdict["#index"] == data):
                # print(eachdict["#index"])
                # print("hhh")
                dict = eachdict
                return dict


# data = [0.8, 0.9, 1.2, 1.0, 1.5, 0.8]
# plot_radar(data)
# extract_data()
# tell_info()
# tang_jie()
data1 = get_scholar("81815")
# data2=get_scholar("10")
# data3=get_scholar("47180")
data = []
data.append(data1)
# data.append(data2)
# data.append(data3)
radarNow(data)
radarPredict(data)
