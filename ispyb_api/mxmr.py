#!/usr/bin/env python
# mxmr.py
#
#    Copyright (C) 2014 Diamond Light Source, Karl Levik
#    
# 2014-09-24 
#
# Methods to store molecular replacement data 
#

try:
  import cx_Oracle
except ImportError, e:
  print 'Oracle API module not found'
  raise e

import string
import logging
import time
import os
import sys
import datetime
from logging.handlers import RotatingFileHandler
from collections import OrderedDict
import copy
from ispyb_api.ExtendedOrderedDict import ExtendedOrderedDict

class MXMR:
  '''MXMR provides methods to store data in the MX molecular replacement tables.'''

  def __init__(self):
    pass

  _run_params = ExtendedOrderedDict([('id',None), ('parentid',None), ('success',None), ('message',None), ('pipeline',None), ('input_coord_file',None), ('output_coord_file',None), ('input_MTZ_file',None), ('output_MTZ_file',None), ('run_dir',None), ('log_file',None), ('cmd_line',None), ('r_start',None), ('r_end',None), ('rfree_start',None), ('rfree_end',None), ('starttime',None), ('endtime',None)])

  def get_run_params(self):
    return copy.deepcopy(self._run_params)

  def insert_run(self, cursor, values):
    '''Store new entry with info about an MX molecular replacement run, e.g. Dimple.'''
    cursor.execute('select ispyb.upsert_mrrun(%s)' % ','.join(['%s'] * len(values)), values)
    rs = cursor.fetchone()
    if len(rs) > 0:
        return int(rs[0])
    return None

  def update_run(self, cursor, values):
    '''Update an existing entry with info about an MX molecular replacement run, e.g. Dimple.'''
    cursor.execute('select ispyb.upsert_mrrun(%s)' % ','.join(['%s'] * len(values)), values)
    rs = cursor.fetchone()
    if len(rs) > 0:
        return int(rs[0])
    return None

  def insert_run_blob(self, cursor, parentid, view1=None, view2=None, view3=None):
    '''Store new entry with info about views (image paths) for an MX molecular replacement run, e.g. Dimple.'''
    values = [None, parentid, view1, view2, view2]
    cursor.execute('select ispyb.upsert_mrrun_blob(%s)' % ','.join(['%s'] * len(values)), values) 
    rs = cursor.fetchone()
    if len(rs) > 0:
        return int(rs[0])
    return None
  
  def update_run_blob(self, cursor, id, parentid=None, view1=None, view2=None, view3=None):
    '''Update existing entry with info about views (image paths) for an MX molecular replacement run, e.g. Dimple.'''
    values = [None, parentid, view1, view2, view2]
    cursor.execute('select ispyb.upsert_mrrun_blob(%s)' % ','.join(['%s'] * len(values)), values)
    rs = cursor.fetchone()
    if len(rs) > 0:
        return int(rs[0])
    return None

mxmr = MXMR()

