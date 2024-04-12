from flask import Flask, render_template, request
import pymysql
import GPT2MJ_Web as gm

app = Flask(__name__)


@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/database', methods=['GET', 'POST'])
def database():
    if request.method == 'GET':

        conn = pymysql.connect(host = 'localhost', port = 3306, user = 'root', password = '123456', charset = 'utf8', db = 'CSFDB')
        cursor = conn.cursor(cursor = pymysql.cursors.DictCursor)

        sql = 'SELECT * FROM db'
        cursor.execute(sql)
        db = cursor.fetchall()

        cursor.close()
        conn.close()

        # print(db)

        return render_template('database.html', db = db)
    else:
        pass

@app.route('/pics')
def pics():
    return render_template('pics.html')

@app.route('/article')
def article():
    return render_template('article.html')

@app.route('/print', methods=['GET', 'POST'])
def print():
    return render_template('print.html')

@app.route('/xxx')
def xxx():
    return "待定"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
