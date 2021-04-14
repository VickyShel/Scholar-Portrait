import json
import os
import random

from pyecharts.charts import WordCloud
from pyecharts import options as opts
from pyecharts.globals import SymbolType

scholars = []
path = "mag_data"  # 文件夹目录
files = os.listdir(path)  # 得到文件夹下的所有文件名称
papers = []
countt = {}
works = {}


def getIndex(name):
    for s in scholars:
        if s.get("name") == name:
            return scholars.index(s)
    return -1;


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
                                pos = getIndex(author.get("name"))
                                print(pos)
                                if pos > 0:
                                    scholars[pos]['interests'].append(r.get("title"))
                            #     print(scholars[pos]['interests'])
                            cnt = cnt + 1
                            if cnt == 100000:
                                break;
                        else:
                            break
                except Exception as e:
                    print(e)
                    f.close()


def getCloud():
    file_path = "interest.txt";
    scholar = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            # while True:
            for line in f:
                line = line.strip();
                if line != '':
                    interests = line.split(',');
                    if len(interests) > 1:
                        scholar['interests'] = interests
                        scholars.append(scholar)
                        scholar = {}
                    else:

                        scholar['name'] = ' '.join(reversed(line.split(' ')))
                        print(scholar['name'])

        except Exception as e:
            print(e)
            f.close()


def show():
    cnt = 0;
    pos = 0;
    for s in scholars:
        print(scholars.index(s), len(s['interests']))
        if cnt < len(['interests']):
            cnt = len(['interests'])
            pos = scholars.index(s)
    words = []
    for word in scholars[pos]['interests']:
        p = (word,)
        p2 = (random.randint(100, 1000),)
        p3 = p + p2
        words.append(p3)
    print(words)
    c = (
        WordCloud()
            .add("", words, word_size_range=[20, 50], shape=SymbolType.ROUND_RECT, is_draw_out_of_bound=True)
            .set_global_opts(title_opts=opts.TitleOpts(title="WordCloud"))
            .render("学者词云.html")
    )
    os.system("学者词云.html")


if __name__ == '__main__':
    # print(countt)
    getCloud();
    getScholar()
    show();
