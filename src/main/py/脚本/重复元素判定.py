
#判断是否重复
def all_unique(str):
    return len(str) == len(set(str))




if __name__ == '__main__':
    str = (1,2,3,4,3,5)
    print(all_unique(str))