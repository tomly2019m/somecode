import pandas as pd

# 如果要获取2018年的 将下方的2019_1修改成2018_1即可
data2 = pd.read_excel(
    '2019_1.xlsx',
    sheet_name="Sheet1"
)

data3 = pd.read_excel(
    '2019_1.xlsx',
    sheet_name='Sheet2'
)

names = ['E' + str(x) for x in range(1, 124)]
zero = [0 for x in range(1, 124)]

Intimes = dict(zip(names, zero))
Outtimes = dict(zip(names, zero))
totalsOF2019 = dict(zip(names, zero))
totalsOF2019OUT = dict(zip(names, zero))
noUses = dict(zip(names, zero))
miniustimes = dict(zip(names, zero))
noUseschu = dict(zip(names, zero))

index = 0
for j in data2['企业代号']:
    if data2['发票状态'][index] == '有效发票':
        Intimes[j] += 1
        totalsOF2019[j] += data2['金额'][index] - data2['税额'][index]
        if data2['金额'][index] < 0:
            miniustimes[j] += 1
    else:
        noUses[j] += 1
    index += 1

index = 0
for j in data3['企业代号']:
    if data3['发票状态'][index] == '有效发票':
        Outtimes[j] += 1
        totalsOF2019OUT[j] += data3['金额'][index] - data3['税额'][index]
    else:
        noUseschu[j] += 1
    index += 1


def output(year: str):
    with open(year + '进.txt', 'w') as f:
        for i in Intimes:
            f.write(str(Intimes[i]))
            f.write('\n')

    with open(year + '出.txt', 'w') as f:
        for i in Outtimes:
            f.write(str(Outtimes[i]))
            f.write('\n')

    with open(year + '进废弃.txt', 'w') as f:
        for i in noUses:
            f.write(str(noUses[i]))
            f.write('\n')

    with open(year + '出废弃.txt', 'w') as f:
        for i in noUseschu:
            f.write(str(noUseschu[i]))
            f.write('\n')

    with open(year + '进负.txt', 'w') as f:
        for i in miniustimes:
            f.write(str(miniustimes[i]))
            f.write('\n')

    with open(year + '净.txt', 'w') as f:
        for i in totalsOF2019:
            temp = totalsOF2019OUT[i] - totalsOF2019[i]
            f.write(str(temp))
            f.write('\n')


if __name__ == '__main__':
    output('2019')
# 要获取不同年份的数据 只需要修改一下相应的年份即可
