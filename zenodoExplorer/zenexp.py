import os
import shutil
import requests
import zipfile
from tqdm import tqdm
import yaml
import glob
from .zendata import zdb

class ze:

    def __init__(self, ACCESS_TOKEN, recIDs, base='https://zenodo.org/api/deposit/depositions/', cache='.cache/'):
        self.ACCESS_TOKEN = ACCESS_TOKEN
        self.recIDs = recIDs
        self.cache = os.path.expanduser(cache)
        self.info = dict()
        self.zdb = zdb()
        for recID in self.recIDs:
            self.info[recID] = dict()
            r = requests.get(base+str(recID), params={'access_token': self.ACCESS_TOKEN})
            for db in r.json()['files']:
                if 'filename' in db:
                    fname = db['filename']
                else:
                    fname = 'glob.zip'
                if 'download' in db['links']:
                    link = db['links']['download']
                else:
                    link = db['links']['self']
                self.info[recID].update({fname:(db['checksum'], link)})
            self.info[recID] = dict(sorted(self.info[recID].items()))
    
    def get_chunk(self, recID, fname):
        new_checksum, url = self.info[recID][fname]
        fbase, fext = os.path.splitext(fname)
        os.makedirs(self.cache+str(recID), exist_ok=True)
        temp_dest = self.cache+str(recID)+'/'+fname
        final_dest = self.cache+str(recID)+'/'+fbase        
        if fext == '.yml':
            final_dest = temp_dest
        download = False
        if os.path.exists(final_dest):
            with open(final_dest+'.hash', 'r') as f:
                old_checksum = f.readline().strip()
            if new_checksum != old_checksum:
                download = True
        else:
            download = True
        if download:
            file_response = requests.get(url, params={'access_token': self.ACCESS_TOKEN})
            with open(final_dest+'.hash', 'w') as f:
                f.write(new_checksum+'\n')
            with open(temp_dest, 'wb') as f:
                f.write(file_response.content)
            if fext == '.zip':
                with zipfile.ZipFile(temp_dest, 'r') as zip_ref:
                    shutil.rmtree(final_dest, ignore_errors=True)
                    zip_ref.extractall(final_dest)
                os.remove(temp_dest)
        return final_dest

    def cache_all_data(self):
        for recID in self.info:
            print(recID)
            for fname in tqdm(self.info[recID]):
                self.get_chunk(recID, fname)
                
    def read_zdb(self):
        self.zdb = zdb() #reset zdb object
        for recID in self.info:
            final_dest = self.get_chunk(recID, 'data.yml')
            with open(final_dest, 'r') as file:
                zdb_dict = yaml.safe_load(file)
                self.zdb.update(zdb_dict, recID)

    def read_dat_files(self, tag, ext=None):
        dat = self.zdb.get_dat(tag)
        recID = int(dat.get_recID())
        fname = dat.zip+'.zip'
        final_dest = self.get_chunk(recID, fname)
        pattern = dat.file.split(',')
        flist = []
        for p in pattern:
            for l in glob.glob(final_dest+'/'+p.strip()):
                flist.append(l)
        if ext:
            flist = [l for l in flist if l.split('.')[-1] == ext[1:]]
        return sorted(flist)
