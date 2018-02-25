def func(path):
    with open(path) as f:
        arr = f.read().split(',')
        for tag in arr:
            print('123' + tag)


func('target.txt')
