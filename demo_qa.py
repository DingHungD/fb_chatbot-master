import Chatbot.chatbot as Chatbot

chatter = Chatbot.Chatbot(build_console=False)

print("Hello, I am Mianbot.")

while True:
    raw = input()
    if raw == "_END_":break
    reply,confidence = chatter.testQuestionAnswering(raw)
    
    print("%s" % (reply))