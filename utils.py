import re

import config
import requests
import logging

def reg_match(text, pattern):
  match = re.search(pattern, text)
  if match:
    return match.group(1)
  else:
    return None

def bot_send(group_id, message):
  if len(config.HTTP_BOT):
    logger = logging.getLogger('bot')
    params = {
      'group_id': group_id,
      'message': message,
      'auto_escape': True
    }
    if len(config.BOT_ACCESS_TOKEN) > 0:
      params['access_token'] = config.BOT_ACCESS_TOKEN
    url = config.HTTP_BOT + ('' if config.HTTP_BOT[-1] == '/' else '/') + 'send_group_msg'
    headers = { 'Content-Type': 'application/x-www-form-urlencoded'}
    res = requests.get(url, params=params, headers=headers)
    if res.status_code != 200:
      logger.info(f'发送消息失败 {res.status_code}\n{res.text}')
    logger.debug(f'发送消息到{group_id}, 返回结果{res.text}')
