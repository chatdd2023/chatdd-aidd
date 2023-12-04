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
        #name可能是entryname
        result=self.mysqlhelper.selectall("select name,entry_name,uniprot_id from chatdd_target_protein_hgnc where lower(name)=lower(%s) or lower(entry_name)=lower(%s)",(name,name))

        if len(result)>0:
            resultlist=[]
            for oneresult in result:
                ans =[]
                ans.append(oneresult[0])
                ans.append(oneresult[1])
                uniprot_id = oneresult[2].decode('utf-8')
                sequence = self.mysqlhelper.selectone("select sequence from chatdd_target_sequence_hgnc where lower(uniprot_id)=lower(%s)",(uniprot_id))
                ans.append(sequence)
                resultlist.append(ans)
            return resultlist
        return None

infoService = TargetProteinInfoService()
#infoService.insertTargetProteinInfo("Protein MGF 100-1R","1001R_ASFK5","MVRLFYNPIKYLFYRRSCKKRLRKALKKLNFYHPPKECCQIYRLLENAPGGTYFITENMTNELIMIAKDPVDKKIKSVKLYLTGNYIKINQHYYINIYMYLMRYNQIYKYPLICFSKYSKIL")
#infoService.insertTargetProteinInfo("Protein MGF 100-1R","1001R_ASFM2","MVRLFHNPIKCLFYRGSRKTREKKLRKSLKKLNFYHPPGDCCQIYRLLENVPGGTYFITENMTNELIMIVKDSVDKKIKSVKLNFYGSYIKIHQHYYINIYMYLMRYTQIYKYPLICFNKYSYCNS")
#infoService.insertTargetProteinInfo("Protein MGF 100-2L","1002L_ASFM2","MGNKESKYLEMCSDEAWLNIPNVFKCIFIRKLFYNKWLKYQEKKLEKRLRLLSFYHAKKDFIGIRDMLQTAPGGSYFITDNITEEFLMLVLKHPEDGSAEFTKLCLKGSCIMIDGYYYDNLDIFLAESPDLYKYPLIRYDR")






print(infoService.seachSequenceByName("5'-AMP-activated protein kinase subunit gamma-3"))
print(infoService.seachSequenceByName("PRKAG3"))