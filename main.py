import sys
import time
import logging
from multiprocessing import Process, Manager
from pathlib import Path
from queue import Queue

import config
from biliibli import Bilibili
from upload import up_cowtransfer

manager = Manager()
logger = logging.getLogger('main')
monitor_pool = []

up_queue = manager.Queue()

def upload_worker():
  logger.info('upload worker started')
  while True:
    (path, upconfs) = up_queue.get(block=True)
    logger.info(f'upload_queue get value {path}')
    if path is None:
      break
    do_upload(path, upconfs)
    up_queue.task_done()
  logger.info('upload_worker exited')
    
def do_upload(path, upconfs):
  logger.info(upconfs)
  for conf in upconfs:
    if conf['platform'] == 'cowtransfer':
      logger.info(f'started for uploading to cowtransfer {conf["path"]}')
      up_cowtransfer(path, conf)
      logger.info(f'finished for uploading to cowtransfer {conf["path"]}')
    else:
      logger.info(f'{conf["platform"]} not supported yet')

def monitor(item):
  instance = Bilibili(item['id'])
  while True:
    #(0,'bilibili_23705645_20211211_194644_【测试用】不要点进来.flv')
    (ret, filename) = instance.run()
    if ret != 0:
      logger.info(f'Streamlink download error, code {ret}')
    else:
      # 检查文件
      path = Path(__file__).absolute().parent / config.RECORD_DIR / filename
      if not (path.exists() and path.is_file()):
        logger.info(f'{filename} not exist, skipping')
        continue
      #if path.stat().st_size < 3000000:
      #  continue
      logger.info('record ended and check pass')
      # 进行上传
      up_queue.put((path, item['uploads']))
      pass
  
def main():
  try:
    for item in config.WATCH_LIVES:
      m_proc = Process(target=monitor,args=(item,))
      m_proc.start()
      monitor_pool.append(m_proc)
      if config.WATCH_LIVES.index(item) != len(config.WATCH_LIVES) - 1:
        time.sleep(config.LOOP_INTERVAL / len(config.WATCH_LIVES))
    
    up_proc = Process(target=upload_worker)
    up_proc.start()

    for proc in monitor_pool:
      proc.join()
    up_proc.join()
  except KeyboardInterrupt:
    up_queue.put((None, None))
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
  logging.basicConfig(level=logging.INFO)
  main()