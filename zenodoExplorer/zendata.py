import pandas as pd
import plotly.graph_objects as go

class dat:

    def __init__(self, data_dict, count):
        self.__dict__.update(data_dict)
        if self.tag[:2] == 'ac':
            self.source = None #Atomic Configs have no source
        elif self.tag[:2] == 'td':
            self.source = data_dict['at_conf']
        elif self.tag[:2] == 'ml':
            self.source = data_dict['tr_data']
        elif self.tag[:2] == 'md':
            self.source = data_dict['pes_model']
        self.uid = count

class zdb:
    
    def __init__(self):
        self.AtomicConfigs = []
        self.TrainData = []
        self.MLIPs = []
        self.MDSims = []
        self.count = 0
        self.tag2uid = {}
        self.uid2tag = {}
    
    def update(self, zdb_dict, recID):
        for k in ['AtomicConfigs', 'TrainData', 'MLIPs', 'MDSims']:
            if k in zdb_dict:
                update_tags(zdb_dict[k], recID)
                for data_dict in zdb_dict[k]:
                    self.__dict__[k].append(dat(data_dict, self.count))
                    self.tag2uid.update({data_dict['tag'] : self.count})
                    self.uid2tag.update({self.count : (k, data_dict['tag'])})
                    self.count += 1
    
    def to_pd(self, field):
        tab = []
        for t in self.__dict__[field]:
            tab.append(t.__dict__)
        df = pd.DataFrame(tab)
        if field != 'AtomicConfigs':
            df = df.drop('zip', axis=1)
            df = df.drop('file', axis=1)
        df = df.drop('source', axis=1)
        df = df.drop('uid', axis=1)
        df = df.set_index('tag')
        return df
    
    # def plot(self):
    #     for k in ['AtomicConfigs', 'TrainData', 'MLIPs', 'MDSims']:
    #         for dat in self.__dict__[k]:
    #             print(dat.uid)

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
