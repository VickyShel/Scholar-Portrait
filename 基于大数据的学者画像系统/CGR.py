import json
import os
import random
import math
import dat
from pyecharts.charts import WordCloud, Graph
from pyecharts import options as opts
from pyecharts.globals import SymbolType

scholars = []
in_map = {}
countt = {}
W = []


def getAuthorsGraph(authors):
    # author_nodes.append({"name": authors[0]['name'], "symbolSize": 100});
    # print(len(authors))
    cnt = len(authors)
    author_links = []
    author_nodes = []
    print(cnt)
    for i in range(cnt):
        print(i, authors[i])
        author_nodes.append(
            {"name": authors[i][0]['name'], "symbolSize": (cnt - i) * ((50-cnt)/3), "itemStyle": {"normal": {"color": "none"}},
             "value": authors[i][1]})
        author_links.append(
            {"source": authors[0][0]['name'], "target": authors[i][0]['name'], "value": (cnt - i) * 5})

    # print(author_links)
    author_graph = Graph(init_opts=opts.InitOpts(width='1000px',
                                                 height='1000px',
                                                 page_title='学者关系'))

    author_graph.add("", author_nodes, author_links,
                     edge_length=200,
                     is_draggable=True,
                     layout='force',
                     repulsion=1000,
                     is_rotate_label=True,
                     symbol='image://static/img/scientist.png'
                     )
    author_graph.render("CGR.html")
    return author_graph


def getScholar(target=None):
    scholars = dat.getAllScholar()
    return work(scholars, target)


def work(scholars, target):
    for interest in target['interests']:
        W.append(interest)
    cnt = 0
    for scholar in scholars:
        for interest in scholar['interests']:
            if interest not in W:
                cnt = cnt + 1
                in_map[interest] = cnt
                W.append(interest)

    v1 = []
    results = []
    mod1 = 0.0
    mod2 = 0.0
    for i in range(len(W)):
        if W[i] in target['interests']:
            v1.append(float(1 / (target['interests'].index(W[i]) + 1)))
        else:
            v1.append(0)
        mod1 += v1[i] * v1[i]
    names = []
    for scholar in scholars:
        if scholar['name'] in names:
            continue
        names.append(scholar['name'])
        tot = 0
        v2 = []
        mod2 = 0.0
        if len(scholar['interests']) == 0:
            continue
        for i in range(len(W)):
            if W[i] in scholar['interests']:
                v2.append(float(1 / (scholar['interests'].index(W[i]) + 1)))
            else:
                v2.append(0)
            tot += v1[i] * v2[i]
            mod2 += v2[i] * v2[i]
        mod1 = math.sqrt(mod1)
        mod2 = math.sqrt(mod2)
        co = float(tot / (mod1 * mod2))

        if co <= float(0.0):
            continue
        # print(co, co <= float(0.0))
        results.append((scholar, co))

    if len(results) < 5:
        for scholar in scholars:
            if random.randint(100, 1000) % 2 == 0 and len(results) < 5:
                flag = False
                for s in results:
                    if s[0]['name'] == scholar['name']:
                        flag = True
                        break
                if flag == True:
                    continue
                results.append((scholar, random.randint(100, 1000) / 1000))

    results=sorted(results, key=lambda x: x[1],reverse=True)
    print(results)
   # show_authors_html(results)

    return getAuthorsGraph(results)


if __name__ == '__main__':
    getScholar()
