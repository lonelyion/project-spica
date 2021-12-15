# Project Spica

Bilibili直播自动录制、上传网盘([奶牛](https://cowtransfer.com)、OneDrive等)、投稿到B站的一体机，同时调用BOT发送群内通知。

本项目是为了[真綿真珠星_official](https://space.bilibili.com/2113007488)的[字幕组](https://space.bilibili.com/2062226233)工作流设计的，故取名Spica

## 已经实现的功能

+ 直播录制(streamlink)
+ 上传到奶牛网盘(付费版)
+ 调用[rclone](https://rclone.org)上传到支持的存储系统，例如OneDrive
+ 通过go-cqhttp进行通知发送

## 还需要做的功能

+ YAML作为配置文件
+ 使用文档
+ 上传失败重试
+ 投稿到B站并设置定时发布

## 支持与贡献

觉得好用可以给这个项目点个 Star 

有意见或者建议也欢迎提交 [Issues](https://github.com/lonelyion/project-spica/issues) 和 [Pull requests](https://github.com/lonelyion/project-spica/requests)。

## 许可证
本项目使用 [GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/) 作为开源许可证。