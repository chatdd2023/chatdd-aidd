from aidd.common.logger import *
import os
from typing import Dict,List,Tuple

logger.info('Info message')
logger.info('error message')
def get_service_description():
    curr_dir=os.path.dirname(os.path.abspath(__file__))
    image_name=open(os.path.join(curr_dir,"docker/IMAGE")).read().strip()
    tag=open(os.path.join(curr_dir,"docker/TAG")).read().strip()
    date=open(os.path.join(curr_dir,"docker/DATE")).read().strip()
    return f"${image_name}:{tag}:{date}"

def fail_response(request_id:str,err_code:int,err_message:str) ->Dict[str,object]:
    response = dict()
    response["requestId"] = request_id
    response["code"] = err_code
    response["message"] = "success"

    return response
def success_response(request_id:str) ->[str,object]:
    response=dict()
    response["requestId"]=request_id
    response["code"]=200
    response["message"]="success"
    return response