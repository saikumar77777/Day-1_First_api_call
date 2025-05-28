import openai

openai.api_key = "YOUR_API_KEY"


system_prompt = {"role": "system", "content": "You are a helpful assistant."}

# Get user input
user_input = input("Enter your prompt: ")
user_prompt = {"role": "user", "content": user_input}

# Call GPT-3.5-turbo
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[system_prompt, user_prompt]
)

# Extract assistant reply
assistant_reply = response["choices"][0]["message"]["content"]
print("\nAssistant Response:\n", assistant_reply)

# Token usage
usage = response["usage"]
print("\nToken Usage:")
print(f"Prompt tokens: {usage['prompt_tokens']}")
print(f"Completion tokens: {usage['completion_tokens']}")
print(f"Total tokens: {usage['total_tokens']}")
