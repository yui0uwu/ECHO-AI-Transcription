import whisper
model = whisper.load_model("base")

print("Transcribing your M4A file...")
result = model.transcribe("test.m4a") 

print("-" * 30)
print(result["text"])
print("-" * 30)