from aidd.db.mysqlhelper import MySqLHelper

'''
     功能：
     author:boge
     date:2023-10-29
'''
class TargetProteinInfoService(object):

    def __init__(self):
       self.mysqlhelper = MySqLHelper()

    def insertTargetProteinInfo (self,name,entry_name,sequence):
        result = self.mysqlhelper.insertone(
            "insert into chatdd_target_protein_info (name,entry_name,sequence) values(%s, %s,%s)",
            (name,entry_name,sequence))
        return result

    def seachSequenceByName(self,name):
        result=self.mysqlhelper.selectall("select name,entry_name,sequence from chatdd_target_protein_info where name=%s",(name))
        if len(result)>0:
            resultlist=[]
            for oneresult in result:
                result=[]
                result.append(oneresult[0])
                result.append(oneresult[1])
                result.append(oneresult[2])
                resultlist.append(result)
            return resultlist
        return None

infoService = TargetProteinInfoService()
#infoService.insertTargetProteinInfo("Protein MGF 100-1R","1001R_ASFK5","MVRLFYNPIKYLFYRRSCKKRLRKALKKLNFYHPPKECCQIYRLLENAPGGTYFITENMTNELIMIAKDPVDKKIKSVKLYLTGNYIKINQHYYINIYMYLMRYNQIYKYPLICFSKYSKIL")
#infoService.insertTargetProteinInfo("Protein MGF 100-1R","1001R_ASFM2","MVRLFHNPIKCLFYRGSRKTREKKLRKSLKKLNFYHPPGDCCQIYRLLENVPGGTYFITENMTNELIMIVKDSVDKKIKSVKLNFYGSYIKIHQHYYINIYMYLMRYTQIYKYPLICFNKYSYCNS")
#infoService.insertTargetProteinInfo("Protein MGF 100-2L","1002L_ASFM2","MGNKESKYLEMCSDEAWLNIPNVFKCIFIRKLFYNKWLKYQEKKLEKRLRLLSFYHAKKDFIGIRDMLQTAPGGSYFITDNITEEFLMLVLKHPEDGSAEFTKLCLKGSCIMIDGYYYDNLDIFLAESPDLYKYPLIRYDR")






#print(infoService.seachSequenceByName("Protein MGF 100-2L"))