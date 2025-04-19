import google.generativeai as genai

genai.configure(api_key="AIzaSyDiuczDaVsxxEZPqjKCBwAamZXCliDEqR4")

# Use the latest available model
model = genai.GenerativeModel("gemini-1.5-pro-latest")  

response = model.generate_content("Hello, how are you?")
print(response.text)
