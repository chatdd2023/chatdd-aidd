import json
from rdkit import Chem
from aidd.inference.dp_model import DPModel
from aidd.utils.data_utils import DataProcessorFast
import torch

config = json.load(open("/Users/bo.li/chatdd-aidd/aidd/config/mol/graphmvp.json", "r"))
smi_processor = DataProcessorFast(entity_type="molecule", config=config["data"]["mol"])

smi = "OC(=O)c1cc(\C=C\c2ccc(cc2)N2CCOCC2)nc2ccccc12"
# 将smiles转为标准canonical格式。这里需要判断一下输入是否合法，如果是一个错误的smiles，需要系统提示用户纠正
mol = Chem.MolFromSmiles(smi)
smi_clean = Chem.MolToSmiles(mol,isomericSmiles=False, canonical=True)



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

sider_task_num = 27
model = DPModel(config, sider_task_num)
state_dict = torch.load("/Users/bo.li/chatdd-aidd/aidd/model/dp/graphmvp_finetune_SIDER.pth", map_location="cpu")
model.load_state_dict(state_dict["model_state_dict"])


model.eval()
output = []
with torch.no_grad():
    logit_output = model(smi_input).detach().cpu().tolist()[0]
    for ind, i in enumerate(logit_output):
        if i > 0:
            output.append(sider_label[ind])
print(output)


tox_label = ['NR-AR', 'NR-AR-LBD', 'NR-AhR', 'NR-Aromatase', 'NR-ER', 'NR-ER-LBD', 'NR-PPAR-gamma',
             'SR-ARE', 'SR-ATAD5', 'SR-HSE', 'SR-MMP', 'SR-p53']

tox_task_num = 12
model = DPModel(config, tox_task_num)
state_dict = torch.load("/Users/bo.li/chatdd-aidd/aidd/model/dp/graphmvp_finetune_Tox21.pth", map_location="cpu")
model.load_state_dict(state_dict["model_state_dict"])
# model.load_state_dict(state_dict)

model.eval()
output = []
with torch.no_grad():
    logit_output = model(smi_input).detach().cpu().tolist()[0]
    for ind, i in enumerate(logit_output):
        if i > 0:
            output.append(tox_label[ind])
print(output)