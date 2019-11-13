# # A simple generator function
# def my_gen():
#     n = 1
#     print('This is printed first')
#     # Generator function contains yield statements
#     yield n
#
#     n += 1
#     print('This is printed second')
#     yield n
#
#     n += 1
#     print('This is printed at last')
#     yield n
#
#
#
# def my_gen_2():
#     i=0
#     while(True):
#         arr = [0,1,2,3,4,5,6,7,8,9]
#         print('arr[i] : ',i)
#         yield
#         i+=1
#
# n = my_gen_2()
# for i in range(5):
#     print('i:',i)
#     next(n)

def test():
    print("in test....")