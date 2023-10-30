from rdkit import Chem
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