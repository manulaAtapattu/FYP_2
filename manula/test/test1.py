
# TimeLapse.a.append(3)
# print(TimeLapse.a)
import time
arr=[]

def f1(i):
    arr.append(i)

i=0
while True:
    if len(arr)>=10:
        print(arr[i])
        i+=1
    else:
        print("size not enough")
        time.sleep(1)
