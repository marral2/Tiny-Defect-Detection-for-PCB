# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import math
import os
import random
import shutil
import sys

sys.path.append('../../')

from libs.configs import cfgs


def mkdir(path):
  if not os.path.exists(path):
    os.makedirs(path)


divide_rate = 0.8

#image_path = os.path.join(cfgs.ROOT_PATH, '{}/JPEGImages'.format(cfgs.DATASET_NAME))
image_path = os.path.join(cfgs.ROOT_PATH, '{}/images'.format(cfgs.DATASET_NAME))
print (image_path)
#xml_path = os.path.join(cfgs.ROOT_PATH, '{}/Annotations'.format(cfgs.DATASET_NAME))
xml_path = "/content/PCB_DATASET/Annotations"

##New code HM Jun2024
root = "/content/PCB_DATASET/images"

def get_files_from_subfolders(root_dir):
  """
  Returns a list of all files in all subfolders of a given root directory.

  Args:
    root_dir: The root directory to search.

  Returns:
    A list of file paths.
  """

  file_list = []
  for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
      file_list.append(os.path.join(dirpath, filename))
  return file_list

#image_list = os.listdir(image_path)
image_list = get_files_from_subfolders(root)

image_name = [n.split('.')[0] for n in image_list]

random.shuffle(image_name)

train_image = image_name[:int(math.ceil(len(image_name)) * divide_rate)]
test_image = image_name[int(math.ceil(len(image_name)) * divide_rate):]

image_output_train = os.path.join(
    #cfgs.ROOT_PATH, '{}_train/JPEGImages'.format(cfgs.DATASET_NAME))
    cfgs.ROOT_PATH, '{}_train/images'.format(cfgs.DATASET_NAME))
mkdir(image_output_train)
image_output_test = os.path.join(
    #cfgs.ROOT_PATH, '{}_test/JPEGImages'.format(cfgs.DATASET_NAME))
     cfgs.ROOT_PATH, '{}_test/images'.format(cfgs.DATASET_NAME))
mkdir(image_output_test)

xml_train = os.path.join(cfgs.ROOT_PATH, '{}_train/Annotations'.format(cfgs.DATASET_NAME))
print(xml_train)
mkdir(xml_train)
xml_test = os.path.join(cfgs.ROOT_PATH, '{}_test/Annotations'.format(cfgs.DATASET_NAME))
mkdir(xml_test)


count = 0
for i in train_image:
  shutil.copy(os.path.join(image_path, i + '.jpg'), image_output_train)
  split_sentence = i.split("/")
  i_xml = "/".join(split_sentence[4:])
  if os.path.exists(os.path.join(xml_path, i_xml + '.xml')):
    shutil.copy(os.path.join(xml_path, i_xml + '.xml'), xml_train)
  if count % 1000 == 0:
    print("process step {}".format(count))
  count += 1

for i in test_image:
  shutil.copy(os.path.join(image_path, i + '.jpg'), image_output_test)
  split_sentence = i.split("/")
  i_xml = "/".join(split_sentence[4:])
  #shutil.copy(os.path.join(xml_path, i + '.xml'), xml_test)
  shutil.copy(os.path.join(xml_path, i_xml + '.xml'), xml_test)
  if count % 1000 == 0:
    print("process step {}".format(count))
  count += 1
