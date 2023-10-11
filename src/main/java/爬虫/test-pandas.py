import pandas


if __name__ == '__main__':
    path = '/Users/jinmu/Downloads/test-csv.csv'
    data = pandas.read_csv(path)
    print(data)

    # index=False 忽略索引
    data.to_csv('/Users/jinmu/Downloads/test-csv-2.csv', index=False)