import os
import sys
import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


def upload_videos_in_directory(url,directory_path,batch_size =20):
    # 获取目录中的所有文件
    all_files = [os.path.join(directory_path, file) for file in os.listdir(directory_path)]

    # 筛选出所有的MP4文件
    video_files = [file for file in all_files if file.lower().endswith('.mp4')]

    # 根据批次大小分割文件列表
    batches = [video_files[i:i+batch_size] for i in range(0, len(video_files), batch_size)]

    num = 0
    for batch in batches:
        num=num+1
        # 创建文件列表
        files = [('files', (os.path.basename(file), open(file, 'rb'), 'video/mp4')) for file in batch]

        # 创建并配置多部分编码器
        multipart_data = MultipartEncoder(fields=files)
        headers = {'Content-Type': multipart_data.content_type}

        print(f'开始上传批次 {num} ，请稍等！')
        # 发送POST请求
        response = requests.post(url, data=multipart_data, headers=headers)

        # 检查响应状态码
        if response.status_code == 200:

            print(f'批次 {num} 中的视频文件上传成功！')
            res = json.loads(response.text)['data']

            if 'totalFileNum' in res:
                print(f"当前批次{num},上传视频个数：" + str(res['totalFileNum']))
            if 'time' in res:
                print(f"当前批次{num},上传消耗时间：" + str(res['time']) + "毫秒")
            if 'successList' in res:
                successList = res.get("successList")
                for string_value in successList:
                     print(f'List item: {string_value}')
                print(f'当前批次{num},上传成功的视频列表: ' + str(successList))
            if 'errorList' in res:
                errorList = res.get("errorList")
                print(f'当前批次{num},上传失败的视频列表: ' + str(errorList))
        else:
            print(f'批次 {num} 中的视频文件上传失败，状态码: {response.status_code}')

        print("---------------------------------")

    print("所有批次上传完成")

if __name__ == '__main__':
    movieId = input("请输入电影ID：")
    file_path = input("请输入视频文件目录：")

    # movieId = '1744730060566380545'
    # file_path = '/Users/jinmu/Documents/1'

    url = "http://94.74.75.38:8091/media/video/movie/#{movieId}/batchUpload"
    http_url = url.replace("#{movieId}", movieId)

    upload_videos_in_directory(http_url, file_path, 20)
    #upload_videos_in_directory("http://127.0.0.1:8091/media/video/movie/1744730060566380545/batchUpload","/Users/jinmu/Documents/3",2)
