print("hello world")
import ollama

flag = 0
while flag != 1: 
    x = input("You :")
    response = ollama.chat("llama2", messages=[{"role": "user", "content": x}])
    print(response["message"]["content"])
    if response["message"]["content"] == "Goodbye":
        flag = 1