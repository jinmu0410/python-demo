import sys



def hello(ip,movieId):
    url = 'http://#{ip}/media/video/movie/#{movieId}/batchUpload'
    http_url = url.replace("#{ip}", ip).replace("#{movieId}", movieId)
    print(http_url)

if __name__ == '__main__':
    param = input("请输入ip：")

    path = input("请输入视频路径：")
    print(path)

    #http_url = url.replace("#{ip}", ip).url.replace("#{movieId}", movieId)

    print(hello(ip,movieId))

