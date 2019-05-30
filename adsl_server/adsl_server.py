import random
import time
import tornado.ioloop
import tornado.web
import redis
import hashlib
from adsl_settings import *

logger = logger(file_name='adsl_server', handel='log')

def get_sign(key):
    sign_raw = MD5(key)
    salt = '46whetf6'
    sign = ''
    for index in range(8):
        sign += sign_raw[index] + salt[index]
    return sign

redis = redis.Redis(**REDIS_SPIDER)
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        keys = redis.keys('proxy_*')
        if keys and redis.get(random.choice(keys)):
            data = redis.get(random.choice(keys))
            logger.info('-----time:{}, back ip:{}'.format(time.strftime("%Y-%m-%d %H:%M:%S"), data))
            self.write(data)
        else:
            self.write('NO PROXY')


    def post(self):
        ip = self.get_body_argument('ip', default=None, strip=False)
        port = self.get_body_argument('port', default='8888', strip=False)
        name = self.get_body_argument('name', default=None, strip=False)
        key = self.get_body_argument('key', default=None, strip=False)
        sign = self.get_body_argument('sign', default=None, strip=False)
        logger.info('----get_proxy_ip: time:{}, ip:{}, port:{}, name:{}, key:{}, sign:{}'.format(time.strftime("%Y-%m-%d %H:%M:%S"), ip, port, name, key, sign))
        if sign == get_sign(key) and ip:
            proxy = ip + ':' + port
            redis.set('proxy_'+name, proxy)
            redis.sadd('use_ips', ip)
        elif sign != get_sign(key):
            self.write('Wrong Token')
        elif not ip:
            self.write('No Client ip')

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()