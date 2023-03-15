'''
Python四大基本数据结构:list,tuple,dict,set
    list 列表
        作用:
            用来装在不同数据类型的数据集结构
        特点:
            有序的
            可以装载任何数据类型
            可以更改
        创建:
            使用list()新建一个列表
            通过[]声明一个列表
    tuple 元组
        作用:
            不可修改的列表,常用来表示记录
        特点:
            有序的
            可以装载任何数据类型
            不可以更改
        创建:
            通过tuple()来新建一个元组
            通过()来声明一个元组
    dict 字典 hashtable 通过hash（散列）函数将传入的key值生成的地址来查找value
        作用：
            通过key进行 返回 value
        特点：
            无序的

'''

# list
print("list 集合")
print("使用list()新建一个列表")
a = list("Hello Python")
print('a = list("Hello Python")')
print(a)
print("通过[]声明一个列表")
a = [1,2,3]
print("a = [1,2,3]")
print(a)

print("\ntuple 元组")
print("通过tuple()来新建一个元组")
a = tuple("Hello Python")
print('a = tuple("Hello Python")')
print(type(a))