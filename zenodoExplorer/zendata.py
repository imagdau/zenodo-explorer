import pandas as pd

class dat:
 
    def __init__(self, data_dict):
        self.__dict__.update(data_dict)

class zdb:
    
    def __init__(self):
        self.AtomicConfigs = []
        self.TrainData = []
        self.MLIPs = []
        self.MDSims = []
    
    def update(self, zdb_dict, recID):
        if 'AtomicConfigs' in zdb_dict:
            update_tags(zdb_dict['AtomicConfigs'], recID)
            self.AtomicConfigs += zdb_dict['AtomicConfigs']
        if 'TrainData' in zdb_dict:
            update_tags(zdb_dict['TrainData'], recID)
            self.TrainData += zdb_dict['TrainData']
        if 'MLIPs' in zdb_dict:
            update_tags(zdb_dict['MLIPs'], recID)
            self.MLIPs += zdb_dict['MLIPs']
        if 'MDSims' in zdb_dict:
            update_tags(zdb_dict['MDSims'], recID)
            self.MDSims += zdb_dict['MDSims']
    
def update_tag(tag, recID):
    if '@' not in tag:
        return tag+'@'+str(recID)
    else:
        return tag

def update_tags(col, recID):
    for c in col:
        for k in ['tag', 'at_conf', 'tr_data', 'pes_model']:
            if k in c:
                c[k] = update_tag(c[k], recID)
