
fp = open('/Users/jinmu/Downloads/test-csv-1.csv', 'rb')

fp.read([10])                         # size为读取的长度，以byte为单位
fp.readline([10])                     # 读一行，如果定义了size，有可能返回的只是一行的一部分
fp.readlines([10])                    # 把文件每一行作为一个list的一个成员，并返回这个list。其实它的内部是通过循环调用readline()来实现的。如果提供size参数，size是表示读取内容的总长。
fp.readable()                           # 是否可读
fp.write(str)                           # 把str写到文件中，write()并不会在str后加上一个换行符
#fp.writelines(seq)                      # 把seq的内容全部写到文件中(多行一次性写入)
fp.writeable()                          # 是否可写
fp.close()                              # 关闭文件。
fp.flush()                              # 把缓冲区的内容写入硬盘
fp.fileno()                             # 返回一个长整型的”文件标签“
fp.isatty()                             # 文件是否是一个终端设备文件（unix系统中的）
fp.tell()                               # 返回文件操作标记的当前位置，以文件的开头为原点
fp.next()                               # 返回下一行，并将文件操作标记位移到下一行。把一个file用于for … in file这样的语句时，就是调用next()函数来实现遍历的。
fp.seek(10)                # 将文件打操作标记移到offset的位置。whence可以为0表示从头开始计算，1表示以当前位置为原点计算。2表示以文件末尾为原点进行计算。
fp.seekable()                           # 是否可以seek
fp.truncate([10])                     # 把文件裁成规定的大小，默认的是裁到当前文件操作标记的位置。

