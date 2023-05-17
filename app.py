import os

from flask import Flask, request, render_template, url_for, redirect, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
import pygal

ALLOWED_EXTENTIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENTIONS


def create_app():
    app = Flask(__name__)
    @app.route('/', methods=['GET', 'POST'])
    def upload():
        if request.method == 'POST':
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                new_filename = f'{filename.split(".")[0]}_{str(datetime.now().year)}.csv'
                save_location = os.path.join('input', new_filename)
                file.save(save_location)


                lines = open('input/'+new_filename, 'r').readlines()
                year_title = list()
                for i in lines:
                    x = i.strip().split(';')
                    if (x[4]== 'Cage, Nicolas'):
                        year_title.append(x[0]+','+x[2])

                if (len(year_title) == 0):
                    return render_template('uploadEx.html')
                    print(1)
                else:
                    chart = pygal.Bar()
                    for y in year_title:
                        data = y.strip().split(',')
                        chart.add(data[1], int(data[0]))
                    chart.render_in_browser()



        return render_template('upload.html')
    return  app


