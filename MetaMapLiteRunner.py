#!/bin/python
# wrapper to run metamaplite and clean results.

import csv
import json
import subprocess
import sys
import os
import getopt
from pathlib import Path
import shutil
from  multiprocessing.pool import ThreadPool as Pool
import multiprocessing as mp
from functools import partial

# Note - Metamap dir must be modified to reflect the location where MetaMapLite is installed.
metamap_dir="../../../metamaplite"
metamap_prog=metamap_dir+"/metamaplite.sh"
indexdir=metamap_dir+"/data/ivf/2018ABascii/USAbase"
indexarg= "--indexdir="+indexdir


def processLine(line):
    try:
        fields=line.split('|')
        fname=fields[0]
        cui=fields[4]
        preferred=fields[3]
        triggerinfo=fields[6]
        trigsplit=triggerinfo.split("-")
        concept=trigsplit[0]
        negation=trigsplit[-1]
        if negation=='0':
            presence='present'
        else:
            presence='absent'
        return (fname,cui,preferred,presence) 
    except:
        print("fails on ..."+line)
        
def filterCuis(processed,cuilist):
    filtered=[]
    for p in processed:
        cui = p[1]
        if cui in cuilist:
            filtered.append(p)
    return filtered

def alreadyProcessed(f):
    filename, file_extension = os.path.splitext(f)
    mmifile = filename+".mmi"
    csvfile = filename+".csv"
    return Path.is_file(Path(mmifile)) and Path.is_file(Path(csvfile))

# check files - remove from list if they have both a ".mmi" and a ".csv" file, 
# indicating completed processing. 
def filterCompleted(files):
    filteredFiles=[]
    for f in files:
        if alreadyProcessed(f) == False:
            print("adding .."+f+" to eligible file")
            filteredFiles.append(f)
    return filteredFiles


# merge lines -  if line n+1 does not start with the file name, merge it together with previous line.
def cleanLines(lines):
    lines2=[]
    filename=lines[0].split("|")[0] # get file name out of the first lien

    lastline=lines[0]
    for i in range(1,len(lines)):
        line = lines[i]
        if not line.startswith(filename):
            lastline=lastline+line
        else:
            lines2.append(lastline)
            lastline=line
    return lines2


# fname passed in is the base name.
def processMMLOutput(fname,cuis=None):

    mminame =fname+".mmi"
    with open(mminame) as f:
        lines = [line.rstrip() for line in f]

    lines2=cleanLines(lines)
        
    processed=[processLine(l) for l in lines2]
    
    filtered = processed
    if cuis is not None:
        filtered = filterCuis(processed,cuis)
    
    outname=fname+".csv"
    # write to filtered
    with open(outname,'w') as out:
        csv_out=csv.writer(out,delimiter="|")
        for row in processed:
            csv_out.writerow(row)


## process each file
def processFile(logfile,fname):
    try: 
        # metamap will process a file of form name.ext, and will spit out name.mmi
        filename, file_extension = os.path.splitext(fname)

        errout = None
        if logfile is not None:
            errout=logfile
        myf = Path(fname)
        if myf.is_file():
            #res = subprocess.call([metamap_prog,indexarg,fname])
            res = subprocess.call([metamap_prog,indexarg,fname],stderr=logfile)
            if res == 0:
                processMMLOutput(filename)
        elif logfile is not None:
            logfile.write("File not found: "+fname)
        return 0
    except subprocess.CalledProcessError as e:
        if logfile is not None:
            logfile.write("Other failure: "+fname+"\n"+e.output)
        return -1

# main - get filenames and run...
# will work with wildcards
def main():

    argv=sys.argv[1:]
    opts,args = getopt.getopt(argv,'sl:')
    logfile= None


    # verify file.
    if shutil.which(metamap_prog) is None:
        print("Path error - cannot find metamap. Please adjust 'metamap_dir' variable")
        sys.exit(0)

    singleThread=False
    for name,value in opts:
        if name=='-l':
            logfilename=value
            logfile = open(logfilename,'w')
        elif name=='-s':
            singleThread=True

    func=partial(processFile,logfile)

    # filter files 
    files = filterCompleted(args)
    for f in files:
        print(f)

    if singleThread==True:
        for file in files:
            func(file)
    else:
        pool=Pool(mp.cpu_count()-1)
        pool.map(func,files)
        pool.close()

    if logfile:
            logfile.close()

if __name__ == "__main__":
    main()
