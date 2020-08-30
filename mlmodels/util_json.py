"""

Alll related to json dynamic parsing


"""# -*- coding: utf-8 -*-
import os
import re
import fnmatch

# import toml
from pathlib import Path
from jsoncomment import JsonComment ; json = JsonComment()

import importlib
from inspect import getmembers

from mlmodels.util import *
from mlmodels.util import path_norm


####################################################################################################
class to_namespace(object):
    def __init__(self, adict):
        self.__dict__.update(adict)

    def get(self, key):
        return self.__dict__.get(key)


def log(*s, n=0, m=0):
    sspace = "#" * n
    sjump = "\n" * m
    print("")
    print(sjump, sspace, *s, sspace, flush=True)


####################################################################################################
def os_package_root_path(filepath="", sublevel=0, path_add=""):
    """
       get the module package root folder
    """
    from pathlib import Path
    import mlmodels, os, inspect 

    path = Path(inspect.getfile(mlmodels)).parent
    # print( path )

    # path = Path(os.path.realpath(filepath)).parent
    for i in range(1, sublevel + 1):
        path = path.parent

    path = os.path.join(path.absolute(), path_add)
    return path


###################################################################################################
def params_json_load(path, config_mode="test", 
                     tlist= [ "model_pars", "data_pars", "compute_pars", "out_pars"] ):
    from jsoncomment import JsonComment ; json = JsonComment()
    pars = json.load(open(path, mode="r"))
    pars = pars[config_mode]

    ### HyperParam, model_pars, data_pars,
    list_pars = []
    for t in tlist :
        pdict = pars.get(t)
        if pdict:
            list_pars.append(pdict)
        else:
            log("error in json, cannot load ", t)

    return tuple(list_pars)

#########################################################################################
#########################################################################################
def load_function(package="mlmodels.util", name="path_norm"):
  import importlib
  return  getattr(importlib.import_module(package), name)



def load_function_uri(uri_name="path_norm"):
    """
    #load dynamically function from URI

    ###### Pandas CSV case : Custom MLMODELS One
    #"dataset"        : "mlmodels.preprocess.generic:pandasDataset"

    ###### External File processor :
    #"dataset"        : "MyFolder/preprocess/myfile.py:pandasDataset"


    """
    
    import importlib, sys
    from pathlib import Path
    pkg = uri_name.split(":")

    assert len(pkg) > 1, "  Missing :   in  uri_name module_name:function_or_class "
    package, name = pkg[0], pkg[1]
    
    try:
        #### Import from package mlmodels sub-folder
        return  getattr(importlib.import_module(package), name)

    except Exception as e1:
        try:
            ### Add Folder to Path and Load absoluate path module
            path_parent = str(Path(package).parent.parent.absolute())
            sys.path.append(path_parent)
            #log(path_parent)

            #### import Absolute Path model_tf.1_lstm
            model_name   = Path(package).stem  # remove .py
            package_name = str(Path(package).parts[-2]) + "." + str(model_name)
            #log(package_name, model_name)
            return  getattr(importlib.import_module(package_name), name)

        except Exception as e2:
            raise NameError(f"Module {pkg} notfound, {e1}, {e2}")


def load_callable_from_uri(uri):
    assert(len(uri)>0 and ('::' in uri or '.' in uri))
    if '::' in uri:
        module_path, callable_name = uri.split('::')
    else:
        module_path, callable_name = uri.rsplit('.',1)
    if os.path.isfile(module_path):
        module_name = '.'.join(module_path.split('.')[:-1])
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    else:
        module = importlib.import_module(module_path)
    return dict(getmembers(module))[callable_name]
        

def load_callable_from_dict(function_dict, return_other_keys=False):
    function_dict = function_dict.copy()
    uri = function_dict.pop('uri')
    func = load_callable_from_uri(uri)
    try:
        assert(callable(func))
    except:
        raise TypeError(f'{func} is not callable')
    arg = function_dict.pop('arg', {})
    if not return_other_keys:
        return func, arg
    else:
        return func, arg, function_dict
    



def test_functions_json(arg=None):
  from mlmodels.util import load_function_uri

  path = path_norm("dataset/test_json/test_functions.json")
  dd   = json.load(open( path ))['test']
  
  for p in dd  :
     try :
         log("\n\n","#"*20, p)

         myfun = load_function_uri( p['uri'])
         log(myfun)

         w  = p.get('args', []) 
         kw = p.get('kw_args', {} )
         
         if len(kw) == 0 and len(w) == 0   : log( myfun())

         elif  len(kw) > 0 and len(w) > 0  : log( myfun( *w,  ** kw ))

         elif  len(kw) > 0 and len(w) == 0 : log( myfun( ** kw ))

         elif  len(kw) == 0 and len(w) > 0 : log( myfun( *w ))
                     
            
     except Exception as e:
        log(e, p )    

import json
import os
import pandas as pd
import time

'''
    For the given path, get the List of all files in the directory tree
    Here the Path is where the json directory exist "mlmodels/mlmodels/dataset"
    Please change path by using os.chdir(***json directory Path***)
    
'''
def getListOfJsonsPaths(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfJsonsPaths(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles



'''
    This function takes as a parameter list of json paths => result of getListOfFiles()
    Detects unreadable json files and,
    Returns a list of Python dictionaries of the jsons, containing two keys
    'Path' key, containing path to the json and 'json' key containing the dictionary

'''
def Jsons_ToDictionaries(json_Paths):
    data=[]
    problem=0
    for i in range(len(json_Paths)):
        try:
            with open(json_Paths[i]) as json_file:
                d=dict()
                d['Path']=json_Paths[i]
                d['Json']=json.load(json_file)
                data.append(d)
        except:
            if(problem==0):
                print("Files That have a structure problem:\n")
            problem+=1
            print('\t',json_Paths[i])
            continue
    print("Total flawed jsons:\t",problem)
    return data



'''
    This function takes as a parameter the result of JsonsToDictionaries,
    which is a list of dictionaries with 'Path' and 'Json' keys
    Returns the list of dictionaries 
    
'''
def IndexedDicts_ToDicts(indexed_Dicts):
    Dicts=[]
    for i in range(len(indexed_Dicts)):
        Dicts.append(indexed_Dicts[i]['Json'])
    return Dicts



'''
    This function takes as a parameter the result of JsonsToDictionaries,
    which is a list of dictionaries with 'Path' and 'Json' keys
    Returns a dataframe of the jsons with a 'Path' column that contains json paths
'''
def IndexedDicts_ToDF(indexed_Dicts):
    all_jsons = IndexedDicts_ToDicts(indexed_Dicts)
    paths=[]
    filenames=[]
    for i in range(len(indexed_Dicts)):
        paths.append(indexed_Dicts[i]['Path'])
    for i in range(len(indexed_Dicts)):
        filename=indexed_Dicts[i]['Path'].split('\\')[-1].split('.json')[0]
        filenames.append(filename)
    
    df = pd.json_normalize(all_jsons)
    df1 = pd.DataFrame({'file_path':paths,'json_name':filenames})
    result = pd.concat([df1, df], axis=1)
    print("Dataframe created successfully")
    return result

'''Get json skeleton from csv'''

def JsSkeleton_Fromcsv(csv):
    df=pd.read_csv(csv)
    d=dict()
    fullname=list(df.columns)[3:]
    for j in range(len(fullname)):
        l=fullname[j].split('.')
        d=Update_Dict(l,d,None)
    return d

''' Update dictionary, fields_list is result of .split('.')'''
def Update_Dict(Fields_list,Dict,value):
    if(len(Fields_list)>1):
        l1=Fields_list[1:]
        k=Fields_list[0]
        if(k not in list(Dict.keys())):
            Dict[k]=dict()
        Dict[k]=Update_Dict(l1,Dict[k],value)
    else:
        k=Fields_list[0]
        Dict[k]=value
        return Dict
    return Dict

'''transform csv to list of dicts and create new normalized jsons'''
def csv_toJsons(csv):
    dicts=[]
    df=pd.read_csv(csv)
    fullname=list(df.columns)[3:]
    filename=list(df['json_name'])
    for i in range(len(filename)):
        dd=JsSkeleton_Fromcsv(csv)
        for j in  range(len(fullname)):
            value=df.iloc[i][fullname[j]]
            fields=fullname[j].split('.')
            dd.update(Update_Dict(fields,dd,value).copy())
        dicts.append(dd)
    paths=list(df['file_path'])
    paths_tocreate=[]
    for i in range(len(paths)):
        lp=paths[i].split('\\')
        dire=""
        if(len(lp)>2):
            for j in  range(1,len(lp)-1):
                dire=dire+'\\'+lp[j]
        paths_tocreate.append(dire)
    paths_tocreate1=list(set(paths_tocreate))
    paths_tocreate1.sort()
    print("Now creating normalized jsons directory")
    for p in paths_tocreate1:
        try:
            os.mkdir('normalized_jsons'+p)
        except OSError:
            print ("Creation of the directory %s failed\t",p)
    
    for i in range(len(filename)):
        with open('normalized_jsons\\'+paths_tocreate[i]+'\\'+filename[i]+'.json', 'w') as fp:
            json.dump(dicts[i], fp, indent = 4)
    print("New normalized jsons created")
    return dicts

#######functions testing part#######
JsonsPaths=getListOfJsonsPaths('json')
Indexed_Dictionaries=Jsons_ToDictionaries(JsonsPaths)
Dictionaries=IndexedDicts_ToDicts(Indexed_Dictionaries)
Df=IndexedDicts_ToDF(Indexed_Dictionaries)
Df.to_csv('data.csv')
print('csv created successfully')
time.sleep(1)
New_dicts=csv_toJsons('data.csv')
