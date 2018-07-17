#read the input from the user

num_array = list()
num = raw_input("Enter how many elements you want:")
#print 'Enter number of strings in array: '
for i in range(int(num)):
    n = raw_input("string :")
    num_array.append(str(n))
print 'ARRAY: ',num_array

#array = ['arun','sanna','cherry']
#print array