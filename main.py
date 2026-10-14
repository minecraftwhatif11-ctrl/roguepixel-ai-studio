import os
import json
from google import genai

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

PROMPT = """
Create one original YouTube Short for a USA gaming audience.

Topic: Minecraft What If
Concept: What if gravity disappeared for 5 seconds?

Return valid JSON with these fields:
{
  "idea": "video idea",
  "title": "short English title",
  "script": "original 30-second narration",
  "description": "YouTube description with relevant hashtags",
  "scenes": [
    "Scene 1 video generation prompt",
    "Scene 2 video generation prompt",
    "Scene 3 video generation prompt"
  ]
}

Make the story exciting, original, and suitable for a general audience.
Do not claim the video has already been generated.
"""

def generate_content():
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=PROMPT
    )

    result = json.loads(response.text)

    os.makedirs("output", exist_ok=True)

    with open("output/video_plan.json", "w",
              encoding="utf-8") as file:
        json.dump(result, file, indent=2,
                  ensure_ascii=False)

    print("Video plan generated successfully!")
    print("Title:", result["title"])

if __name__ == "__main__":
    generate_content()
