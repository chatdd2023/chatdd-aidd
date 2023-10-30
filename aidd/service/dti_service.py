import json
import os
from aidd.inference.dti_model import DTIModel
from aidd.service.target_protein_info_service import TargetProteinInfoService
from aidd.utils.data_utils import DataProcessorFast
import torch
import numpy as np
from aidd.config.env import *  # 导入 os 模块，其中包含了环境变量
from aidd.common.logger import *

class DTIService(object):

    def __init__(self):
         self.config = json.load(open(os.getenv("MGRAPHDTA_JSON_PATH"),"r"))
         self.target=TargetProteinInfoService()
         self.model = DTIModel(self.config["network"], pred_dim=1)
         self.state_dict = torch.load(os.getenv("DTI_MODEL_PATH"), map_location="cpu")

    def process(self,request_id,smi_clean,target):
        logger_ouput_INFO(request_id, "DTIService", "process", f"DTI 计算开始  smi_clean:{smi_clean} target:{target}")
        sequence=self.target.seachSequenceByName(target)
        dtiallresult = {}
        for result in sequence:
            dtiresult = {}
            dtiresult["Target_Name"] = result[0].decode("utf-8")
            dtiresult["Uniprot_ID"] = result[1].decode("utf-8")
            dtiresult["Affinity_Value"] = self.compute(request_id,smi_clean, result[2].decode('utf-8'))
            dtiallresult.update(dtiresult)
        return dtiallresult
    def compute(self,request_id,smi_clean,sequence):

        try:
            processor1 = DataProcessorFast(entity_type="molecule", config=self.config["data"]["mol"])
            processor2 = DataProcessorFast(entity_type="protein", config=self.config["data"]["protein"])

            smi_input = processor1(smi_clean)
            sequence_input = processor2(sequence)

            self.model.load_state_dict(self.state_dict["model_state_dict"])
            self.model.eval()

            with torch.no_grad():
                logit = self.model(smi_input, sequence_input)  # standard value is Kd in nM（pKd = -math.log10(Kd/1e9)）
                logit_output=np.array(logit.detach().cpu()).tolist()
                logit_output_rounded_x = round(logit_output, 3)
                return logit_output_rounded_x
        except Exception as e:
            logger_ouput_Error(request_id,"__main__", "__main__", f"{str(e)}")

