print("hello world")
import ollama

response = ollama.chat("llama2", messages=[{"role": "user", "content": "Tell me a joke"}])
print(response["message"]["content"])
