import google.generativeai as genai
import random

genai.configure(api_key="GEMINI_API_KEY")


def fake_weather(city: str):
    try:
        if not city:
            return {"error": "City name is required"}
        if len(city) < 2:
            return {"error": "City name too short"}

        temp = random.randint(20, 40)
        cond = random.choice(["Sunny", "Cloudy", "Rainy", "Stormy"])

        return {"city": city, "temperature": f"{temp}°C", "condition": cond}
    except Exception as e:
        return {"error": f"Weather API failed: {str(e)}"}

def summarizer(text: str):
    try:
        if not text:
            return {"error": "Text cannot be empty"}

        # simple short summary
        summary = " ".join(text.split()[:20]) + "..."
        return {"summary": summary}

    except Exception as e:
        return {"error": f"Summarizer failed: {str(e)}"}

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",

    tools=[{
        "function_declarations": [
            {
                "name": "fake_weather",
                "description": "Simulated weather API.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string"}
                    },
                    "required": ["city"]
                }
            },
            {
                "name": "summarizer",
                "description": "Summarize long text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string"}
                    },
                    "required": ["text"]
                }
            }
        ]
    }],

    system_instruction="""
Use tools when:
- User asks for weather → call fake_weather
- User asks to summarize → call summarizer
If tool fails, explain the error.
If no tool needed, answer normally.
"""
)

def run_agent(user_input):
    response = model.generate_content(user_input)
    first = response.candidates[0].content.parts[0]

    # If Gemini calls a tool
    if hasattr(first, "function_call") and first.function_call:
        fc = first.function_call

        if fc.name == "fake_weather":
            result = fake_weather(**fc.args)
        elif fc.name == "summarizer":
            result = summarizer(**fc.args)

        follow_up = model.generate_content(
            [
                response.candidates[0].content,
                {"function_response": {"name": fc.name, "response": result}}
            ]
        )
        return follow_up.text

    # Otherwise normal answer
    return response.text

if __name__ == "__main__":
    print("\n--- Weather Test ---")
    print(run_agent("What is the weather in Hyderabad?"))

    print("\n--- Summarizer Test ---")
    print(run_agent("Summarize this: Artificial intelligence is transforming industries..."))

    print("\n--- Normal Question ---")
    print(run_agent("Who invented electricity?"))

