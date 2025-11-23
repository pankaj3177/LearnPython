#1.1 Convert 3.75 to an integer and print the value
print(int(3.75))    #3

#1.2 Convert "123" to a float and print the value
print(float(123))   #123.0

#1.3 Convert 0 to a boolean and print the value
print(bool(0))      #False

#1.4 Convert False to a string and print the value
print(str(False))   #False

#2.1 Convert all characters in the string to uppercase. x = "hello"
x = "hello"
print(x.upper())    #HELLO

#3 Given x = 5 and y = 3.14, calculate z = x + y and determine the data type of z. And convert it to integer
x=5
y=3.14
z=x+y
print(type(z))      #<class 'float'>
print(int(z))       #8

#4
s = 'hello'

#4.1 Convert the string to uppercase.
print(s.upper())                        #HELLO

#4.2 Replace 'e' with 'a'.
print(s.replace('e','a'))   #hallo

#4.3 Check if the string starts with 'he'.
print(s.startswith('he'))               #True

#4.4 Check if the string ends with 'lo'.
print(s.endswith('lo'))                 #True