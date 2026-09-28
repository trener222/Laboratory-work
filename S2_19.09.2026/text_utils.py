
# Решение задания 7

def load_data():
    return [3, 17, 8, 25, 6, 12, 25, 9, 14]
def filter_above(values, threshold=10):
    total=[]
    for x in values:
        if x>threshold:
            total.append(x)
    return total
def mean(values):
    return sum(filter_above(values))/len(filter_above(values))

if __name__ == '__main__':
    print('Самопроверка:', mean(load_data()))
