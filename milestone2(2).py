import google.generativeai as genai
import random

# Configure Gemini API
genai.configure(api_key="GEMINI_API_KEY")


def calculator(expression: str):
    try:
        return {"result": str(eval(expression))}
    except Exception as e:
        return {"error": f"Invalid expression: {str(e)}"}

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
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",

    tools=[{
        "function_declarations": [
            {
                "name": "calculator",
                "description": "Solve mathematical expressions.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {"type": "string"}
                    },
                    "required": ["expression"]
                }
            },
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
            }
        ]
    }],

    system_instruction="""
Use tools when:
- User asks math → use calculator
- User asks weather → use fake_weather
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

        if fc.name == "calculator":
            result = calculator(**fc.args)
        elif fc.name == "fake_weather":
            result = fake_weather(**fc.args)

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
    print("\n--- Calculator Test ---")
    print(run_agent("What is 89 * 67?"))

    print("\n--- Weather Test ---")
    print(run_agent("What is the weather in Chennai?"))

    print("\n--- Normal Question ---")
    print(run_agent("Who discovered gravity?"))

    print("\n--- Error Case Test ---")
    print(run_agent("Weather in X?"))
