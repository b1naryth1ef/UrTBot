import json, os

class ConfigFile(object):
    def __init__(self, name='config', path=['.'], default={}):
        self.configfile = name.replace('.cfg', '')
        path.append(self.configfile+'.cfg')
        self.configpath = os.path.join(*path)
        self.default = default
        self.config = self.load(self.default)

        self.check()
        self.save()

    def load(self, default):
        try:
            with open(self.configpath, 'r') as f:
                return json.loads(''.join(f.readlines()))
        except IOError:
            print 'Creating config file!'
            return default
        except:
            raise Exception('Invalid config file! Please check your JSON formatting!')

    def save(self):
        s = json.dumps(self.config, sort_keys=True, indent=4)
        with open(self.configpath, 'w') as f:
            f.write(s)

    def check(self):
        def checkDict(a, b, rmv=False):
            mark = []
            for key in a:
                if isinstance(key, dict): continue
                if key not in b.keys():
                    if rmv:
                        print 'Removing key %s' % key
                        mark.append(key)
                    else:
                        print 'Adding key %s' % key
                        b[key] = a[key]
                if key in b and isinstance(b[key], dict):
                    checkDict(a[key], b[key], rmv)
            for i in mark:
                del a[i]
        checkDict(self.default, self.config)
        checkDict(self.config, self.default, rmv=True)

    def __getitem__(self, attr):
        return self.config[attr]

    def __getattr__(self, attr):
        if attr in self.config.keys():
            return self.config[attr]
        return self.__dict__[attr]
