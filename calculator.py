print("1- addition")
print("2- substraction")
print("3- multiplication")
print("4- division")
option = int(input("Choose the option:"))
if(option in[1,2,3,4]):
    a = int(input("Enter the first num:"))
    b = int(input("Enter the second num:"))
    if(option == 1):
        result = a + b
    elif(option == 2):
        result = a - b
    elif(option == 3):
        result = a * b  
           
    elif(option == 4):
        result = a // b


else:
    print("Invalid operation") 
print("Result of operation is {}".format(result))       

      