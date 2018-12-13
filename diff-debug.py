import os
import sys
import json


def read_input():
    with open('modified-uids.json') as f:
        mod = json.load(f)
        print('Reading mod file...')

    with open('old.json', encoding='latin-1') as f:
        old = json.load(f)
        print('Reading old file...')

    with open('new.json', encoding='latin-1') as f:
        new = json.load(f)
        print('Reading new file...')

    return mod, new, old
    

def sample_set(data, size):
    subset = []
    for i, entry in enumerate(data):
        if i > size:
            break
        subset.append(entry)
    return subset

def output(mod):

    if not mod:
        return None
    else:
        with open('applicant_mod_results.json', 'a+') as f:
            if f.tell() == 0:
                a = []
                a.append(mod)
                json.dump(a, f, indent=2)
            else:
                f.seek(f.tell() - 1, os.SEEK_SET)
                f.truncate()
                f.write(',')
                json.dump(mod, f, indent=2)
                f.write(']')
        

def object_diff(new, old, mod, buid):

    def new_mod():
        d = {'buid': buid,
                'new': {
                    key: new[key]
                    },
                'old': {
                    key: old[key]
                    }
                }
        mod.update(d)
    

    try:
        for key in new:
            if new[key] != old[key]:
                if not mod:
                    new_mod()
                else:
                    try: 
                        mod['new'].update({key: new[key]})
                        mod['old'].update({key: old[key]})
                    except KeyError:
                        new_mod()
    except TypeError:
        None
    return mod
        

def diff(uids, new, old):
    print('Running diff...')

    objects = [*new[0]]

    for i in uids:
        mod = {}
        for obj in objects:
            try:
                new_entry = [x[obj] for x in new if x['applicant']['univId'] == i][0]
                old_entry = [x[obj] for x in old if x['applicant']['univId'] == i][0]
                print('Diffing %s for %s' % (obj, i))
                mod = object_diff(new_entry,old_entry,mod,i)
            except (IndexError, TypeError, KeyError) as e:
                # mod.update({'buid': i,
                #         'error': 'Insert/delete'
                #          })
                print('Cannot diff %s for %s' % (obj, i))
                print(e)
                pass
        output(mod)
        mod = {}

    return mod
                

def main():

    mod, new, old = read_input()

    uids = [x['buid'] for x in mod]

    new = [x for x in new if x['applicant']['univId'] in uids]
    old = [x for x in old if x['applicant']['univId'] in uids]
    

    diff(uids, new, old)

if __name__ == '__main__':
    main()
    
    
            
                
    





