from flask import Flask, render_template, request
from datetime import timedelta
import flask_cors
import pymysql
import CGR
import WordCloud
import dat
import json
import newRadar
import NewPredictH
import history
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
cors = flask_cors.CORS(app, resources={r"/*": {"origins": "*"}})
# 打开数据库连接
db = pymysql.connect(host='121.196.111.9',
                     port=3306,
                     user='test',
                     passwd='123456',
                     db='blogs'
                     )
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询
cursor.execute("SELECT VERSION()")

# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchone()

print("Database version : %s " % data)

# 关闭数据库连接
scholarSelected = {}
searchName = ""


@app.route('/searchresult')
def searchresult():
    global searchName
    searchName = request.args.get("name")
    return render_template("search-result.html", scholarName=searchName)


@app.route('/predict')
def predict():
    return render_template("predict.html")


@app.route('/ret')
def ret():
    return render_template("ret.html")


@app.route('/scholar')
def scholar():
    return render_template("scholar.html")


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/getList')
def getList():
    name = request.args.get("name")
    scholars = dat.blurry_precise_search(name, 0)
    return json.dumps(scholars)


@app.route('/graphChart')
def graphChart():
    return CGR.getScholar(scholarSelected).dump_options_with_quotes()


@app.route('/getScholar')
def getScholar():
    return json.dumps(scholarSelected)


@app.route('/getDetail')
def getDeatail():
    name = request.args.get("name")
    global scholarSelected
    scholarSelected = dat.blurry_precise_search(name, 1)[0]
    return json.dumps(scholarSelected)


@app.route('/getWordCloud')
def getWordCloud():
    return WordCloud.show(scholarSelected).dump_options_with_quotes()


@app.route('/getRadar')
def getRadarNow():
    return newRadar.get_radar(scholarSelected['name']).dump_options_with_quotes()


@app.route('/getPredict')
def getPredict():
    return NewPredictH.predict(scholarSelected['name']).dump_options_with_quotes()


@app.route('/getHistory')
def getHistory():
    return history.getHistory(scholarSelected['name']).dump_options_with_quotes()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
