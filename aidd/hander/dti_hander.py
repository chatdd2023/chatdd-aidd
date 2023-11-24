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
from aidd.common.utils import transition_to_canonical, get_canonical, get_canonical_query
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
        chat_session_id = None
        try:
            json_data = json.loads(data)
            errors=[]
            errors=validate(json_data)
            if len(errors) > 0:
                # 解析JSON数据失败，返回错误JSON响应
                await self.finish(fail_response(request_id, errors,500))
                return
            request_id = json_data['request_id']
            chat_session_id = json_data.get('chat_session_id', '')
            logger_ouput_INFO(request_id, self.__class__.__name__, "post",
                              f"DTI分子和靶点亲和性计算 请求调用开始  request json : {json_data}",chat_session_id=chat_session_id)

            # 化合物的输入
            compound = json_data['compound']
            input_result=get_canonical_query(compound)
            #print("input_result=======",input_result)
            logger_ouput_INFO(request_id, self.__class__.__name__, "post",
                              f"input_result : {input_result}",chat_session_id=chat_session_id)
            if input_result is None:
               message_compound_error=constant.message_compound_error.replace("{compound name}",compound)
               logger_ouput_Error(request_id, self.__class__.__name__, "post",
                                 f"input_result 为空 : {message_compound_error}",chat_session_id=chat_session_id)
               await self.finish(fail_response(request_id, message_compound_error,400))
               return
            else:
                # 靶点 & 小分子的输入
                dti_service = DTIService()
                dti_all_result = dti_service.process(request_id,input_result, json_data['target'])
                logger_ouput_INFO(request_id, self.__class__.__name__, "post",
                                  f"dti_all_result : {dti_all_result}",chat_session_id=chat_session_id)
                if dti_all_result is None:
                    message_target_error = constant.message_target_error.replace("{target name}", json_data['target'])
                    logger_ouput_Error(request_id, self.__class__.__name__, "post",
                                      f"dti_all_result 为空 : {message_target_error}",chat_session_id=chat_session_id)
                    await self.finish(fail_response(request_id, message_target_error,400))
                    return

                logger_ouput_INFO(request_id,  self.__class__.__name__, "post",
                                  f"DTI 计算结束  response json : {dti_all_result}",chat_session_id=chat_session_id)
                await self.finish(success_aidd_response(request_id, dti_all_result))
                return

        except ValueError:
            # 解析JSON数据失败，返回错误JSON响应
            logger_ouput_Error(request_id, self.__class__.__name__, "post",
                              f"无效的JSON数据: {data}",chat_session_id=chat_session_id)
            await self.finish(fail_response(request_id, "无效的JSON数据",500))
            return

        except Exception as e:
            # 处理异常情况，返回错误JSON响应
            logger_ouput_Error(request_id, self.__class__.__name__, "post",
                              f"{e}",chat_session_id=chat_session_id)
            await self.finish(fail_response(request_id, str(e),500))
            return

def validate(data:Dict)->List[str]:
    errors=[]
    for key in ["request_id","target","compound"]:
        if key not in data:
            errors.append(f"Field {key} not found")
            return errors
    return errors