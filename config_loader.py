import json
import os.path


class Config:
    def __init__(self, file='config.json'):
        # 定义
        self.Ver = 'PYSS-1'
        self.IP = '0.0.0.0'
        self.Port = 8080
        self.SSLCert = None
        self.SSLKey = None

        # 读取
        self.file = file
        if os.path.exists(file):
            self._config = json.load(open(file, 'r', encoding='utf8'))
        else:
            self.write()
            self._config = json.load(open(file, 'r', encoding='utf8'))

        if 'Ver' in self._config:
            self.Ver = self._config['Ver']
        else:
            self._v0read()
            self.write()

        if self.Ver == 'PYSS-1':
            self._v1read()
        else:
            if self.Ver == 'PYSS-1':
                self._v1read()
            self.write()

    def write(self):
        config = {
            "Ver": self.Ver,
            "IP": self.IP,
            "Port": self.Port,
            "SSLCert": self.SSLCert,
            "SSLKey": self.SSLKey
        }
        json.dump(config, open(self.file, 'w', encoding='utf8'))

    def _v1read(self):
        config = self._config
        self.IP = config['IP']
        self.Port = config['Port']
        self.SSLCert = config['SSLCert']
        self.SSLKey = config['SSLKey']

    def _v0read(self):
        config = self._config
        self.IP = config['IP']
        self.Port = config['Port']
        self.SSLCert = config['SSLCert']
        self.SSLKey = config['SSLKey']
