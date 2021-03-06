#!/usr/bin/env python
# mxacquisition.py
#
#    Copyright (C) 2014 Diamond Light Source, Karl Levik
#    
# 2014-09-24 
#
# Methods to store MX acquisition data 
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
from ispyb_api.ExtendedOrderedDict import ExtendedOrderedDict
import copy

class MXAcquisition:
  '''MXAcquisition provides methods to store data in the MX acquisition tables.'''

  def __init__(self):
    pass

  _data_collection_group_params =\
    ExtendedOrderedDict([('id',None), ('parentid',None), ('sampleid',None), ('experimenttype',None), ('starttime',None), ('endtime',None), 
                         ('crystal_class',None), ('detector_mode',None), ('actual_sample_barcode',None), ('actual_sample_slot_in_container',None),
                         ('actual_container_barcode',None), ('actual_container_slot_in_sc',None), ('comments',None)])

  _data_collection_params =\
    ExtendedOrderedDict([('id',None), ('parentid',None), ('visitid',None), ('sampleid',None), ('detectorid',None), ('positionid',None), 
                         ('apertureid',None), ('datacollection_number',None), ('starttime',None), ('endtime',None), ('run_status',None), 
                         ('axis_start',None), ('axis_end',None), ('axis_range',None), ('overlap',None), ('n_images',None), 
                         ('start_image_number',None), ('n_passes',None), ('exp_time',None), 
                         ('imgdir',None), ('imgprefix',None), ('imgsuffix',None), ('file_template',None), 
                         ('wavelength',None), ('resolution',None), ('detector_distance',None), ('xbeam',None), ('ybeam',None), 
                         ('comments',None), ('slitgap_vertical',None), ('slitgap_horizontal',None), ('transmission',None), 
                         ('synchrotron_mode',None), ('xtal_snapshot1',None), ('xtal_snapshot2',None), ('xtal_snapshot3',None), 
                         ('xtal_snapshot4',None), ('rotation_axis',None), ('phistart',None), ('kappastart',None), ('omegastart',None), 
                         ('resolution_at_corner',None), ('detector2theta',None), ('undulator_gap1',None), ('undulator_gap2',None), 
                         ('undulator_gap3',None), ('beamsize_at_samplex',None), ('beamsize_at_sampley',None), ('avg_temperature',None), 
                         ('actual_centering_position',None), ('beam_shape',None), ('focal_spot_size_at_samplex',None), 
                         ('focal_spot_size_at_sampley',None), ('polarisation',None), ('flux',None), 
                         ('processed_data_file',None), ('dat_file',None), ('magnification',None), ('total_absorbed_dose',None), 
                         ('binning',None), ('particle_diameter',None), ('box_size_ctf',None), ('min_resolution',None), 
                         ('min_defocus',None), ('max_defocus',None), ('defocus_step_size',None), ('amount_astigmatism',None), 
                         ('extract_size',None), ('bg_radius',None), ('voltage',None), ('obj_aperture',None), ('c1aperture',None), 
                         ('c2aperture',None), ('c3aperture',None), ('c1lens',None), ('c2lens',None), ('c3lens',None)])

  _image_params =\
    ExtendedOrderedDict([('id',None), ('parentid',None), ('img_number',None), ('filename',None), ('file_location',None), 
                         ('measured_intensity',None), ('jpeg_path',None), ('jpeg_thumb_path',None), ('temperature',None), 
                         ('cumulative_intensity',None), ('synchrotron_current',None), ('comments',None), ('machine_msg',None)])

  def get_data_collection_group_params(self):
    return copy.deepcopy(self._data_collection_group_params)

  def get_data_collection_params(self):
    return copy.deepcopy(self._data_collection_params)

  def get_image_params(self):
    return copy.deepcopy(self._image_params)

  def insert_data_collection_group(self, cursor, values):
    '''Store new MX data collection group.'''
    cursor.execute('select ispyb.upsert_dcgroup(%s)' % ','.join(['%s'] * len(values)), values)
    rs = cursor.fetchone()
    if len(rs) > 0:
        return int(rs[0])
    return None

  def update_data_collection_group(self, cursor, values):
    '''Update existing data collection group.'''
    if values[0] is not None:
        cursor.execute('select ispyb.upsert_dcgroup(%s)' % ','.join(['%s'] * len(values)), values)

  def put_data_collection_group(self, cursor, values):
    cursor.execute('select ispyb.upsert_dcgroup(%s)' % ','.join(['%s'] * len(values)), values)
    rs = cursor.fetchone()
    if len(rs) > 0:
        return int(rs[0])
    return None

  def insert_data_collection(self, cursor, values):
    '''Store new data collection.'''
    cursor.execute('select ispyb.upsert_dc(%s)' % ','.join(['%s'] * len(values)), values)
    rs = cursor.fetchone()
    if len(rs) > 0:
        return int(rs[0])
    return None

  def update_data_collection(self, cursor, values):
    '''Update existing data collection.'''
    cursor.execute('select ispyb.upsert_dc(%s)' % ','.join(['%s'] * len(values)), values)
    rs = cursor.fetchone()
    if len(rs) > 0:
        return int(rs[0])
    return None

  def insert_image(self, cursor, values):
    '''Store new MX diffraction image.'''
    cursor.execute('select ispyb.upsert_image(%s)' % ','.join(['%s'] * len(values)), values)
    rs = cursor.fetchone()
    if len(rs) > 0:
        return int(rs[0])
    return None

  def update_image(self, cursor, values):
    '''Update existing diffraction image.'''
    cursor.execute('select ispyb.upsert_image(%s)' % ','.join(['%s'] * len(values)), values)
    rs = cursor.fetchone()
    if len(rs) > 0:
        return int(rs[0])
    return None

mxacquisition = MXAcquisition()

