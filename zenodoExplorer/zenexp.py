import os
import requests
import zipfile
from tqdm import tqdm
import yaml
import glob
from .zendata import zdb

class ze:

    def __init__(self, ACCESS_TOKEN, recIDs):
        self.ACCESS_TOKEN = ACCESS_TOKEN
        self.recIDs = recIDs
        self.urls = dict()
        self.zdb = zdb()
        for recID in self.recIDs:
            self.urls[recID] = dict()
            r = requests.get('https://zenodo.org/api/deposit/depositions/'+str(recID), params={'access_token': self.ACCESS_TOKEN})
            self.urls[recID].update({db['filename']:db['links']['download'] for db in r.json()['files']})
            self.urls[recID] = dict(sorted(self.urls[recID].items()))
    
    def get_chunk(self, recID, fname):
        url = self.urls[recID][fname]
        fbase, fext = os.path.splitext(fname)
        os.makedirs('.cache/'+str(recID), exist_ok=True)
        temp_dest = '.cache/'+str(recID)+'/'+fname
        final_dest = '.cache/'+str(recID)+'/'+fbase        
        if fext == '.yml':
            final_dest = temp_dest
        if not os.path.exists(final_dest):
            file_response = requests.get(url, params={'access_token': self.ACCESS_TOKEN})
            with open(temp_dest, 'wb') as f:
                f.write(file_response.content)
            if fext == '.zip':
                with zipfile.ZipFile(temp_dest, 'r') as zip_ref:
                    zip_ref.extractall(final_dest)
                    os.remove(temp_dest)
        return final_dest

    def cache_all_data(self):
        for recID in self.urls:
            print(recID)
            for url_key in tqdm(self.urls[recID]):
                self.get_chunk(recID, url_key)
                
    def read_zdb(self):
        for recID in self.urls:
            final_dest = self.get_chunk(recID, 'data.yml')
            with open(final_dest, 'r') as file:
                zdb_dict = yaml.safe_load(file)
                self.zdb.update(zdb_dict, recID)

    def read_dat_files(self, tag):
        dat = self.zdb.get_dat(tag)
        recID = int(dat.get_recID())
        fname = dat.zip+'.zip'
        final_dest = self.get_chunk(recID, fname)
        pattern = dat.file.split(',')
        flist = []
        for p in pattern:
            for l in glob.glob(final_dest+'/'+p.strip()):
                flist.append(l)
        return flist
