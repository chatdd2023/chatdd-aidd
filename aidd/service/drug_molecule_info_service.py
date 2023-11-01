from aidd.db.mysqlhelper import MySqLHelper

'''
     功能：
     author:boge
     date:2023-10-29
'''
class DrugMoleculeInfo(object):

    def __init__(self):
       self.mysqlhelper = MySqLHelper()

    def insert_drug_molecule_info(self,name,smiles):
        result = self.mysqlhelper.insertone(
            "insert into chatdd_drug_molecule_info(name,smiles) values(%s, %s)",
            (name,smiles))
        print(result)

    def seachSmilesByName(self,name):
        result=self.mysqlhelper.selectall("select smiles from chatdd_drug_molecule_info"
                                          " where name=%s",(name))
        if result:
            return result
        return None

    def seachSmilesLimitNumber(self,number):
        result=self.mysqlhelper.selectall("select name,smiles from chatdd_drug_molecule_info limit %s",(number))
        if result:
            return result
        return None

#one=DrugMoleculeInfo()
#one.insert_drug_molecule_info("R-hirudin","CCC(C)C1C(=O)NC(C(=O)NCC(=O)NC(C(=O)NC(C(=O)NCC(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(CSSCC2C(=O)NCC(=O)NC(C(=O)NCC(=O)NC(C(=O)NC(C(=O)NC(CSSCC(C(=O)NC(C(=O)NCC(=O)NC(C(=O)NC(C(=O)NC(C(=O)N2)C(C)C)CC(=O)N)CO)CCC(=O)O)NC(=O)C(CC(C)C)NC(=O)C3CSSCC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NCC(=O)NC(C(=O)NC(C(=O)NC(C(=O)N3)CC(C)C)CC(=O)N)CCC(=O)N)CO)CCC(=O)O)C(C)O)NC(=O)C(CC(=O)O)NC(=O)C(C(C)O)NC(=O)C(CC4=CC=C(C=C4)O)NC(=O)C(C(C)O)NC(=O)C(CC(C)C)N)C(=O)N1)CCCCN)CC(=O)N)CCC(=O)N)C(=O)NC(C(C)C)C(=O)NC(C(C)O)C(=O)NCC(=O)NC(CCC(=O)O)C(=O)NCC(=O)NC(C(C)O)C(=O)N5CCCC5C(=O)NC(CCCCN)C(=O)N6CCCC6C(=O)NC(CCC(=O)N)C(=O)NC(CO)C(=O)NC(CC7=CNC=N7)C(=O)NC(CC(=O)N)C(=O)NC(CC(=O)O)C(=O)NCC(=O)NC(CC(=O)O)C(=O)NC(CC8=CC=CC=C8)C(=O)NC(CCC(=O)O)C(=O)NC(CCC(=O)O)C(=O)NC(C(C)CC)C(=O)N9CCCC9C(=O)NC(CCC(=O)O)C(=O)NC(CCC(=O)O)C(=O)NC(CC1=CC=C(C=C1)O)C(=O)NC(CC(C)C)C(=O)NC(CCC(=O)N)C(=O)O)CCC(=O)N)CC(=O)N)CCCCN)CCC(=O)O)CC(=O)O)CO)CC(C)C")

