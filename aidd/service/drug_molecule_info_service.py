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
        result=self.mysqlhelper.selectall("select smiles from "
                                          " where name=%s",(name))
        if result>0:
            return result

        return None

    def seachSmilesLimitNumber(self,number):
        result=self.mysqlhelper.selectall("select name,smiles from chatdd_drug_molecule_info limit %s",(number))
        if result>0:
            return result
        return None

