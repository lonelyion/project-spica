import requests
import sys
import time
import subprocess
import random
import logging
from pathlib import Path

import config
from utils import bot_send

class Bilibili:
  def __init__(self, id) -> None:
    self.id = id
    self.title = ''
    self.file_name = ''
    self.logger = logging.getLogger(f'bilibili/{self.id}')
  
  def check_stream(self) -> bool:
    # 开播检测
    room_init_data = requests.get(f"https://api.live.bilibili.com/room/v1/Room/room_init?id={self.id}").json()
    if room_init_data['code'] == 0:
      vid = room_init_data['data']['room_id']
    else:
      self.logger.info('Get room ID from API failed: %s', room_init_data)
      vid = self.id
    
    room_info_data = requests.get(f"https://api.live.bilibili.com/room/v1/Room/get_info?room_id={vid}").json()
    if room_info_data['code'] != 0:
      self.logger.debug(room_init_data)
      return False
    
    room_info_data = room_info_data['data']
    self.title = room_info_data['title']
    self.logger.info(f'room {self.id} status {room_info_data["live_status"]}')
    if room_info_data['live_status'] != 1:
      return False
    return True
  
  def download(self, filename) -> int:
    # 调用streamlink录制直播
    if len(config.STREAM_LINK_PATH) == 0:
      path = 'streamlink'
    else:
      path = config.STREAM_LINK_PATH
    proc_args = [ path,
                '--loglevel', 'trace',
                '--config', Path(__file__).absolute().parent / "streamlink_cookies.conf",
                f'https://live.bilibili.com/{self.id}',
                'best',
                '-o', Path(__file__).absolute().parent / config.RECORD_DIR / filename
                ]
    self.logger.info(f'start recording {self.id}')
    proc = subprocess.Popen(proc_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
      with proc.stdout as stdout:
        for line in iter(stdout.readline, b''):  # b'\n'-separated lines
          #print(line.decode(), end='', file=sys.stderr)
          self.logger.debug(f'streamlink:{line.decode().rstrip()}')
      retval = proc.wait()
    except KeyboardInterrupt:
      if sys.platform != 'win32':
        proc.communicate(b'q')
      raise
    return retval

  def run(self, group_id):
    try:
      while True:
        if not self.check_stream():
          time.sleep(config.LOOP_INTERVAL)
        else:
          break
      start_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
      self.file_name = f'bilibili_{self.id}_{start_time}_{self.title}.flv'
      message = f'开始录制直播间{self.id}\n标题:{self.title}\n开始时间:{start_time}'
      bot_send(group_id, message)
      retval = self.download(self.file_name)
      self.logger.info(f'streamlink ret code:{retval} for {self.file_name}')
      return (retval, self.file_name)
    except:
      self.logger.exception("Unexpected expection at Bilibili.run")
      self.logger.exception(sys.exc_info)
