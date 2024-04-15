import pandas as pd

class dat:

    def __init__(self, data_dict):
        self.__dict__.update(data_dict)
        self.id = data_dict['tag']
        if self.id[:2] == 'ac':
            self.source = None #Atomic Configs have no source
        elif self.id[:2] == 'td':
            self.source = data_dict['at_conf']
        elif self.id[:2] == 'ml':
            self.source = data_dict['tr_data']
        elif self.id[:2] == 'md':
            self.source = data_dict['pes_model']

class zdb:
    
    def __init__(self):
        self.AtomicConfigs = []
        self.TrainData = []
        self.MLIPs = []
        self.MDSims = []
    
    def update(self, zdb_dict, recID):
        for k in self.__dict__:
            if k in zdb_dict:
                update_tags(zdb_dict[k], recID)
                for data_dict in zdb_dict[k]:
                    self.__dict__[k].append(dat(data_dict))
    
    def to_pd(self, tag):
        tab = []
        for t in self.__dict__[tag]:
            tab.append(t.__dict__)
        df = pd.DataFrame(tab)
        df = df.set_index('tag')
        return df

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
