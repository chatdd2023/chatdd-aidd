from rdkit import Chem
import time,datetime

from aidd.service.drug_molecule_info_service import DrugMoleculeInfo
import pubchempy as pcp
'''
  功能：常用功能类
  author:boge
  date:2023-10-30
'''
def transition_to_canonical(smile):
    # 将smiles转为标准canonical格式。判断一下输入是否合法，如果是一个错误的格式smiles，返回None
    try:
        mol = Chem.MolFromSmiles(smile)
        smi_clean = Chem.MolToSmiles(mol, isomericSmiles=False, canonical=True)
        return smi_clean
    except Exception as err:
        return None

def get_canonical(compound):
    input_result = transition_to_canonical(compound)
    if input_result is None:
        drugMoleculeInfo = DrugMoleculeInfo()
        input_result = drugMoleculeInfo.seachSmilesByName(compound)
        if input_result is None:
            pcp_result = pcp.get_properties('CanonicalSMILES', compound, 'name')
            if len(pcp_result) > 0:
                input_result = pcp_result[0]['CanonicalSMILES']
    return input_result


# 计算两个日期相差天数，自定义函数名，和两个日期的变量名。
def Caltime(date1, date2):
    date1 = time.strptime(date1,"%Y-%m-%d")
    date2 = time.strptime(date2, "%Y-%m-%d")
    date1 = datetime.datetime(date1[0], date1[1], date1[2])
    date2 = datetime.datetime(date2[0], date2[1], date2[2])
    return (date2 - date1).days