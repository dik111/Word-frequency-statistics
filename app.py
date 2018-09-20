import datetime
from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from collections import Counter
import jieba
import pymysql


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:asd2828@127.0.0.1/edm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))


##自定义表单类
class Databaseform(FlaskForm):
    project = StringField('项目名称：',validators=[DataRequired()])
    startdate = StringField('开始日期：',validators=[DataRequired()])

    enddate = StringField('结束日期：' , validators=[DataRequired()])
    submit = SubmitField('一键导入')







@app.route('/',methods=['GET','POST'])
def index():
    database_form = Databaseform() ##
    yesterday = datetime.date.today() - datetime.timedelta(1)
    yesterday = yesterday.strftime('%Y%m%d')

    if request.method=='POST':

        if database_form.validate_on_submit(): ##如果表单通过验证

            project_name = database_form.project.data
            if database_form.startdate.data>database_form.enddate.data:
                start_day = database_form.startdate.data
                flash('日期范围错误，开始日期不能大于结束日期！')
            else:
                start_day = database_form.startdate.data
                ##结束日期最大为昨天
                if database_form.enddate.data > yesterday:
                    flash('日期超出范围，结束日期最大为昨天！')
                    end_day = database_form.enddate.data
                else:
                    end_day = database_form.enddate.data
                    conn_edm = pymysql.connect(host='127.0.0.1', user='root', password='asd2828', db='edm',
                                               charset="utf8")  ##连接edm数据库
                    cur = conn_edm.cursor()  ##建立游标
                    sql = ''' select `模板标题` from 子任务 where 日期>='%s' and 日期 <= '%s' and 项目 regexp replace('%s','，','|') ''' %(start_day,end_day,project_name)
                    cur.execute(sql)
                    title = cur.fetchall()






        return render_template('home.html', form=database_form, yesterday=yesterday,project_name=project_name,start_day=start_day,end_day=end_day,title=title)


    else:
        return render_template('home.html',form = database_form,yesterday=yesterday)



    return render_template('home.html', form=database_form, yesterday=yesterday, start_day=start_day)
@app.route('/count',methods=['GET','POST'])
def count():
    database_form = Databaseform()  ##
    yesterday = datetime.date.today() - datetime.timedelta(1)
    yesterday = yesterday.strftime('%Y%m%d')

    if request.method == 'POST':

        if database_form.validate_on_submit():  ##如果表单通过验证

            project_name = database_form.project.data
            if database_form.startdate.data > database_form.enddate.data:
                start_day = database_form.startdate.data
                flash('日期范围错误，开始日期不能大于结束日期！')
            else:
                start_day = database_form.startdate.data
                ##结束日期最大为昨天
                if database_form.enddate.data > yesterday:
                    flash('日期超出范围，结束日期最大为昨天！')
                    end_day = database_form.enddate.data
                else:
                    end_day = database_form.enddate.data
                    conn_edm = pymysql.connect(host='127.0.0.1', user='root', password='asd2828', db='edm',
                                               charset="utf8")  ##连接edm数据库
                    cur = conn_edm.cursor()  ##建立游标
                    sql = ''' select `模板标题` from 子任务 where 日期>='%s' and 日期 <= '%s' and 项目 regexp replace('%s','，','|') ''' % (
                    start_day, end_day, project_name)
                    cur.execute(sql)
                    title = cur.fetchall()

        return render_template('count.html', form=database_form, yesterday=yesterday, project_name=project_name,
                               start_day=start_day, end_day=end_day, title=title)

    else:


        user_text = request.args.get('text')

        user_text = user_text.replace('(AD)','')
        list1 = user_text.split('\r\n')
        list2 = list(set(list1))
        list2 = "".join(list2)
        seg_list = jieba.cut(list2)
        c = Counter()
        for x in seg_list:
            if len(x) > 1 and x != '\r\n':
                c[x] += 1
        str1 = '''
                <tr><td bgcolor="#F5DEB3">排名</td>
                    <td bgcolor="#F5DEB3">高频词</td>
                    <td bgcolor="#F5DEB3">词频</td>
                </tr>'''
        html = str1
        try:
            for i in range(20):
                str2 = '''<tr><th>''' + str(i + 1) + '''</td><td>''' + str(c.most_common(20)[i][0]) + '''</td><td>''' + str(
                    c.most_common(20)[i][1]) + '''</td></tr>'''
                html += str2
        except Exception as e:
            html = str1
            print(e)

        return render_template('count.html',html=html,form=database_form,yesterday=yesterday)

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
