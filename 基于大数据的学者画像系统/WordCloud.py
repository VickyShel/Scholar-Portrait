import json
import os
import random

from pyecharts.charts import WordCloud
from pyecharts import options as opts
from pyecharts.globals import SymbolType

scholars = []
papers = []
countt = {}
works = {}
concepts = []


def getCloud():
    file_path = "authors.txt"
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        try:
            for line in f:
                r = json.loads(line)
                # print(r.get("experts"))
                scholars = list(r.get("experts"))
        except Exception as e:
            print(e)
            f.close()
    show(scholars[1])


def show(theScholar):

    words = []
    cnt = len(theScholar['interests'])
    for i in range(cnt):
        value = int((cnt-i+1)*1000/cnt+100)
        p = (theScholar['interests'][i],)
        p2 = (value,)
        p3 = p + p2
        words.append(p3)
    # for word in theScholar['interests']:
    #     p = (word,)
    #     #p2 = (random.randint(100, 1000),)
    #     p2 = (,)
    #     p3 = p + p2
    #     words.append(p3)
    c = (
        WordCloud()
        .add("", words, word_size_range=[20, 50], shape='diamond', is_draw_out_of_bound=True)
        # .set_global_opts(title_opts=opts.TitleOpts(title="WordCloud"))
    )
    return c


if __name__ == '__main__':
    getCloud()
