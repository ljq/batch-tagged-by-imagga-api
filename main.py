#!/usr/bin/env python
# coding=utf-8
# Batch tagged images By imagga API

import os, sys, json
import config
import tagging

def main():
    # check python version < 3
    if sys.version_info < (3, 10):
        print("current python version is less 3.10, current version: %s." % sys.version)
        return
    
    tag_input = config.tag_input
    print('Tagging images started')

    if os.path.isdir(tag_input):
        tag_cat_dirs = os.listdir(tag_input)
        
        for catname_dir in tag_cat_dirs:
            # cat dir tagging
            cat_files = os.listdir(tag_input+'/'+catname_dir)
            results = {}
            for catname_file in cat_files:
                # tagging 
                cat_list_file = tag_input+'/'+catname_dir+'/'+catname_file
                tags_data = {}
                tags_data = tagging.task_process(cat_list_file, catname_dir)
                results[catname_file] = tags_data
            
            # 输出文件夹检查
            tag_output_path=config.tag_output+'/'+catname_dir
            if os.path.exists(tag_output_path):
                pass
            else:
                os.mkdir(tag_output_path)
            
            # 聚合写入json文件
            tags_json_data = json.dumps(results)
            with open (file = tag_output_path+'/'+catname_dir+'.json', mode = "w+",encoding = "utf-8") as catname_dir_file:
                status = catname_dir_file.write(tags_json_data)
                print(status)
        
if __name__ == '__main__':
    main()