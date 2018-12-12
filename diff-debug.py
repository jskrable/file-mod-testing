import os
import sys
import json


def read_input():
    with open('sub_modified-uids.json') as f:
        mod = json.load(f)
        print('Reading mod file...')

    with open('sub_old.json', encoding='latin-1') as f:
        old = json.load(f)
        print('Reading old file...')

    with open('sub_new.json', encoding='latin-1') as f:
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
        mod.append(d)

        
    for key in new:
        if new[key] != old[key]:
            if len(mod) == 0:
                new_mod()
            for entry in mod:
                if entry['buid'] == buid:
                    entry['new'].update({key: new[key]}) 
                    entry['old'].update({key: old[key]}) 
                else:
                    new_mod()
    return mod
        

def diff(uids, new, old):
    print('Running diff...')
    mod = []

    for i in uids:
        try:
            new_person = [x['applicant'] for x in new if x['applicant']['univId'] == i][0]
            old_person = [x['applicant'] for x in old if x['applicant']['univId'] == i][0]
            new_app = [x['application'] for x in new if x['applicant']['univId'] == i][0]
            old_app = [x['application'] for x in old if x['applicant']['univId'] == i][0]
            new_couns = [x['counselor'] for x in new if x['applicant']['univId'] == i][0]
            old_couns = [x['counselor'] for x in old if x['applicant']['univId'] == i][0]
        except IndexError:
            mod.append({'buid': i,
                        'error': 'Insert/delete'
                        })
        
        mod = object_diff(new_person,old_person,mod,i)
        mod = object_diff(new_app,old_app,mod,i)
        mod = object_diff(new_couns,old_couns,mod,i)

    return mod
                

def main():

    mod, new, old = read_input()

    uids = [x['buid'] for x in mod]

    new = [x for x in new if x['applicant']['univId'] in uids]
    old = [x for x in old if x['applicant']['univId'] in uids]
    

    changed = diff(uids, new, old)

    print(changed)

if __name__ == '__main__':
    main()
    
    
            
                
    





