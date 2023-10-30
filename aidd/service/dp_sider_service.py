import json
import os
from aidd.inference.dp_model import DPModel
from aidd.utils.data_utils import DataProcessorFast
import torch
from aidd.config.env import *  # 导入 os 模块，其中包含了环境变量
from aidd.common.logger import *

class DpSiderService(object):

    def __init__(self):
         self.config = json.load(open(os.getenv("GRAPHMVP_JSON_PATH"),"r"))
         self.model = DPModel(self.config, 27)
         self.state_dict = torch.load(os.getenv("FINETUNE_SIDER_MODEL_PATH"), map_location="cpu")
         self.model.load_state_dict(self.state_dict["model_state_dict"])
         self.model.eval()

    def process(self,request_id,smi_clean):
        logger_ouput_INFO(request_id, "DpSiderService", "process", f"DP 药物副作用计算开始  smi_clean:{smi_clean} ")

        sequence=self.target.seachSequenceByName("")
        dtiallresult = {}
        for result in sequence:
            dtiresult = {}
            dtiresult["Target_Name"] = result[0].decode("utf-8")
            dtiresult["Uniprot_ID"] = result[1].decode("utf-8")
            dtiresult["Affinity_Value"] = self.compute(request_id,smi_clean)
            dtiallresult.update(dtiresult)
        return dtiallresult
    def compute(self,request_id,smi_clean):
        smi_processor = DataProcessorFast(entity_type="molecule", config=self.config["data"]["mol"])
        smi_input = smi_processor(smi_clean)
        sider_label = ['Hepatobiliary disorders',
                       'Metabolism and nutrition disorders', 'Product issues', 'Eye disorders',
                       'Investigations', 'Musculoskeletal and connective tissue disorders',
                       'Gastrointestinal disorders', 'Social circumstances',
                       'Immune system disorders', 'Reproductive system and breast disorders',
                       'Neoplasms benign, malignant and unspecified (incl cysts and polyps)',
                       'General disorders and administration site conditions',
                       'Endocrine disorders', 'Surgical and medical procedures',
                       'Vascular disorders', 'Blood and lymphatic system disorders',
                       'Skin and subcutaneous tissue disorders',
                       'Congenital, familial and genetic disorders',
                       'Infections and infestations',
                       'Respiratory, thoracic and mediastinal disorders',
                       'Psychiatric disorders', 'Renal and urinary disorders',
                       'Pregnancy, puerperium and perinatal conditions',
                       'Ear and labyrinth disorders', 'Cardiac disorders',
                       'Nervous system disorders',
                       'Injury, poisoning and procedural complications']

        output = []
        with torch.no_grad():
            logit_output = self.model(smi_input).detach().cpu().tolist()[0]
            for ind, i in enumerate(logit_output):
                if i > 0:
                    output.append(sider_label[ind])
        return logit_output



