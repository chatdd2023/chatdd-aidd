'''
   功能：
   author:boge
   date:2023-10-30
'''

from aidd.common.utils import get_canonical_query
from aidd.hander.base import *
import aidd.common.constants as constant
from aidd.db.redishelper import RedisHelper
from aidd.service.target_protein_info_service import TargetProteinInfoService
class DtiLocalHandler(tornado.web.RequestHandler):
    async def post(self):
        data = self.request.body.decode("utf-8")
        request_id=None
        try:
            json_data = json.loads(data)
            errors=[]
            errors=validate(json_data)
            if len(errors) > 0:
                # 解析JSON数据失败，返回错误JSON响应
                await self.finish(fail_response(request_id, errors))
            request_id = json_data['request_id']
            logger_ouput_INFO(request_id, "__main__", "__main__", f"请求调用开始  request json : {json_data}")

            # 化合物的输入
            target = json_data['target']
            top_n = int(json_data['top_n'])
            entry_names = transit_target2entry_name(target)
            logger_ouput_INFO(request_id, "__main__", "__main__", f"请求调用开始  entry_names : {entry_names}")
            if entry_names is None:
               message_target_error = constant.message_target_error.replace("{target name}", json_data['target'])
               await self.finish(fail_response(request_id, message_target_error,400))
            else:
                # 靶点 & 小分子的输入
                dti_all_result={}
                for entry_name in entry_names:
                    print("==========entry_name",entry_name)
                    one_result = get_rank_molecule(entry_name,top_n)
                    if one_result:
                        dti_all_result.setdefault(entry_name,one_result)
                if dti_all_result is None or len(dti_all_result)==0:
                    message_target_error = constant.message_target_error.replace("{target name}", json_data['target'])
                    await self.finish(fail_response(request_id, message_target_error,400))
                logger_ouput_INFO(request_id, "__main__", "__main__", f"DTI 计算结束  response json : {dti_all_result}")
                await self.finish(success_aidd_response(request_id, dti_all_result))

        except ValueError:
            # 解析JSON数据失败，返回错误JSON响应
            await self.finish(fail_response(request_id, "无效的JSON数据",500))

        except Exception as e:
            # 处理异常情况，返回错误JSON响应
            await self.finish(fail_response(request_id, str(e),500))

def validate(data:Dict)->List[str]:
    errors=[]
    for key in ["request_id","target","top_n"]:
        if key not in data:
            errors.append(f"Field {key} not found")
            return errors
    return errors

def transit_target2entry_name(target):
    lines = TargetProteinInfoService().seachSequenceByName(target)
    if not lines or len(lines)==0:
        return None
    ans=[]
    for line in lines:
        ans.append(line[1].decode())
    return ans

def get_rank_molecule(entry_name,top_n) ->Dict[str,int]:
    redishelper = RedisHelper()
    _dict = redishelper.search_float(f"*++{entry_name}")
    if not _dict or len(_dict)==0:
        return None
    sorted_dict = dict(sorted(_dict.items(), key=lambda item: item[1]))
    return dict(list(sorted_dict.items())[:top_n])