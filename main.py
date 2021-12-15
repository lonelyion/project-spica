import sys
import time
import logging
from multiprocessing import Process, Manager
from pathlib import Path
from queue import Queue

import config
from biliibli import Bilibili
from upload_platforms import up_cowtransfer, up_rclone
from utils import bot_send

manager = Manager()
logger = logging.getLogger('main')
monitor_pool = []

up_queue = manager.Queue()

def upload_worker():
  logger.info('上传线程开始')
  while True:
    (path, upconfs, group_id) = up_queue.get(block=True)
    logger.info(f'upload_queue get value {path}')
    if path is None:
      break
    do_upload(path, upconfs, group_id)
    up_queue.task_done()
  logger.info('上传线程退出')
    
def do_upload(path, upconfs, group_id):
  filename = Path(path).name
  success_platforms = []
  for conf in upconfs:
    logger.info(f'开始上传到{conf["platform"]}: {conf["path"]}')
    ret = -1
    if conf['platform'] == 'cowtransfer':
      ret = up_cowtransfer(path, conf)
    elif conf['platform'] == 'rclone':
      ret = up_rclone(path, conf)
    else:
      logger.info(f'还不支持{conf["platform"]}')
    if ret == 0:
      success_platforms.append(dict(platform=conf['platform'], remote_path=conf['path']))
    logger.info(f'上传任务结束{conf["platform"]}: {conf["path"]}')
  
  if len(success_platforms) > 0:
    # 有一个成功就算成功
    if config.DELETE_UPLOADED:
      Path(path).unlink()
      logger.info(f'删除了文件{path}')
    if group_id:
      message = f'录播{filename}成功上传到:\n'
      for item in success_platforms:
        message += f'【{item["platform"]}】{item["remote_path"]}\n'
      bot_send(group_id, message)
  elif group_id:
      message = f'悲报！录播{filename}一个都没上传成功！'
      bot_send(group_id, message)

def monitor(item):
  instance = Bilibili(item['id'])
  while True:
    #(0,'bilibili_23705645_20211211_194644_【测试用】不要点进来.flv')
    (ret, filename) = instance.run(item['group_id'])
    if ret != 0:
      logger.info(f'Streamlink录制错误, code {ret}')
    else:
      # 检查文件
      path = Path(__file__).absolute().parent / config.RECORD_DIR / filename
      if not (path.exists() and path.is_file()):
        logger.info(f'{filename}文件不存在，跳过')
        continue
      #if path.stat().st_size < 3000000:
      #  continue
      logger.info('录制结束并且文件存在')
      # 进行上传
      up_queue.put((path, item['uploads'], item['group_id']))
      pass
  
def main():
  try:
    for item in config.watch_lives:
      m_proc = Process(target=monitor,args=(item,))
      m_proc.start()
      monitor_pool.append(m_proc)
      if config.watch_lives.index(item) != len(config.watch_lives) - 1:
        time.sleep(config.LOOP_INTERVAL / len(config.watch_lives))
    
    up_proc = Process(target=upload_worker)
    up_proc.start()

    for proc in monitor_pool:
      proc.join()
    up_proc.join()
  except KeyboardInterrupt:
    up_queue.put((None, None, None))
    while up_queue.qsize() != 0:
      print(f'WAITING FOR THE UPLOAD TASKS BEING DONE! {up_queue.qsize()}')
      time.sleep(5)
    
    for proc in monitor_pool:
      proc.terminate()
    up_proc.terminate()
  except:
    logger.info(f'Error running thread for {item["id"]}')
    logger.exception(sys.exc_info)


if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)
  main()