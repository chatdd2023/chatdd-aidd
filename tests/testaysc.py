import json

import tornado.httpclient
import tornado.ioloop
import tornado.log
import tornado.httpclient


class AsyncHttpClient:
    def __init__(self, timeout=None):
        self.http_client = tornado.httpclient.AsyncHTTPClient()
        self.timeout = timeout

    async def post(self, url, headers=None, data=None):
        try:
            data=json.dumps(data)
            response = await self.http_client.fetch(url, method="POST", headers=headers, body=data,request_timeout=self.timeout,connect_timeout=self.timeout)
            return response.body
        except tornado.httpclient.HTTPError as e:
            raise e
        except tornado.ioloop.TimeoutError as e:
            raise e
        except Exception as e:
            raise e

async def main():
    http_client = AsyncHttpClient(timeout=5)  # 创建客户端实例，设置超时时间为5秒
    url = "http://pre-chat.pharmolix.com/generate"  # 替换为你要POST请求的URL
    headers = {"Content-Type": "application/json"}  # 可选，设置请求头信息
    data = {"prompt":"你好"}  # 替换为你要POST的数据，此处为JSON格式的字节串
    try:
        response_body = await http_client.post(url, headers=headers, data=data)
        print(response_body)
    except Exception as e:
        print("An error occurred:", str(e))

tornado.ioloop.IOLoop.current().run_sync(main)