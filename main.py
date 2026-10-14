import os
import json
from google import genai

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

def generate_content():
    models = client.models.list()

    available_model = None

    for model in models:
        name = model.name

        if (
            "flash" in name.lower()
            and "generateContent"
            in getattr(model, "supported_actions", [])
        ):
            available_model = name
            break

    if not available_model:
        raise RuntimeError(
            "No compatible Flash model found. "
            "Check available models in Google AI Studio."
        )

    prompt = """
    Create one original Minecraft What-If YouTube Short
    for a USA audience.

    Topic: What if gravity disappeared for 5 seconds?

    Return valid JSON with:
    idea, title, script, description, scenes.

    Create three detailed video-generation prompts.
    Make the story exciting, original, and suitable
    for a general audience.
    """

    response = client.models.generate_content(
        model=available_model,
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        text = text.rsplit("```", 1)[0].strip()

    result = json.loads(text)

    os.makedirs("output", exist_ok=True)

    with open(
        "output/video_plan.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            result,
            file,
            indent=2,
            ensure_ascii=False
        )

    print("Video plan generated successfully!")
    print("Model:", available_model)
    print("Title:", result["title"])

if __name__ == "__main__":
    generate_content()
