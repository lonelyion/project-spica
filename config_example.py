# -*- coding: UTF-8 -*-
"""
全局配置
"""

# 检测开播的间隔
LOOP_INTERVAL = 30
# 最短录制时间(s)
MIN_INTERVAL = 180
# 临时保存目录相对路径
RECORD_DIR = 'record_video/'
# 是否删除已经上传好的录播
DELETE_UPLOADED = True
# streamlink的路径，留空使用系统路径
STREAM_LINK_PATH = ''
#/home/ion/.conda/envs/record/bin/streamlink
# cowtransfer-uploader的路径，留空使用系统路径
COWTRANSFER_PATH = '/home/xxxxxxxxxxx/bin/cowtransfer-uploader'
# Go-CQHTTP的HTTP服务监听地址
HTTP_BOT = "http://localhost:5700/"
# Go-CQHTTP的Access Token（如果有）
BOT_ACCESS_TOKEN = ""

WATCH_LIVES = [
  {
    'id': 449047,
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