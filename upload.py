import requests
import json
import os
import sys
import time
import subprocess
import random
import logging
import traceback
from pathlib import Path

import config

def up_cowtransfer(path, upconf):
  logger = logging.getLogger('upload/cow')
  cow_path = 'cowtransfer-uploader' if len(config.COWTRANSFER_PATH) == 0 else config.COWTRANSFER_PATH
  transfer_url = ''
  if upconf['platform'] == 'cowtransfer':
    proc_args = [ cow_path,
                  '-c', f'"remember-mev2={upconf["remember-mev2"]};"',
                  '-a', f'"{upconf["cow-auth-token"]}"',
                  '-p', '8',
                  '--valid', '30',
                  '--silent',
                  path
                ]
    logger.info(f'开始上传{path}到奶牛网盘')
    proc = subprocess.Popen(proc_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
      with proc.stdout as stdout:
        for line in iter(stdout.readline, b''):  # b'\n'-separated lines
          line = line.decode().rstrip()
          if line.startswith('Destination'):
            transfer_url = line.split(' ')[1]
          logger.debug(f'cowtransfer-uploader:{line}')
      retval = proc.wait()
      if retval != 0:
        logger.info(f'cowtransfer-upload exit with {retval}')
      else:
        logger.info(f'cowtransfer-upload transfer link {transfer_url}')
        # 先获取一下GUID
        # https://cowtransfer.com/api/transfer/v2/transferdetail?url=565a736a57cc42
        req_headers = {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
          'Origin': 'https://cowtransfer.com',
          'Referer': transfer_url,
          'Authorization': upconf['cow-auth-token'],
          'Cookie': f'remember-mev2={upconf["remember-mev2"]};cow-auth-token={upconf["cow-auth-token"]};'
        }
        transfer_id = transfer_url.split('/')[-1]
        transfer_detail = requests.get(f'https://cowtransfer.com/api/transfer/v2/transferdetail?url={transfer_id}',
                                        headers=req_headers).json()
        transfer_guid = transfer_detail['guid']   #565a736a-57cc-42fb-8d9d-25c97ac7571f
        logging.info(f'got transfer guid {transfer_guid}')
        # 然后移动到指定路径
        # 手动构建multipart的payload，用files不知道出什么问题
        payload = f'-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"fileGuids\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"transferGuids\"\r\n\r\n{transfer_guid}\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"path\"\r\n\r\n{upconf["path"]}\r\n-----011000010111000001101001--\r\n'
        req_headers['Content-Type'] = 'multipart/form-data; boundary=---011000010111000001101001'
        save_to_result = requests.post('https://cowtransfer.com/api/space/out/saveto', 
                                       data=payload.encode('utf-8'), 
                                       headers=req_headers
                                      ).json()
        if save_to_result['errorCode'] == 0:
          # ok
          logger.info(f'{path} uploaded to cowtransfer directory {upconf["path"]} with link {transfer_url}')
    except:
      logger.info('unexpected error')
      logger.exception(traceback.format_exc())
    return
