'''
Data for CSC6220 
Jan 05, 2019 
Akond Rahman 
'''
import pandas as pd 
import numpy as np 

import _pickle as pickle
import time
import datetime
import os 
import csv 
import sys
from git import Repo
import  subprocess
import time 
import  datetime 
from collections import Counter

def giveTimeStamp():
  tsObj = time.time()
  strToret = datetime.datetime.fromtimestamp(tsObj).strftime('%Y-%m-%d %H:%M:%S')
  return strToret

def getEligibleProjects(fileNameParam):
  repo_list = []
  with open(fileNameParam, 'rU') as f:
    reader = csv.reader(f)
    for row in reader:
      repo_list.append(row[0])
  return repo_list

def getModFilesInDiff(diff_str):
    mod_files  = []
    splitted_lines = diff_str.split('\n')
    for x_ in splitted_lines:
      if '/' in x_  and '.' in x_: 
        if '---' in x_:
          # print(splitted_lines) 
          del_ =  x_.split(' ')[-1].replace('a', '')
          mod_files.append(del_) 
        elif '+++' in x_:
          # print(splitted_lines) 
          add_ =  x_.split(' ')[-1].replace('b', '')
          mod_files.append(add_)
    mod_files = np.unique(mod_files) 
    mod_files = [x_ for x_ in mod_files if ('doc' not in x_) and ('test' not in x_) ]
    # print(mod_files)
    # print(';'*25)
    return mod_files

def getDiff(repo_, hash_):
    mod_files_list = []
   
    cdCommand   = "cd " + repo_ + " ; "
   
    diffCommand = "git diff " + hash_ + "~" + " " + hash_
    command2Run = cdCommand + diffCommand
    try:
      diff_output = subprocess.check_output(["bash", "-c", command2Run])
      diff_output =  diff_output.decode('latin-1') ### exception for utf-8 
      # print(diff_output) 
      mod_files_list =  getModFilesInDiff(diff_output)
    except subprocess.CalledProcessError as e_:
      diff_output = "NOT_FOUND" 
    return diff_output, mod_files_list

def filterFiles(ls_):
  mod_list = [] 
  for elem in ls_:
    z_  = elem.split('.')[-1].lower() 
    # print(z_) 
    if ( ('md' not in z_)   and ('rst' not in z_) and  \
                                  ('html' not in z_) and ('txt' not in z_) and  \
                                  ('json' not in z_) and ('test' not in z_) and  \
                                  ('html' not in z_) and ('image' not in z_) and  \
                                  ('git' not in z_) and  ('dat' not in z_)  and ('travis' not in z_) and  ('inl' not in z_) and \
                                  ('mod' not in z_) and  ('cfg' not in z_)  and ('json' not in z_) and  ('xml' not in z_)   ): 
                                  mod_list.append( elem  ) 
  return mod_list 

def buildContent(df_, HOST_DIR, repo_type):
    content = [] 
    repo_df  = df_[df_['REPO_TYPE']==repo_type]
    all_repo_cnt = len( np.unique(repo_df['REPO'].tolist()) )  
    print('TOTAL REPOS ARE {} FOR {}'.format(  all_repo_cnt, repo_type) ) 
    all_hash = np.unique( repo_df['HASH'].tolist() ) 
    for hash_ in all_hash: 
        hash_df = df_[df_['HASH']==hash_]
        repo_name = hash_df['REPO'].tolist()[0]
        secu_flag = hash_df['SECU_FLAG'].tolist()[0] 
        repo_path = HOST_DIR + repo_name + '/'
        diff_txt, file_list  = getDiff(repo_path, hash_) 
        repo_type = hash_df['REPO_TYPE'].tolist()[0] 
        filtered_files = filterFiles(file_list) 
        # print(repo_path, filtered_files) 
        # print('<>'*25)
        for fil_ in filtered_files: 
          file_path     = HOST_DIR + repo_name + fil_ 
          if(os.path.exists(file_path)):
            map_name      = file_path.replace('/', '_')
            tuple_        = (repo_name, repo_path, repo_type, hash_, file_path, map_name, secu_flag)  
            print(tuple_) 
            content.append( tuple_ )



if __name__=='__main__': 

    t1 = time.time()
    print('Started at:', giveTimeStamp() )
    print('*'*100 )

    CURATED_FILE = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Teaching/Spring2020/CSC6220-TNTECH/CURATED_SECURITY_FULL.csv' 
    HOST_DIR='/Users/arahman/TEACHING_REPOS/NON_JULIA_SCIENTIFIC_SOFTWARE/'

    CURATED_DF   = pd.read_csv(CURATED_FILE) 
    TYPE2ANALYZE = 'ComputationalBiology'
    buildContent(CURATED_DF, HOST_DIR, TYPE2ANALYZE) 

    print('*'*100 )
    print('Ended at:', giveTimeStamp() )
    print('*'*100 )
    t2 = time.time()
    time_diff = round( (t2 - t1 ) / 60, 5) 
    print('Duration: {} minutes'.format(time_diff) )
    print( '*'*100  )
