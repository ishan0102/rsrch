# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai
import pdfplumber

# r = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Who won the world series in 2020?"},
#         {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
#         {"role": "user", "content": "Where was it played?"},
#     ],
# )

# print(r)


with pdfplumber.open("papers/Attention_Is_All_You_Need.pdf") as pdf:
    first_page = pdf.pages[0]
    print(first_page.chars[0])
