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
            "insert into chatdd_drug_molecule_info (name,smiles) values(%s, %s)",
            (name,smiles))
        print(result)

    def seachSmilesByName(self,name):
        result=self.mysqlhelper.selectall("select smiles from chatdd_drug_molecule_info where name=%s",(name))
        if len(result)>0:
            return result
        return None

#one=DrugMoleculeInfo()
#one.insert_drug_molecule_info("4,5 dibromorhodamine methyl ester","COC(=O)C1=CC=CC=C1C2=C3C=CC(=N)C(=C3OC4=C2C=CC(=C4Br)N)Br")
#result=one.seachSmilesByName("4,5 dibromorhodamine methyl ester")
#print(len(result))
#print(result[0][0])