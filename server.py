import hashlib
import importlib
import logging
import os.path
import platform
import sys
from types import FunctionType

from flask import Flask, request, Response
from flask_cors import CORS
from gevent import pywsgi

from config_loader import Config
from util import request_parse


class Server:
    def __init__(self, config: Config):
        # 初始化Flask对象
        self.app = Flask(__name__)

        CORS(self.app)

        # 初始化变量
        self.address = (config.IP, config.Port)
        self.get_todo_list_count = {}
        self.config = config
        self.ver = '0.0.1'
        self.logger = logging.getLogger(__name__)

        self.files_hash = {}

        @self.app.route('/<path:name>', methods=['GET'])
        def main(name: str):
            path = os.path.join('scripts', *(name.split('/')))
            module_name = '.'.join(['scripts'] + name.split('.')[0].split('/'))
            req_data = request_parse(request)
            if os.path.exists(path):
                with open(path, 'rb') as f:
                    file_hash = hashlib.sha1(f.read()).hexdigest()
                    if path in self.files_hash:

                        if file_hash != self.files_hash[path]:
                            self.files_hash[path] = file_hash

                            importlib.reload(importlib.import_module(module_name))
                    else:

                        self.files_hash[path] = file_hash
                module = importlib.import_module(module_name)
                func_main: FunctionType = getattr(module, 'main')

                try:
                    rt_type = getattr(module, 'return_type')
                except:
                    rt_type = None
                args_list = []
                for i in func_main.__annotations__:
                    if i in func_main.__annotations__:
                        args_list.append(func_main.__annotations__[i](req_data[i]))
                    else:
                        return 'Error:The parameter does not match {}'.format(str(func_main.__annotations__)), 400

                try:
                    rst = func_main(*args_list)
                except Exception as err:
                    return err, 500
                if rt_type is not None:
                    return Response(response=rst, content_type=rt_type)
                else:
                    return Response(response=rst, content_type='application/octet-stream')
            else:
                return 'No found.', 404

    def start(self):
        self.logger.info('Server is starting up...')
        self.logger.info('Server is listening to {}:{}.'.format(self.address[0], self.address[1]))
        self.logger.info('----Server is loaded----')
        self.logger.info('Version:{}'.format(self.ver))
        self.logger.info('Py ver:{}'.format(sys.version))
        self.logger.info('SYS ver:{}'.format(platform.platform()))
        self.logger.info('------------------------')
        server = pywsgi.WSGIServer((self.address[0], self.address[1]), self.app)
        server.serve_forever()
