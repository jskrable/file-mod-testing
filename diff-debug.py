import os
import sys
import json


def read_input():
    # Define input files here
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
    

def output(mod):
    
    # Update modifed JSON file
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
    
    # Update mod dict

    def new_mod():
        # Insert new key
        d = {'buid': buid,
                'new': {
                    key: new[key]
                    },
                'old': {
                    key: old[key]
                    }
                }
        mod.update(d)

    # Loop through object
    for key in new:
        if new[key] != old[key]:
            # Update mod dict if different
            if not mod:
                new_mod()
            else:
                try: 
                    mod['new'].update({key: new[key]})
                    mod['old'].update({key: old[key]})
                except KeyError:
                    new_mod()

    return mod
        

def diff(uids, new, old):

    # Run diff
    print('Running diff...')

    # Get list of objects in data
    objects = [*new[0]]

    # Loop through all uids
    for i in uids:
        # Init mod dict for uid
        mod = {}
        for obj in objects:
            # For each obj in data, get old and new
            try:
                new_entry = [x[obj] for x in new if x['applicant']['univId'] == i][0]
                old_entry = [x[obj] for x in old if x['applicant']['univId'] == i][0]
                print('Diffing %s for %s' % (obj, i))
                # Update mod with differences
                mod = object_diff(new_entry,old_entry,mod,i)
            # Catch inserts/deletes
            except IndexError:
                mod.update({'buid': i,
                         'error': 'Insert/delete'
                          })
            # Catch missing objects
            except(TypeError, KeyError) as e:
                print('Cannot diff %s for %s' % (obj, i))
                print(e)
                pass
        # Append results file
        output(mod)
        mod = {}

    return mod
                

def main():

    # Read input files
    mod, new, old = read_input()

    # Get list of uids
    uids = [x['buid'] for x in mod]
    
    # Consider only modified uids
    # Drop this to consider Inserts/Deletes
    new = [x for x in new if x['applicant']['univId'] in uids]
    old = [x for x in old if x['applicant']['univId'] in uids]
    

    diff(uids, new, old)

if __name__ == '__main__':
    main()
    
    
            
                
    





