from aidd.common.logger import *
import os
from typing import Dict,List,Tuple
import tornado
import json

def success_aidd_response(request_id:str,data:dict):
    response={
        "requestId":request_id,
        "code":200,
        "data":data,
        "message":"success"
    }
    return response

def success_aidd_response(request_id:str,data:list):
    response={
        "requestId":request_id,
        "code":200,
        "data":data,
        "message":"success"
    }
    return response
def fail_response(request_id:str,message:str,code:int):
    response={
        "requestId":request_id,
        "code":code,
        "message":message
    }
    return response