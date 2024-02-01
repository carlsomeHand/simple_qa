import os
import json

# 获取当前脚本文件的绝对路径
prefix_path = os.path.split(os.path.abspath(__file__))[0]

CORPUS = os.path.join(prefix_path, 'Sam_Altman.txt')
api_json = os.path.join(prefix_path, 'api.json')

with open(api_json, 'r', encoding='utf-8') as f:
     api_key = json.load(f)['api_key']

# api_key = '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'
