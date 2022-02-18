import cv2 as cv
import numpy as np
import potrace
import matplotlib.pyplot as plt
from flask import Flask
from flask_cors import CORS
from flask import request
import json


app = Flask(__name__)
CORS(app)



def get_contour(filename):
    img = cv.imread(filename)
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    edged = cv.Canny(gray, 30, 200)
    return edged[::-1]

def get_trace(data):
    bmp = potrace.Bitmap(data)
    path = bmp.trace(2, potrace.POTRACE_TURNPOLICY_MINORITY, 1.0, 1, .5)
    return path

def get_latex(file):
    latex = []
    path = get_trace(get_contour(file))

    for curve in path.curves:
        segments = curve.segments
        start = curve.start_point
        for segment in segments:
            x0,y0 = start.x,start.y
            if segment.is_corner:
                x1,y1 = segment.c.x,segment.c.y
                x2,y2 = segment.end_point.x,segment.end_point.y
                latex.append('((1-t)%f+t%f,(1-t)%f+t%f)' % (x0, x1, y0, y1))
                latex.append('((1-t)%f+t%f,(1-t)%f+t%f)' % (x1, x2, y1, y2))
                
            else:
                x1, y1 = segment.c1.x,segment.c1.y
                x2, y2 = segment.c2.x,segment.c2.y
                x3, y3 = segment.end_point.x,segment.end_point.y
                latex.append('((1-t)((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f))+t((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f)),(1-t)((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f))+t((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f)))' % (x0, x1, x1, x2, x1, x2, x2, x3, y0, y1, y1, y2, y1, y2, y2, y3))
            start = segment.end_point
    return latex
        

# latex = get_latex('komi.jpg')


@app.route('/')
def index():
    return '<h3>Home</h3>'

@app.route('/init')
def init():
    # frame = request.args.get('frame')
    # print(frame)
    # latex = get_latex(f'./frames/frame{frame}.png')
    latex = get_latex('komi.jpg')
    return json.dumps({'latex':latex})

if __name__ == '__main__':
    app.run()
