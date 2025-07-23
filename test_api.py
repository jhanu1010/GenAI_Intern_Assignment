import requests

questions = [
    "What is my total sales?",
    "Which product had the highest CPC?",
    "Calculate the RoAS"
]

for q in questions:
    print("\n----------------------------")
    print("Question:", q)
    response = requests.post("http://127.0.0.1:8000/ask", json={"question": q})
    print("Response status:", response.status_code)
    print("Response data:", response.json())
