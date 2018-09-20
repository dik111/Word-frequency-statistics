# -*- coding: UTF-8 -*-
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import sys
sys.path.append('D:\\python\\Flask_Project')
from app import app

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(8008)
IOLoop.instance().start()

