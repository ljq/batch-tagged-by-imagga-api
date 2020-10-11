#!/usr/bin/env python
# coding=utf-8

import requests, json
import sys
import config

def upload_imagga(image_path):                
        response = requests.post('https://api.imagga.com/v2/uploads',
                                 auth=(config.api_key, config.api_secret),
                                 files={'image': open(image_path, 'rb')})
        if (response.json()['status']['type'] == 'success'):
                print ('\t Upload successful')
                upld_id = response.json()['result']['upload_id']
                return (upld_id)
        else:
                print('\t Something went wrong. Exiting...')
                sys.exit(2)
  

def tag_imagga(t_image):
        response = requests.get('https://api.imagga.com/v2/tags?image_upload_id=%s' % t_image,
                                auth=(config.api_key, config.api_secret))
        if (response.json()['status']['type'] == 'success'):
            print ('\t Tagging successful')
            return(response.json())
        else:
                print('\t Something went wrong. Exiting...')
                sys.exit(2)
        

def delete_imagga(upld_id):
        response = requests.delete('https://api.imagga.com/v2/uploads/%s'
                                   % (upld_id), auth=(config.api_key, config.api_secret))
        if (response.json()['status']['type'] == 'success'):
            print ('\t Delete successful')
            return(response.json())
        else:
                print('\t Something went wrong. Exiting...')
                sys.exit(2)
        
        
def task_process(t_image, catname_dir):
        # Upload the image 
        #print('Uploading image to Imagga: ', t_image)
        upld_id = upload_imagga(t_image)
        
        # Tag the image 
        print('Tagging the image ('+catname_dir+'):')
        tags_json = tag_imagga(upld_id)

        ## Parse the tags and print
        tags_data = tags_json['result']['tags']
        if config.debug_mode==True:
            num_tags = len(tags_json['result']['tags'])
            tags_to_print = min(num_tags, config.limit_print_num_tags)

            print ('\t Top tags (confidence score):')
            print ('CatNameDir：'+catname_dir+'\t')
            for i in range(tags_to_print):
                print('\t {} {}'.format(str(tags_json['result']['tags'][i]['tag']['en']),
                    round(tags_json['result']['tags'][i]['confidence'], 1)))
            return
        
        # Delete the image
        #print('Deleting image from Imagga:')
        delete_imagga(upld_id)
        return tags_data
