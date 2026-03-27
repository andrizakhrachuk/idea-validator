import json
import os
import sys
from typing import Dict, Any
from dotenv import load_dotenv
from openai import OpenAI

class IdeaStructurer:
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4.1-mini",
        temperature: float = 0.3,
        max_tokens: int = 800
    ):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def structure_idea(self, idea_text: str) -> Dict[str, Any]:
        prompt = f"""
        Convert the following business idea into a structured JSON.

        Idea:
        {idea_text}

        Return ONLY valid JSON in the following format:
        {{
            "problem": "",
            "solution": "",
            "existing_alternatives": "",
            "assumptions": [],
            "risks": []
        }}
        """

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a startup analyst."},
                {"role": "user", "content": prompt}
            ],
        )

        content = response.choices[0].message.content.strip()

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            print("Invalid JSON returned by model:")
            print(content)
            return {}

def run() -> None:
    load_dotenv()
    if len(sys.argv) > 1:
        idea = " ".join(sys.argv[1:])
    else:
        idea = input("Enter your business idea: ")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    structurer = IdeaStructurer(
        api_key=api_key,
        model="gpt-4.1-mini",
        temperature=0.2
    )

    result = structurer.structure_idea(idea)
    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    run()