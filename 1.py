# -*- coding: utf-8 -*-
from  flask import  Flask,render_template,request,flash
app=Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/test/')
def test():
    return '<h1 style="color:blue"> 测试页面</h1>'

######测试上传
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save('E:/tmp/%s' % f.filename)
        flash('You were successfully logged in')
        return '上传成功'
    return render_template('upload.html')

#########自定义错误返回页面
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__=='__main__':
    app.run()