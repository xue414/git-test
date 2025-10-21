def echo():
    message = input("Enter something: ")
    print(message)

if __name__ == "__main__":
    echo()
import sys 
def echo(): 
    shout = "-s" in sys.argv 
    message = input("Enter something: ") 
    print(message.upper() if shout else message) 
if __name__ == "__main__": 
    echo()
    