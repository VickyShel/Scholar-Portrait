import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import pymysql

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import json
import pyecharts.options as opts
from pyecharts.charts import Line, Grid
from pyecharts.commons.utils import JsCode


def readFile():
    with open('./H_indexes.json', 'r', encoding='utf-8') as f:
        author_text = json.load(f)
    return author_text

def get_h_index_from_db():
    try:
        db = pymysql.connect(host='121.196.111.9',port=3306,user='test',passwd='123456',db='blogs')
        cur = db.cursor()
        sql = "SELECT * FROM Hindex"
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        jsonData = []
        for i in range(len(data)):
            result = {'name': data[i][0],
                      'h_index_1': data[i][1],
                      'h_index_2': data[i][2],
                      'h_index_3': data[i][3],
                      'h_index_4': data[i][4],
                      'h_index_5': data[i][5],
                      'h_index_6': data[i][6],
                      'h_index_7': data[i][7],
                      'h_index_8': data[i][8],
                      'h_index_9': data[i][9],
                      'h_index_10': data[i][10],
                      'h_index_11': data[i][11],
                      'h_index_now': data[i][12]}
            jsonData.append(result)

        jsondatar = json.dumps(jsonData, indent=4)
       # print(jsondatar)
       # f = open("authors2.json", "a")
        with open("new_H_indexes.json", "w+") as f:
            f.write(jsondatar)
            f.flush()
            f.close()
        # 去除首尾的中括号
        hindexdict = json.loads(jsondatar)
        return hindexdict

    except:
        print('MySQL connect fail...')

def logistic_increase_function(t, K, P0, r):
    t0 = 2009
    # # t:time   t0:initial time    P0:initial_value    K:capacity  r:increase_rate
    exp_value = np.exp(r * (t - t0))
    return (K * exp_value * P0) / (K + (exp_value - 1) * P0)


def predictHIndex(prime):
    t = [2009, 2010, 2011, 2012, 2013, 2014,
         2015, 2016, 2017, 2018, 2019, 2020]
    t = np.array(t)
    P = np.array(prime)

    # 用最小二乘法估计拟合
    popt, pcov = curve_fit(logistic_increase_function, t, P)
    P_predict = logistic_increase_function(t, popt[0], popt[1], popt[2])
    tomorrow = [2021, 2022, 2023, 2024, 2025]
    tomorrow = np.array(tomorrow)
    tomorrow_predict = logistic_increase_function(
        tomorrow, popt[0], popt[1], popt[2])
    predictData = tomorrow_predict.tolist()
    for i in range(len(predictData)):
        predictData[i] = math.ceil(predictData[i])
    print(predictData)
    # for d in predictData:
    #     prime.append(int())
    returnData = prime + predictData
    for i in range(len(returnData)):
        if i > 0 and returnData[i] < returnData[i - 1]:
            returnData[i] = returnData[i-1]
    # plot1 = plt.plot(t, P, 's', label="Confimed H-Index")
    # plot2 = plt.plot(t, P_predict, 'r', label='Predict H-Index')
    # plot3 = plt.plot(tomorrow, tomorrow_predict, 's', label='Predict H-Index')
    # print(tomorrow_predict)
    # print(tomorrow_predict[1])
    # plot2 = plt.plot(tomorrow, tomorrow_predict_fast, 's', label='predict infected people number fast')
    # plot3 = plt.plot(tomorrow, tomorrow_predict_fast, 'r')
    # plot4 = plt.plot(tomorrow, tomorrow_predict_slow, 's', label='predict infected people number slow')
    # plot5 = plt.plot(tomorrow, tomorrow_predict_slow, 'g')
    # plot6 = plt.plot(t, P_predict_fast, 'b', label='confirmed infected people number')

    # plt.xlabel('Year')
    # plt.ylabel('H-Index')

    # plt.legend(loc=0)  # 指定legend的位置右下角
    #
    # print("32\n")
    # # print(faster_logistic_increase_function(np.array(32), popt_fast[0], popt_fast[1]))
    # # print(slower_logistic_increase_function(np.array(32), popt_slow[0], popt_slow[1]))
    #
    # print("33\n")
    # # print(faster_logistic_increase_function(np.array(33), popt_fast[0], popt_fast[1]))
    # # print(slower_logistic_increase_function(np.array(33), popt_slow[0], popt_slow[1]))

    # plt.show()
    print("Program done!")
    return show(returnData)


def show(data):
    t = [2009, 2010, 2011, 2012, 2013, 2014,
         2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
    newlist = [str(x) for x in t]
    background_color_js = "new echarts.graphic.LinearGradient(0, 0, 0, 1,[{offset: 0, color: '#c86589'}, {offset: 1, color: '#06a7ff'}], false)"
    area_color_js = "new echarts.graphic.LinearGradient(0, 0, 0, 1,[{offset: 0, color: '#eb64fb'}, {offset: 1, color: '#3fbbff0d'}], false)"
    
    c = (
        Line(init_opts=opts.InitOpts(bg_color=JsCode(background_color_js)))
        .add_xaxis(xaxis_data=newlist)
        .add_yaxis(
            series_name="h指数",
            y_axis=data,
            is_smooth=True,
            is_symbol_show=True,
            symbol="circle",
            symbol_size=6,
            linestyle_opts=opts.LineStyleOpts(color="#fff"),
            label_opts=opts.LabelOpts(
                is_show=True, position="top", color="white"),
            itemstyle_opts=opts.ItemStyleOpts(
                color="red", border_color="#fff", border_width=3
            ),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            areastyle_opts=opts.AreaStyleOpts(
                color=JsCode(area_color_js), opacity=1),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="h指数",
                pos_bottom="5%",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(
                    color="#fff", font_size=16),
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                boundary_gap=False,
                axislabel_opts=opts.LabelOpts(margin=30, color="#ffffff63"),
                axisline_opts=opts.AxisLineOpts(is_show=False),
                axistick_opts=opts.AxisTickOpts(
                    is_show=True,
                    length=25,
                    linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
                ),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
                ),
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                position="right",
                axislabel_opts=opts.LabelOpts(margin=20, color="#ffffff63"),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(width=2, color="#fff")
                ),
                axistick_opts=opts.AxisTickOpts(
                    is_show=True,
                    length=15,
                    linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
                ),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
                ),
            ),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )
    c.render("predict.html")
    return c


def predict(name):
    data = get_h_index_from_db()
    prime = []
    for i in range(len(data)):
        if data[i]['name'] == name:
            prime.append(int(data[i]['h_index_1']))
            prime.append(int(data[i]['h_index_2']))
            prime.append(int(data[i]['h_index_3']))
            prime.append(int(data[i]['h_index_4']))
            prime.append(int(data[i]['h_index_5']))
            prime.append(int(data[i]['h_index_6']))
            prime.append(int(data[i]['h_index_7']))
            prime.append(int(data[i]['h_index_8']))
            prime.append(int(data[i]['h_index_9']))
            prime.append(int(data[i]['h_index_10']))
            prime.append(int(data[i]['h_index_11']))
            prime.append(int(data[i]['h_index_now']))
            break
    return predictHIndex(prime)

# predict('Hendrik Zender')
