'''
Python的六大基本类型,可以通过type()方法进行查询当前的值:int,float,string,boolean,bytes
    int 整数类型
        python暂时没有Int的局限(没有长度限制)
    float 浮点数
        浮点数强调的是小数的表现形式
    string 字符串,字符序列
        有序的!
        字符串的表示：
            x = ''
            x = ""
            x = '''''' 支持换行等方式记录字符串
        转义字符：
            告诉python解释器，当前表示的是一个字符,或者是特殊字符
                s = "2\"" 通过\来转义 "
                s = "2\n" 通过\来转义 换行
    boolean 布尔值
        用来表示"True"或"False"
            True == 1
            False == 0
    bytes 二进制序列
        二进制的表示形式
    None 空
        
'''

# int
print("int类型")
a = 2
print("a = 2")
# type 和 Str类型不能使用+
print(type(a))

# float
print("\nfloat类型")
a = 1.2
print("a = 1.2")
print(type(a))

# string
print("\nstring类型")
a = "2"
print('a = "2"')
print(type(a))

a = "Hello"
print('a = Hello')
print(type(a))

# boolean
print("\nboolean类型")
a = bool(0)
print("a = bool(0)")
print(a)
print(type(a))

# bytes
print("\nbytes类型")
a = bytes("Hello".encode("utf-8"))
print("a = bytes('Hello'.encode('utf-8'))")
print(a)
print(type(a))