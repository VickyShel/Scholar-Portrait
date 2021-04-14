import json
import os
import random
from time import sleep
import numpy as np
from pyecharts.charts import Graph, Page, Line3D
from pyecharts.faker import Faker
from pyecharts import options as opts

path = "mag_data"  # 文件夹目录
files = os.listdir(path)  # 得到文件夹下的所有文件名称
s = []
papers = []
tokens = ["id", "title", "authors", "bsmajor", "bsuniv", "email", "fax", "msdate", "msmajor", "msuniv",
          "phddate", "phdmajor", "phduniv", "phone", "position"]


def getPapers():
    # f=open("data/aminer_authors_5.txt");
    for file in files:  # 遍历文件夹
        if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
            file_path = path + "/" + file;
            cnt = 0
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    while True:
                        line = f.readline()
                        if line:
                            r = json.loads(line)
                            papers.append(r)
                            show(r);
                            cnt = cnt + 1
                            if cnt == 10:
                                break;
                        else:
                            break
                except Exception as e:
                    print(e)
                    f.close()
    print(cnt)


page = Page();
graph = Graph();
countt = {}


def show(paper):
    cnt = 0;
    nodes = []
    nodes.append({"name": paper.get("title"), "symbolSize": 100});
    cnt = len(paper.get("authors"));
    try:
        for author in paper.get("authors"):
            nodes.append({"name": author.get("name"), "symbolSize": cnt * 10});
            if author.get("name") in countt:
                countt[author.get("name")] += 1;

            else:
                countt[author.get("name")] = 1;
            cnt = cnt - 1;
    except Exception as e:
        print(e)

    links = []
    # for i in nodes:
    #     for j in nodes:
    #         links.append({"source": i.get('name'), "target": j.get('name')})
    for i in nodes:
        links.append({"source": i.get('name'), "target": nodes[0].get('name')})
    #  graph = Graph()
    graph.add("", nodes, links,
              edge_length=200,
              is_draggable=True,
              layout='force',
              repulsion=100,
              is_rotate_label=True
              )
    graph.render("关系图系列.html")
    page.add(graph)
    page.render("关系图系列.html")


author_links = []
author_nodes = []


def show_authors():
    for paper in papers:
        for author in paper.get("authors"):
            author_nodes.append({"name": author.get("name"), "symbolSize": countt[author.get("name")] * 10});
    new_nodes = sorted(author_nodes, key=lambda e: e.__getitem__('symbolSize'), reverse=True);
    for paper in papers:
        for author in paper.get("authors"):
            for author2 in paper.get("authors"):
                author_links.append({"source": author.get('name'), "target": author2.get('name')})
    author_graph = Graph(init_opts=opts.InitOpts(width='1000px',
                                                 height='1000px',
                                                 page_title='学者关系'))
    author_graph.add("", author_nodes, author_links,
                     edge_length=200,
                     is_draggable=True,
                     layout='force',
                     repulsion=1000,
                     is_rotate_label=True
                     )
    author_graph.set_global_opts(visualmap_opts=opts.VisualMapOpts(range_color=[]))
    author_graph.render("学者关系网.html")


def getScholar():
    for file in files:  # 遍历文件夹
        if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
            file_path = path + "/" + file;
            cnt = 0
            mostname = ''
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    while True:
                        line = f.readline()
                        if line:
                            r = json.loads(line)
                            print(r)
                            papers.append(r)
                            for author in r.get("authors"):
                                if author.get("name") in countt:
                                    countt[author.get("name")] += 1;
                                    if cnt < countt[author.get("name")]:
                                        cnt = countt[author.get("name")]
                                        mostname=author.get("name")
                                else:
                                    countt[author.get("name")] = 1;

                            cnt = cnt + 1
                            if cnt == 100:
                                break;
                        else:
                            break
                except Exception as e:
                    print(e)
                    f.close()

    show_authors();
    os.system("学者关系网.html")


if __name__ == '__main__':
    getScholar();
