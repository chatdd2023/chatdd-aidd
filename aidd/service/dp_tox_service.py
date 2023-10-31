import json
import os
from aidd.inference.dp_model import DPModel
from aidd.utils.data_utils import DataProcessorFast
import torch
from aidd.config.env import *  # 导入 os 模块，其中包含了环境变量
from aidd.common.logger import *

tox_label = ['NR-AR', 'NR-AR-LBD', 'NR-AhR', 'NR-Aromatase', 'NR-ER', 'NR-ER-LBD', 'NR-PPAR-gamma',
             'SR-ARE', 'SR-ATAD5', 'SR-HSE', 'SR-MMP', 'SR-p53']
class DpToxService(object):

    def __init__(self):

         self.config = json.load(open(os.getenv("GRAPHMVP_JSON_PATH"),"r"))
         self.model = DPModel(self.config, 12)
         self.state_dict = torch.load(os.getenv("FINETUNE_TOX21_MODEL_PATH"), map_location="cpu")
         self.model.load_state_dict(self.state_dict["model_state_dict"])
         self.model.eval()

    def process(self,request_id,smi_clean):
        logger_ouput_INFO(request_id, "DpToxService", "process", f"DP 药物毒性计算开始  smi_clean:{smi_clean} ")
        smi_processor = DataProcessorFast(entity_type="molecule", config=self.config["data"]["mol"])
        smi_input = smi_processor(smi_clean)
        output_result=self.compute(smi_input, type)
        #将数组转换为集合，并找出它们的交集
        intersection = set(tox_label) & set(output_result)
        result_dict = {item: "+" if item in intersection else "-" for item in tox_label + output_result}
        return result_dict

    def compute(self,smi_input,type):
        output = []
        with torch.no_grad():
            logit_output = self.model(smi_input).detach().cpu().tolist()[0]
            for ind, i in enumerate(logit_output):
                if i > 0:
                    output.append(tox_label[ind])
        return output



