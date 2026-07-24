import tiktoken

enc=tiktoken.encoding_for_model("gpt-4o")
text="hey there! my name is Piyush"
tokens=enc.encode(text)
print("Tokens",tokens)

decode=enc.decode([48467, 1354, 0, 922, 1308, 382, 398, 3403, 1776])
print(decode)