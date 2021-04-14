import codecs
import json
import os
import random
from time import sleep
import numpy as np
from pyecharts.charts import Graph, Page, Line3D, Pie
from pyecharts.faker import Faker
from pyecharts import options as opts

path = "training.txt"  # 文件夹目录# 得到文件夹下的所有文件名称
s = []
users = []
tokens = ["id", "title", "authors", "bsmajor", "bsuniv", "email", "fax", "msdate", "msmajor", "msuniv",
          "phddate", "phdmajor", "phduniv", "phone", "position"]
page = Page()
# graph = Graph();
countt = {}


def getORGs():
    user = []
    cnt = 0
    for line in codecs.open(path, 'r', encoding='utf-8'):
        line = line.strip().lower()
        if line == '':
            user_dic = {}
            for item in user:
                item = item.split(':')
                # print (item)
                user_dic[item[0][1:]] = ':'.join(item[1:])
            users.append(user_dic)
            user = []
        else:
            user.append(line)


def show():

    for author in users:
        if author.get("org") in countt:
            countt[author.get("org")] += 1

        else:
            countt[author.get("org")] = 1
    new_dict = sorted(countt.items(), key=lambda x: x[1], reverse=True)
    print(new_dict[:30])
    new_dict = new_dict[:10]
    c = (
        Pie(init_opts=opts.InitOpts(width='800px',
                                    height='800px',
                                    page_title='机构学者数量'))
        .add(
            "",
            new_dict,
            center=["50%", "50%"],
            radius=100
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="机构学者数量"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_left="80%", orient="vertical"),
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        .render("机构学者数量.html")
    )
    os.system("机构学者数量.html")


if __name__ == '__main__':
    getORGs()
    show()
