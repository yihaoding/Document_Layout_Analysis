# -*- coding: utf-8 -*-
"""scene_graph_generator.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1h4CTz5R9s7Zj6LRTBYU_jGY9OiixzV7N
"""

import json
import os 
from PIL import Image, ImageDraw, ImageFont

def reletive_position(box1,box2):
  x1,y1 = box1[:2]
  x2,y2 = box2[:2]
  if abs(x1-x2) > abs(y1-y2):
    if x1 > x2:
      return 'right'
    else:
      return 'left'
  else:
    if y1 > y2:
      return 'down'
    else:
      return 'above'

def publaynet_scene_graph_generator(train_json_path,image_path):
  with open(train_json_path) as f:
    train_json = json.load(f)
  img_list = os.listdir(image_path)
  scene_graph = {}
  relation_id = 0
  for i in range(len(img_list):
    img_name = img_list[i]
    print(img_name)
    scene_graph[img_name] = {}
    for j in range(len(train_json['images'])):
      image_info = train_json['images'][j]
      if img_name == image_info['file_name']:
        scene_graph[img_name]['image_id'] = image_info['id']
        scene_graph[img_name]['width'] = image_info['width']
        scene_graph[img_name]['height'] = image_info['height']
    scene_graph[img_name]['objects'] = {}
    for j in range(len(train_json['annotations'])):
      box_info = train_json['annotations'][j]
      if scene_graph[img_name]['image_id'] == box_info['image_id']:
        scene_graph[img_name]['objects'][box_info['id']] = {}
        if int(box_info['category_id']) == 1:
          label = 'text'
        elif int(box_info['category_id'])  == 2:
          label = 'title'
        elif int(box_info['category_id'])  == 3:
          label = 'list'
        elif int(box_info['category_id']) == 4:
          label = 'table'
        elif int(box_info['category_id']) == 5:
          label = 'figure'
        scene_graph[img_name]['objects'][box_info['id']]['name'] = box_info['category_id']
        scene_graph[img_name]['objects'][box_info['id']]['box'] = box_info['bbox']
        scene_graph[img_name]['objects'][box_info['id']]['relations'] = {}
    for box1 in scene_graph[img_name]['objects']:
      for box2 in scene_graph[img_name]['objects']:
        if box1 != box2:
          scene_graph[img_name]['objects'][box1]['relations'][str(relation_id)] = {} 
          bbox1 = scene_graph[img_name]['objects'][box1]['box']
          bbox2 = scene_graph[img_name]['objects'][box2]['box']
          scene_graph[img_name]['objects'][box1]['relations'][str(relation_id)]['name'] = reletive_position(bbox1,bbox2)
          scene_graph[img_name]['objects'][box1]['relations'][str(relation_id)]['object'] = box2
          relation_id += 1
  return scene_graph

def funsd_scene_graph_generator(input_path, type):

  # There are two types scene graphs one is position based global scene graph
  # Another one is document components structural relationship based binary scene graph
  # Type 0 means global relationship which will return reletively globally positional relationship 
  # Type 1 will return binary structure or logical relationship between components

  json_path = input_path+'/annotations/'
  img_path = input_path+'/images'
  img_list = os.listdir(img_path)
  bbox_id = 0
  relation_id = 0
  bi_relation = 0
  scene_graph = {}
  for index in range(len(img_list)):
    print(index)
    name = img_list[index][:-4]
    image = Image.open(img_path+'/'+name+'.png')
    info_path = json_path+name+'.json'
    with open(info_path) as f:
      info_list = json.load(f)
    info_list = info_list['form']
    scene_graph[name] = {}
    scene_graph[name]['file_name'] = name
    scene_graph[name]['width'] = image.size[0]
    scene_graph[name]['height'] = image.size[1]
    scene_graph[name]['objects'] = {}
    for i in range(len(info_list)):
      scene_graph[name]['objects'][str(i)] = {}
      scene_graph[name]['objects'][str(i)]['id'] = bbox_id
      bbox_id += 1
      scene_graph[name]['objects'][str(i)]['box'] = info_list[i]['box']
      scene_graph[name]['objects'][str(i)]['category'] = info_list[i]['label']
      scene_graph[name]['objects'][str(i)]['text'] = info_list[i]['text']
      scene_graph[name]['objects'][str(i)]['relations'] = {}

    # returning scene graph is position based global scene graph
    if type == 1:
      for i in scene_graph[name]['objects']:
        current_box = scene_graph[name]['objects'][i]
        box1 = current_box['box']
        c_relation = 0
        for j in scene_graph[name]['objects']:
          if i != j:
            box2 = scene_graph[name]['objects'][j]['box']
            current_box['relations'][str(c_relation)] = {}
            current_box['relations'][str(c_relation)]['id'] = relation_id
            current_box['relations'][str(c_relation)]['object'] = scene_graph[name]['objects'][j]['id']
            current_box['relations'][str(c_relation)]['name'] = reletive_position(box1,box2)
            relation_id += 1
            c_relation += 1


    # type 0 will return binary relationships between bounding box
    # for funsd dataset, it will represent the question and corresponding answer relationships
    # if current node is a question, the relation will be annotated as 'answer' to its answer
    # if current node is a answer, the relation will be annotated as 'question' 
    elif type == 0:
      for i in scene_graph[name]['objects']:
        current_box = scene_graph[name]['objects'][i]
        k = int(i)
        if len(info_list[k]['linking']) != 0:
          for n in range(len(info_list[k]['linking'])):
            linking_node = info_list[k]['linking'][n]
            current_box['relations'][str(n)] = {}
            node1 = linking_node[0]
            node2 = linking_node[1]
            if node1 == k:
              current_box['relations'][str(n)]['name'] = info_list[node2]['label']
              current_box['relations'][str(n)]['id'] = bi_relation
              current_box['relations'][str(n)]['object'] = scene_graph[name]['objects'][str(node2)]['id']
              bi_relation += 1
            elif node2 == k:
              current_box['relations'][str(n)]['name'] = info_list[node1]['label']
              current_box['relations'][str(n)]['id'] = bi_relation
              current_box['relations'][str(n)]['object'] = scene_graph[name]['objects'][str(node1)]['id']
              bi_relation += 1

  if type == 1:
    return scene_graph
  if type == 0:
    return scene_graph
              
# the bounding box format of docbank dataset is different from 
# other datasets, which need be transfered into [x,y,w,h] 
def bbox_transfer(bbox):
  new_bbox = []
  new_bbox.append(bbox[0])
  new_bbox.append(bbox[1])
  new_bbox.append(bbox[2]-bbox[0])
  new_bbox.append(bbox[3]-bbox[1])
  return new_bbox

# docbank dataset scene graph generator
def docbank_scene_graph_generator(image_path,box_path):
  with open(image_path) as f:
    img_json = json.load(f)
  df_box = pd.read_csv(box_path)
  bbox_list = df_box.values.tolist()
  # 0:id, 1:x1, 2:y1, 3:x2, 4:y2, 5:label, 6:text, 7:image_id
  scene_graph = {}
  relation_id = 0
  s_relation_id = 0
  bbox_id = 0 # testing setting is 0
  for i in range(3):
    print(i)
    img_id = img_info[i]['id']
    name = img_info[i]['name']
    print(name)
    scene_graph[name] = {}
    scene_graph[name]['id'] = img_id
    scene_graph[name]['width'] = img_info[i]['page_size'][0]
    scene_graph[name]['height'] = img_info[i]['page_size'][1]
    scene_graph[name]['objects'] = {}
    num_bbox = 0
    for j in range(len(bbox_list)):
      if bbox_list[j][7] == img_id:
        scene_graph[name]['objects'][str(num_bbox)] = {}
        scene_graph[name]['objects'][str(num_bbox)]['id'] = bbox_id
        scene_graph[name]['objects'][str(num_bbox)]['box'] = bbox_transfer(bbox_list[j][1:5])
        scene_graph[name]['objects'][str(num_bbox)]['category'] = bbox_list[j][5]
        scene_graph[name]['objects'][str(num_bbox)]['text'] = bbox_list[j][6]
        scene_graph[name]['objects'][str(num_bbox)]['relations'] = {}
        bbox_id += 1
        num_bbox += 1
    for k in scene_graph[name]['objects']:
      objects = scene_graph[name]['objects'][k]
      obj_relations = 0
      for others in scene_graph[name]['objects']:
        if others != k:
          others = scene_graph[name]['objects'][others]
          objects['relations'][str(obj_relations)] = {}
          objects['relations'][str(obj_relations)]['id'] = str(relation_id)
          objects['relations'][str(obj_relations)]['object'] = others['id']
          bbox1 = objects['box']
          bbox2 = others['box']
          scene_graph[name]['objects'][k]['relations'][str(obj_relations)]['name'] = relative_position(bbox1,bbox2)
          obj_relations += 1
          relation_id += 1
  return scene_graph

