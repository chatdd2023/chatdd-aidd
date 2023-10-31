import tornado.web
import json
from typing import Dict,List
from aidd.hander.base import fail_response, success_response
from aidd.config.env import *  # 导入 os 模块，其中包含了环境变量

'''
   功能：
   author: boge
   date:2023-10-28
'''
class DpHandler(tornado.web.RequestHandler):
    async def post(self):
        # 检查请求头中的 Content-Type 是否为 application/json
        if self.request.headers.get('Content-Type') != 'application/json':
            # 不是 JSON 类型，返回错误信息
            await self.write(
                json.dumps(fail_response("", 400, "Invalid Content-Type"), ensure_ascii=False
                           ))
            return
        json_body={}
        try:
            # 尝试解析请求体为 JSON
            body = self.request.body.decode('utf-8')
            json_body = json.loads(body)
            request_id = json_body['request_id']
            print(request_id)
        except json.JSONDecodeError:
            # 如果解析失败，返回错误信息
            await self.write(
                    json.dumps(fail_response(request_id, 400,"Invalid JSON request body"), ensure_ascii=False
                               ))
        # 参数检查和业务逻辑处理
        # 如果参数检查不通过，返回失败的 JSON 字符串要
        try:
            errors = self.validate(json_body)
            # 错误返回
            if len(errors) > 0:
                print(json.dumps(fail_response(request_id, 400, str(errors[0])), ensure_ascii=False
                               ))
                self.write(
                    json.dumps(fail_response(request_id, 400, str(errors[0])), ensure_ascii=False
                               ))
                return
            # 此处写成功返回
            request_id = json_body['request_id']

            self.write(json.dumps(success_response(request_id), ensure_ascii=False))


        # 异常返回
        except Exception as e:
            self.write(json.dumps(fail_response(request_id, 400, "internal error"), ensure_ascii=False))

    def validate(self, data: Dict) -> List[str]:
        errors = []
        for key in ["request_id", "data"]:
            if key not in data:
                errors.append(f"Field {key} not found")
                return errors
        return errors


url_patterns = [
    (r"/dp", DpHandler),
]

if __name__ == "__main__":

    app = tornado.web.Application(url_patterns)
    http_server = tornado.httpserver.HTTPServer(app)

    if args.num_process==1:
        print("服务开始启动。。。。")
        http_server.listen(args.http_port)
    else:
        http_server.bind(args.http_port)
        http_server.start(num_processes=args.num_process)

    tornado.ioloop.IOLoop.instance().start()
    print("服务启动成功")
