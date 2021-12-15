# -*- coding: UTF-8 -*-
"""
全局配置
"""

# 检测开播的间隔，单位秒
LOOP_INTERVAL = 30

# 临时保存目录相对路径
RECORD_DIR = 'record_video/'

# 是否删除已经上传好的录播
DELETE_UPLOADED = True

# streamlink的路径，留空使用系统路径
STREAM_LINK_PATH = ''
#/home/ion/.conda/envs/record/bin/streamlink

# cowtransfer-uploader的路径，留空使用系统路径
COWTRANSFER_PATH = '/home/xxxxxxxxxxx/bin/cowtransfer-uploader'

# rclone的路径，留空使用系统路径
RCLONE_PATH = ''
#/usr/bin/rclone

# Go-CQHTTP的HTTP服务监听地址
HTTP_BOT = "http://localhost:5700/"

# Go-CQHTTP的Access Token（如果有）
BOT_ACCESS_TOKEN = ""

# 直播间配置
watch_lives = [
  {
    'id': 449047,
    'group_id': 123456789,
    'uploads': [
      {
        'platform': 'rclone',
        'path': 'od:/public/miriko_record'
      },
      {
        'platform': 'cowtransfer',
        'path': '/录播',
        'remember-mev2': 'XXXXXXXXXXXXXXXXXXXXXXX',
        'cow-auth-token': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
      },
      {
        'platform': 'bilibili',
        'account': 'test',
        'password': 'password'
      }
    ]
  },
  {
    'id': 23705645,
    'group_id': 123456789,
    'uploads': [
      {
        'platform': 'rclone',
        'path': 'aws:/public/spica_record'
      },
      {
        'platform': 'cowtransfer',
        'path': '/录播2',
        'remember-mev2': 'XXXXXXXXXXXXXXXXXXXXXXX',
        'cow-auth-token': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
      },
    ]
  }
]

