import numpy as np
import matplotlib.pyplot as plt
import pyecharts.options as opts
import json
import random
import pymysql
# import pyecharts
import dat
from pyecharts.charts import Radar


def get_radar(name):
    data = get_data()
    hIndexStr = ''
    for i in range(len(data)):
        if data[i]['name'] == name:
            hIndexStr = data[i]['h_index']
            break
    hInex = float(hIndexStr)
    array = []
    total = dat.get_info_by_name(name)
    print(total)
    array = [[total[10][3], total[10][4], total[10]
             [5], total[10][6], total[10][7]]]
    print(array)
    return leida_pyecharts(array, name)
    # predict(array,hInex)


def getAllPrime(hIndex):
    # if(data["#pc"]=="157"):
    #     data["#pi"]=float(data["#pi"])/15
    #     data["#upi"]=float(data["#upi"])/15
    allArr = []
    # pc = int(data["#pc"]) / 300
    # cn = int(data["#cn"]) / 10000
    # hi = (int(data["#hi"])+10) / 50
    # pi = float(data["#pi"])/ 200
    # upi = float(data["#upi"]) / 200
    pc = int(hIndex*10+random.randint(3, 300))
    if(pc > 600):
        pc = 600
    cn = pc*5
    # cn=6000;
    if(cn > 5000):
        cn = 5000
    hi = int(hIndex)
    pi = float(random.random())
    gi = int(hIndex + random.randint(3, 10))
    arr = []
    arr.append(pc)
    arr.append(cn)
    arr.append(hi)
    arr.append(pi)
    arr.append(gi)
    allArr.append(arr)
    for i in range(2010, 2021):
        arr = []
        r = random.randint(0, 3)
        rate = float((10+r) / 10)
        pc = int(pc * rate)
        if(pc > 600):
            pc = 600
        cn = int(cn * rate)
        if(cn > 5000):
            cn = 5000
        hi = int(cn * rate)
        if(hi > 50):
            hi = 50
        print(pi, 2-rate)
        pi = pi * (2-rate)
        gi = int(gi * rate)
        arr.append(pc)
        arr.append(cn)
        arr.append(hi)
        arr.append(pi)
        arr.append(gi)
        allArr.append(arr)
    print(allArr)
    return allArr


def getPrime(hIndex):
    # if(data["#pc"]=="157"):
    #     data["#pi"]=float(data["#pi"])/15
    #     data["#upi"]=float(data["#upi"])/15
    arr = []
    # pc = int(data["#pc"]) / 300
    # cn = int(data["#cn"]) / 10000
    # hi = (int(data["#hi"])+10) / 50
    # pi = float(data["#pi"])/ 200
    # upi = float(data["#upi"]) / 200
    pc = int(hIndex*10+random.randint(3, 600))
    # pc=700;
    if(pc > 600):
        pc = 600
    cn = pc*5
    # cn=6000;
    if(cn > 5000):
        cn = 5000
    hi = int(hIndex)
    pi = float(random.random())
    gi = int(hIndex+random.randint(3, 10))
    arr.append(pc)
    arr.append(cn)
    arr.append(hi)
    arr.append(pi)
    arr.append(gi)
    return arr


def get_scholar_info_from_db():
    try:
        db = pymysql.connect(host='121.196.111.9',
                             port=3306,
                             user='test',
                             passwd='123456',
                             db='blogs'
                             )
        cur = db.cursor()
        sql = "SELECT * FROM Scholar_info"
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        jsonData = []
        for i in range(len(data)):
            result = {'name': data[i][1],
                      'year_num': data[i][2],
                      'paper': data[i][3],
                      'citation': data[i][4],
                      'h_index': data[i][5],
                      'p_index': data[i][6],
                      'g_index': data[i][7],
                      }
            jsonData.append(result)
        print(len(jsonData[0]))

        jsondatar = json.dumps(jsonData, indent=4)
       # print(jsondatar)
       # f = open("authors2.json", "a")
        with open("new_scholar_info.json", "w+") as f:
            f.write(jsondatar)
            f.flush()
            f.close()
        # 去除首尾的中括号
        infodict = json.loads(jsondatar)
        return infodict

    except:
        print('MySQL connect fail...')


def insert_to_db():
    db = pymysql.connect(host='121.196.111.9',
                         port=3306,
                         user='test',
                         passwd='123456',
                         db='blogs'
                         )
    cursor = db.cursor()
    query = "insert into Scholar_info (name, year_num, paper, citation, h_index, p_index, g_index) values (%s, %s, %s, %s, %s, %s, %s)"
    scholar_info = []
    h_indexes = dat.get_h_index_from_db()
    hi_index = ['h_index_1',
                'h_index_2',
                'h_index_3',
                'h_index_4',
                'h_index_5',
                'h_index_6',
                'h_index_7',
                'h_index_8',
                'h_index_9',
                'h_index_10',
                'h_index_11',
                'h_index_now']
    for i in range(len(h_indexes)):
        year_num = 2010
        hii_index = 0
        arrAll = getAllPrime(h_indexes[i][hi_index[hii_index]])
        for j in range(len(h_indexes[i])-1):
            arr = arrAll[j]
            scholar_info.append(h_indexes[i]['name'])
            scholar_info.append(int(year_num))
            scholar_info.append(int(arr[0]))
            scholar_info.append(int(arr[1]))
            scholar_info.append(int(arr[2]))
            scholar_info.append(float(arr[3]))
            scholar_info.append(int(arr[4]))
            year_num += 1
            hii_index += 1
            cursor.execute(query, scholar_info)
            db.commit()
            scholar_info = []


def prime(array, hIndex):
    # if(data["#pc"]=="157"):
    #     data["#pi"]=float(data["#pi"])/15
    #     data["#upi"]=float(data["#upi"])/15
    arr = []
    # pc = int(data["#pc"]) / 300
    # cn = int(data["#cn"]) / 10000
    # hi = (int(data["#hi"])+10) / 50
    # pi = float(data["#pi"])/ 200
    # upi = float(data["#upi"]) / 200
    pc = int(hIndex*10+random.randint(3, 600))
    # pc=700;
    if(pc > 600):
        pc = 600
    cn = pc*5
    # cn=6000;
    if(cn > 5000):
        cn = 5000
    hi = int(hIndex)
    pi = float(random.random())
    gi = int(hIndex+random.randint(3, 10))
    arr.append(pc)
    arr.append(cn)
    arr.append(hi)
    arr.append(pi)
    arr.append(gi)
    array.append(arr)
    return array


def get_data():
    # with open('./jsonFile.json', 'r', encoding='utf-8') as f:
    #     author_text = json.load(f)
    author_text = dat.getAllScholar()
    return author_text


def leida_pyecharts(data, name):
    # array=[]
    # array2=[]
    # array=prime(array,data[0])
    # array1=insert_array_change(array1,data[0])
    # array2=insert_array(array2,data[2])
    # c_schema = [{"name": "PaperNum", "max": 600, "min": 0},
    #             {"name": "CitationNum", "max": 5000, "min": 0},
    #             {"name": "H-index", "max": 50, "min": 0},
    #             {"name": "P-index", "max": 1, "min": 0},
    #             {"name": "G-index", "max": 50, "min": 0}]
    c = (
        Radar(init_opts=opts.InitOpts(width="1280px",
              height="720px", bg_color="#F6F6F6"))
        # Radar()
        # .set_colors(["#4587E7"])
        .add_schema(
            schema=[
                opts.RadarIndicatorItem(name="PaperNum", max_=600),
                opts.RadarIndicatorItem(name="CitationNum", max_=5000),
                opts.RadarIndicatorItem(name="H-index", max_=100),
                opts.RadarIndicatorItem(name="P-index", max_=1),
                opts.RadarIndicatorItem(name="G-index", max_=100),
            ],
            splitarea_opt=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
            textstyle_opts=opts.TextStyleOpts(color="#696969"),
        )
        .add(
            series_name="学者影响力",
            data=data,
            linestyle_opts=opts.LineStyleOpts(color="#696969", width="3"),
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title=""), legend_opts=opts.LegendOpts()
        )
        # .render("basic_radar_chart.html")
    )
    return c
    # Radar(init_opts=opts.InitOpts(width="1280px", height="720px", bg_color="#CCCCCC"))
    # .add_schema(
    #     schema=[
    #         opts.RadarIndicatorItem(name="销售（sales）", max_=6500),
    #         opts.RadarIndicatorItem(name="管理（Administration）", max_=16000),
    #         opts.RadarIndicatorItem(name="信息技术（Information Technology）", max_=30000),
    #         opts.RadarIndicatorItem(name="客服（Customer Support）", max_=38000),
    #         opts.RadarIndicatorItem(name="研发（Development）", max_=52000),
    #         opts.RadarIndicatorItem(name="市场（Marketing）", max_=25000),
    #     ],
    #     splitarea_opt=opts.SplitAreaOpts(
    #         is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
    #     ),
    #     textstyle_opts=opts.TextStyleOpts(color="#fff"),
    # )
    # .add(
    #     series_name="预算分配（Allocated Budget）",
    #     data=v1,
    #     linestyle_opts=opts.LineStyleOpts(color="#CD0000"),
    # )
    # .add(
    #     series_name="实际开销（Actual Spending）",
    #     data=v2,
    #     linestyle_opts=opts.LineStyleOpts(color="#5CACEE"),
    # )
    # .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    # .set_global_opts(
    #     title_opts=opts.TitleOpts(title="基础雷达图"), legend_opts=opts.LegendOpts()
    # )
    # .render("basic_radar_chart.html")
    # Radar(init_opts=opts.InitOpts(width="1280px", height="720px", bg_color="#CCCCCC"))
    # # .config(c_schema=c_schema, radar_text_size=15, yaxis_line_width=1)
    # .add(name, data, item_color="#55648B", symbol_size=10,
    #           symbol='rect', area_color="#55648B", area_opacity=0.4,
    #           legend_top='bottom', legend_text_size=15, line_width=3)
    # radar = Radar("雷达图")
    # radar.config(c_schema=c_schema, radar_text_size=15, yaxis_line_width=1)
    # radar.add(name, data, item_color="#55648B", symbol_size=10,
    #           symbol='rect', area_color="#55648B", area_opacity=0.4,
    #           legend_top='bottom', legend_text_size=15, line_width=3)

    # radar.add("Anon et al", array1, item_color="#EE1000", symbol_size=10,
    #           symbol='rect', area_color="#EE1000", area_opacity=0.4,
    #           legend_top='bottom', legend_text_size=15, line_width=3)
    # #
    # radar.add("G. Salton", array2, item_color="#2E8B57", symbol_size=10,
    #           symbol='rect', area_color="#2E8B57", area_opacity=0.4,
    #           legend_top='bottom', legend_text_size=15, line_width=3)
    # radar.show_config()
    # radar.render("Rader.html")

# create_random_radar("Robert Dale")


if __name__ == '__main__':
    #getAllPrime("aaa", 10)
    insert_to_db()
