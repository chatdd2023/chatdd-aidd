'''
   功能：
   author:boge
   date:2023-10-30
'''
import tornado
import json
import aidd
from aidd.common.constants import message_compound_error
from aidd.common.logger import logger_ouput_INFO
from aidd.common.utils import transition_to_canonical, get_canonical
from aidd.service.drug_molecule_info_service import DrugMoleculeInfo
from aidd.service.dti_service import DTIService
from typing import Dict,List
from aidd.hander.base import *
import pubchempy as pcp
import aidd.common.constants as constant
class DtiHandler(tornado.web.RequestHandler):
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
            compound = json_data['compound']
            input_result=get_canonical(compound)

            if input_result is None:
               message_compound_error=constant.message_compound_error.replace("{compound name}",compound)
               await self.finish(fail_response(request_id, message_compound_error,400))

            else:
                # 靶点 & 小分子的输入
                dti_service = DTIService()
                dti_all_result = dti_service.process(request_id,input_result, json_data['target'])
                if dti_all_result is None:
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
    for key in ["request_id","target","compound"]:
        if key not in data:
            errors.append(f"Field {key} not found")
            return errors
    return errors