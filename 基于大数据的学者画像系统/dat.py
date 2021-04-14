import json
import pymysql
import os
db = pymysql.connect(host='121.196.111.9',
                     port=3306,
                     user='test',
                     passwd='123456',
                     db='blogs'
                     )


def get_data():
    with open('jsonFile.json', 'r', encoding='utf-8') as f:
        author_text = json.load(f)
    return author_text


def get_h_index():
    print("!11111111")
    print(os.getcwd())
    with open('H_indexes.json', 'r', encoding='utf-8') as f:
        index_text = json.load(f)
    return index_text


# flag = 0:Blurry Search, flag = 1:Precise Search
def blurry_precise_search(author_name, flag):
    cursor = db.cursor()
    if flag == 0:
        query = "select * from Scholar where name like '%%%%%s%%%%'" % author_name
    else:
        query = "select * from Scholar where name = '%s'" % author_name
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    data = []
    for i in range(len(result)):
        s = result[i][5].lstrip('[')
        s = s.rstrip(']')
        interest = s.split(",")
        tmp_result = {'id': result[i][0],
                      'name': result[i][1],
                      'name_zh': result[i][2],
                      'position': result[i][3],
                      'h_index': result[i][4],
                      'interests': interest}
        data.append(tmp_result)
    return data


def index_insert(index_text):
    i = 0
    while True:
        value_index = (index_text[i]['name'],
                       int(index_text[i]['h-index_1']),
                       int(index_text[i]['h-index_2']),
                       int(index_text[i]['h-index_3']),
                       int(index_text[i]['h-index_4']),
                       int(index_text[i]['h-index_5']),
                       int(index_text[i]['h-index_6']),
                       int(index_text[i]['h-index_7']),
                       int(index_text[i]['h-index_8']),
                       int(index_text[i]['h-index_9']),
                       int(index_text[i]['h-index_10']),
                       int(index_text[i]['h-index_11']),
                       int(index_text[i]['h-index_now']))
        print(value_index)
        insert_index = "insert into Hindex(name,h_index_1,h_index_2,h_index_3,h_index_4,h_index_5,h_index_6,h_index_7,h_index_8,h_index_9,h_index_10,h_index_11,h_index_now) values ('%s',%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d)"%(index_text[i]['name'],
                       int(index_text[i]['h-index_1']),
                       int(index_text[i]['h-index_2']),
                       int(index_text[i]['h-index_3']),
                       int(index_text[i]['h-index_4']),
                       int(index_text[i]['h-index_5']),
                       int(index_text[i]['h-index_6']),
                       int(index_text[i]['h-index_7']),
                       int(index_text[i]['h-index_8']),
                       int(index_text[i]['h-index_9']),
                       int(index_text[i]['h-index_10']),
                       int(index_text[i]['h-index_11']),
                       int(index_text[i]['h-index_now']))
        cursor = db.cursor()
        print(insert_index)
        try:
            cursor.execute(insert_index)
            db.commit()
        except Exception:
            print("a")
        i += 1
    db.close()

def data_insert(author_text):

    i = 0
    while True:
        value_author = (author_text['experts'][i]['id'], author_text['experts'][i]['name'],
                        author_text['experts'][i]['name_zh'], author_text['experts'][i]['position'],
                        int(author_text['experts'][i]['h_index']), str(author_text['experts'][i]['interests']))
        insert_author = "insert into Scholar(id,name,name_zh,position,h_index,interests) values (%s,%s,%s,%s,%s,%s)"
        cursor = db.cursor()
        cursor.execute(insert_author, value_author)
        db.commit()
        cursor.close()
        i += 1


def getAllScholar():
    try:
        # 1.创建mysql数据库连接对象connection
        # connection对象支持的方法有cursor(),commit(),rollback(),close()
        # 2.创建mysql数据库游标对象 cursor
        # cursor对象支持的方法有execute(sql语句),fetchone(),fetchmany(size),fetchall(),rowcount,close()
        cur = db.cursor()
        # 3.编写sql
        sql = "SELECT * FROM Scholar"
        # 4.执行sql命令
        # execute可执行数据库查询select和命令insert，delete，update三种命令(这三种命令需要commit()或rollback())
        cur.execute(sql)
        # 5.获取数据
        # fetchall遍历execute执行的结果集。取execute执行后放在缓冲区的数据，遍历结果，返回数据。
        # 返回的数据类型是元组类型，每个条数据元素为元组类型:(('第一条数据的字段1的值','第一条数据的字段2的值',...,'第一条数据的字段N的值'),(第二条数据),...,(第N条数据))
        data = cur.fetchall()
        # 6.关闭cursor
        cur.close()
        # 7.关闭dbection
        # db.close()
        jsonData = []
        # 循环读取元组数据
        # 将元组数据转换为列表类型，每个条数据元素为字典类型:[{'字段1':'字段1的值','字段2':'字段2的值',...,'字段N:字段N的值'},{第二条数据},...,{第N条数据}]
        n = 0
        for i in range(len(data)):
            result = {'id': data[i][n + 0], 'name': data[i][n + 1], 'name_zh': data[i][n + 2], 'position': data[i][n + 3],
                      'h_index': data[i][n + 4], 'interests': data[i][n + 5]}
            jsonData.append(result)
          #  n += 6

        return jsonData

    except:
        print('MySQL connect fail...')


def DataToJson():
    try:
        # 1.创建mysql数据库连接对象connection
        # connection对象支持的方法有cursor(),commit(),rollback(),close()
        # 2.创建mysql数据库游标对象 cursor
        # cursor对象支持的方法有execute(sql语句),fetchone(),fetchmany(size),fetchall(),rowcount,close()
        cur = db.cursor()
        # 3.编写sql
        sql = "SELECT * FROM Scholar"
        # 4.执行sql命令
        # execute可执行数据库查询select和命令insert，delete，update三种命令(这三种命令需要commit()或rollback())
        cur.execute(sql)
        # 5.获取数据
        # fetchall遍历execute执行的结果集。取execute执行后放在缓冲区的数据，遍历结果，返回数据。
        # 返回的数据类型是元组类型，每个条数据元素为元组类型:(('第一条数据的字段1的值','第一条数据的字段2的值',...,'第一条数据的字段N的值'),(第二条数据),...,(第N条数据))
        data = cur.fetchall()
        # 6.关闭cursor
        cur.close()
        # 7.关闭dbection
        # db.close()
        jsonData = []
        # 循环读取元组数据
        # 将元组数据转换为列表类型，每个条数据元素为字典类型:[{'字段1':'字段1的值','字段2':'字段2的值',...,'字段N:字段N的值'},{第二条数据},...,{第N条数据}]
        n = 0
        for i in range(len(data)):
            result = {'id': data[i][n + 0], 'name': data[i][n + 1], 'name_zh': data[i][n + 2], 'position': data[i][n + 3],
                      'h_index': data[i][n + 4], 'interests': data[i][n + 5]}
            jsonData.append(result)
          #  n += 6

        jsondatar = json.dumps(jsonData)
       # print(jsondatar)
       # f = open("authors2.json", "a")
        with open("jsonFile.json", "w+") as f:
            f.write(jsondatar)
            f.flush()
            f.close()
        # 去除首尾的中括号
        authordict = json.loads(jsondatar)
        return authordict

    except:
        print('MySQL connect fail...')

def get_h_index_from_db():
    try:
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
        print(len(jsonData[0]))

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

def get_info_by_name(scholar_name):
	c = db.cursor()
	query = "select * from Scholar_info where name = %s"
	c.execute(query,scholar_name)
	data = c.fetchall()
	print(data)
	return data

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_info_by_name("Yikang He")
