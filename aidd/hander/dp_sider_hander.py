'''
   功能：
   author:boge
   date:2023-10-30
'''
import tornado
import json
import aidd
from aidd.common.logger import logger_ouput_INFO
from aidd.common.utils import transition_to_canonical
from aidd.service.dp_sider_service import DpSiderService
from aidd.service.dp_tox_service import DpToxService
from aidd.service.drug_molecule_info_service import DrugMoleculeInfo
from typing import Dict,List
from aidd.hander.base import *

class DpSiderHandler(tornado.web.RequestHandler):
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
            logger_ouput_INFO(request_id, "__main__", "__main__", f"药物副作用请求调用开始  request json : {json_data}")
            # 化合物的输入
            compound = json_data['compound']
            drugMoleculeInfo = DrugMoleculeInfo()
            smiles = drugMoleculeInfo.seachSmilesByName(compound)
            # 检索drog库 如果结果不为None
            if smiles is not None:
                inputsmiresult = transition_to_canonical(smiles[0][0])
            # 如果为None 则直接转换输入的化合物
            else:
                inputsmiresult = transition_to_canonical(compound)

            # 如果转换的结果为None 则返回错误结果
            if inputsmiresult is None:
                await self.finish(fail_response(request_id, "compound format error"))

            dpsider_service=DpSiderService()
            dptsider_all_result = dpsider_service.process(request_id,inputsmiresult)
            await self.finish(success_aidd_response(request_id, dptsider_all_result))

        except ValueError:
            # 解析JSON数据失败，返回错误JSON响应
            await self.finish(fail_response(request_id, "无效的JSON数据"))
        except Exception as e:
            # 处理异常情况，返回错误JSON响应
            await self.finish(fail_response(request_id, str(e)))

def validate(data:Dict)->List[str]:
    errors=[]
    for key in ["request_id","compound"]:
        if key not in data:
            errors.append(f"Field {key} not found")
            return errors
    return errors