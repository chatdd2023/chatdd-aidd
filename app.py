import tornado.web

from aidd.hander.dp_sider_hander import DpSiderHandler
from aidd.hander.dp_tox_hander import DpToxHandler
from aidd.hander.dti_hander import DtiHandler
from aidd.config.env import *  # 导入 os 模块，其中包含了环境变量
from aidd.common.logger import *

'''
   功能：
   author:boge
   date:2023-10-30
'''

url_patterns = [
    (r"/tooling/dti", DtiHandler),
    (r"/tooling/dptox",DpToxHandler),
    (r"/tooling/dpsider",DpSiderHandler),
]

if __name__ =="__main__":
    logger_ouput_INFO(None,"__main__","__main__","开始启动")
    app = tornado.web.Application(url_patterns)
    http_server = tornado.httpserver.HTTPServer(app)

    if args.num_process == 1:
        http_server.listen(args.http_port)
        logger_ouput_INFO(None, "__main__", "__main__", f"启动成功{args.http_port}")
        tornado.ioloop.IOLoop.instance().start()
        logger.info("服务启动成功")
    else:
        http_server.bind(args.http_port)
        http_server.start(num_processes=args.num_process)
        logger_ouput_INFO(None, "__main__", "__main__", f"启动成功{args.http_port}")
        tornado.ioloop.IOLoop.instance().start()




