#!/bin/bash
# 每周 5 使用 tar 命令备份/var/log 下的所有日志文件
# vim  /root/logbak.sh
# 编写备份脚本,备份后的文件名包含日期标签,防止后面的备份将前面的备份数据覆盖
# 注意 date 命令需要使用反引号括起来,反引号在键盘<tab>键上面

tar -czf log-`date +%Y%m%d`.tar.gz /var/log

# crontab -e #编写计划任务，执行备份脚本
00 03 * * 5 /home/wenmin/datas/logbak.sh