import os
import requests
import zipfile
from tqdm import tqdm
import yaml
import glob
from hashlib import md5
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
    
    def get_chunk(self, recID, fname, compare_hash):
        url = self.urls[recID][fname]
        fbase, fext = os.path.splitext(fname)
        os.makedirs('.cache/'+str(recID), exist_ok=True)
        temp_dest = '.cache/'+str(recID)+'/'+fname
        final_dest = '.cache/'+str(recID)+'/'+fbase        
        if fext == '.yml':
            final_dest = temp_dest
        if not os.path.exists(final_dest) or compare_hash:
            rewrite = True
            file_response = requests.get(url, params={'access_token': self.ACCESS_TOKEN})
            new_hash = md5(file_response.content).hexdigest()
            if os.path.exists(final_dest+'.hash'):
                with open(final_dest+'.hash', 'r') as f:
                    old_hash = f.readline().strip()
                    if new_hash == old_hash:
                        rewrite = False
            if rewrite:
                with open(final_dest+'.hash', 'w') as f:
                    f.write(new_hash+'\n')
                with open(temp_dest, 'wb') as f:
                    f.write(file_response.content)
                if fext == '.zip':
                    with zipfile.ZipFile(temp_dest, 'r') as zip_ref:
                        zip_ref.extractall(final_dest)
                        os.remove(temp_dest)
        return final_dest

    def cache_all_data(self, compare_hash=False):
        for recID in self.urls:
            print(recID)
            for url_key in tqdm(self.urls[recID]):
                self.get_chunk(recID, url_key, compare_hash)
                
    def read_zdb(self, compare_hash=True):
        for recID in self.urls:
            final_dest = self.get_chunk(recID, 'data.yml', compare_hash)
            with open(final_dest, 'r') as file:
                zdb_dict = yaml.safe_load(file)
                self.zdb.update(zdb_dict, recID)

    def read_dat_files(self, tag, compare_hash=False):
        dat = self.zdb.get_dat(tag)
        recID = int(dat.get_recID())
        fname = dat.zip+'.zip'
        final_dest = self.get_chunk(recID, fname, compare_hash)
        pattern = dat.file.split(',')
        flist = []
        for p in pattern:
            for l in glob.glob(final_dest+'/'+p.strip()):
                flist.append(l)
        return flist
