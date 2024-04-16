import pandas as pd
import plotly.graph_objects as go

class dat:

    def __init__(self, data_dict):
        self.__dict__.update(data_dict)
        if self.tag[:2] == 'ac':
            self.source = None #Atomic Configs have no source
        elif self.tag[:2] == 'td':
            self.source = data_dict['at_conf']
        elif self.tag[:2] == 'ml':
            self.source = data_dict['tr_data']
        elif self.tag[:2] == 'md':
            self.source = data_dict['pes_model']

class zdb:
    
    def __init__(self):
        self.AtomicConfigs = []
        self.TrainData = []
        self.MLIPs = []
        self.MDSims = []
    
    def update(self, zdb_dict, recID):
        for k in ['AtomicConfigs', 'TrainData', 'MLIPs', 'MDSims']:
            if k in zdb_dict:
                update_tags(zdb_dict[k], recID)
                for data_dict in zdb_dict[k]:
                    self.__dict__[k].append(dat(data_dict))

    def to_pd(self, field):
        tab = []
        for t in self.__dict__[field]:
            tab.append(t.__dict__)
        df = pd.DataFrame(tab)
        if field != 'AtomicConfigs':
            df = df.drop('zip', axis=1)
            df = df.drop('file', axis=1)
        df = df.drop('source', axis=1)
        df = df.set_index('tag')
        return df
    
    def plot(self):
        tag2uid = dict()
        uid2tag = dict()
        node = dict(
            pad = 15,
            thickness = 15,
            line = dict(color = "black", width = 0.5),
            label =  [],
            x = [],
            y = [],
            # color =  []
        )
        link = dict(
            source = [],
            target = [],
            value = [],
            label = [],
            # color = []
        )
        
        def node_update(dat, count, x, y):
            node['label'].append(dat.tag)
            node['x'].append(x)
            node['y'].append(y)
            uid2tag[count] = dat.tag
            tag2uid[dat.tag] = count
            count += 1
            return count
        
        def link_update(dat, count):
            link['source'].append(tag2uid[dat.source])
            link['target'].append(count)
            link['value'].append(1)
        
        count = 0
        dx = 0.8/4
        dy = 0.8/len(self.AtomicConfigs)

        for i, dat in enumerate(self.AtomicConfigs):
            count = node_update(dat, count, 0.1+dx*0, 0.1+dy*i)
        
        dy = 0.8/len(self.TrainData)
        for i, dat in enumerate(self.TrainData):
            link_update(dat, count)
            count = node_update(dat, count, 0.1+dx*1, 0.1+dy*i)
        
        dy = 0.8/len(self.MLIPs)
        for i, dat in enumerate(self.MLIPs):
            link_update(dat, count)
            count = node_update(dat, count, 0.1+dx*2, 0.1+dy*i)
        
        dy = 0.8/len(self.MDSims)
        for i, dat in enumerate(self.MDSims):
            link_update(dat, count)
            count = node_update(dat, count, 0.1+dx*3, 0.1+dy*i)

        fig = go.Figure(go.Sankey(node=node, link=link, arrangement='snap'))
        return fig

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
