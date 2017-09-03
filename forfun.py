# -*- coding: utf-8 -*-
import spider

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

# configuration
DEBUG = True

# create our little application :)
app = Flask(__name__)
app.debug = DEBUG

site = spider.Qiushibaike()

@app.route('/<int:id>')
def page(id=1):
    global site
    return render_template('index.html',entries=site.getPageItems(id))

@app.route('/')
def index():
    return page(1)

if __name__ == '__main__':
    app.run()