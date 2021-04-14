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
page = Page();
# graph = Graph();
countt = {}

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
                            if cnt == 3:
                                break;
                        else:
                            break
                except Exception as e:
                    print(e)
                    f.close()
    #("关系图系列.html")
    os.system("论文作者顺次.html")



def show(paper):
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
    for i in nodes:
        links.append({"source": i.get('name'), "target": nodes[0].get('name')})
    graph = Graph()
    graph.add("", nodes, links,
              edge_length=200,
              is_draggable=True,
              layout='force',
              repulsion=1000,
              is_rotate_label=True,
              )
    #graph.render("关系图系列.html")
    page.add(graph)
    page.render("论文作者顺次.html")

author_links = []
author_nodes = []


def show_authors():
    for paper in papers:
        for author in paper.get("authors"):
            author_nodes.append({"name": author.get("name"), "symbolSize": countt[author.get("name")] * 10});
    new_nodes = sorted(author_nodes, key=lambda e: e.__getitem__('symbolSize'),reverse=True);
    for paper in papers:
        for author in paper.get("authors"):
            for author2 in paper.get("authors"):
                author_links.append({"source": author.get('name'), "target": author2.get('name')})

    author_graph = Graph()
    author_graph.add("", author_nodes, author_links,
                     edge_length=200,
                     is_draggable=True,
                     layout='force',
                     repulsion=1000,
                     is_rotate_label=True
                     )
    author_graph.render("学者关系网.html")

def getScholar():
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
                            for author in r.get("authors"):
                                if author.get("name") in countt:
                                    countt[author.get("name")] += 1;
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
    getPapers();
    getScholar();
    # show_scholar()
    # os.system("关系图系列.html")
