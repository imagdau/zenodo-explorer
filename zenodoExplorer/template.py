class AtomicConfigs:

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def plot(self):
        # to be implemented: compositions by cluster size, volumes for periodic
        pass

class TrainData:

    def __init__(self, atomic_configs, ab_initio_level, ab_initio_code, rec, zip, file):
        self.atomic_configs = atomic_configs
        self.ab_initio_level = ab_initio_level
        self.ab_initio_code = ab_initio_code
        self.rec = rec
        self.zip = zip
        self.file = file

    def to_dict(self):
        d = self.__dict__.copy()
        d['atomic_configs'] = self.atomic_configs.name
        return d

    def __repr__(self):
        return self.to_dict().__repr__()


# class MLIP:

#     def __init__(self, zip_parent, path):
#         self.config_desc = Train
#         self.ab_initio_level ab_initio_level
#         self.mlip_code = ab_initio_code
#         self.zip_parent = zip_parent
#         self.path = path
