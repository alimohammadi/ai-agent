import os
from dotenv import load_dotenv
from google import genai




def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    # for m in client.models.list():
    #     print(m.name)

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    )

    print(response.text)

    if response is None or response.usage_metadata is None:
        print("Response is malformed")
        return
    else:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


main()