import os
import base64
import requests

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv


# Load .env
load_dotenv()

API_KEY = os.getenv("FOUNDRY_API_KEY")
PROJECT_ENDPOINT = os.getenv("FOUNDRY_PROJECT_ENDPOINT")

AGENT_NAME = "ProductQualityInspector"
AGENT_VERSION = "3"


# Flask
app = Flask(__name__, template_folder="template")


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Product inspection
@app.route("/api/inspect", methods=["POST"])
def inspect_product():

    # Check image
    if "image" not in request.files:
        return jsonify({
            "success": False,
            "error": "No image selected."
        }), 400

    image = request.files["image"]

    if image.filename == "":
        return jsonify({
            "success": False,
            "error": "Please select an image."
        }), 400

    try:

        # Read image
        image_bytes = image.read()

        # Convert image to Base64
        encoded_image = base64.b64encode(image_bytes).decode("utf-8")

        content_type = image.content_type or "image/jpeg"

        image_url = f"data:{content_type};base64,{encoded_image}"


        # Correct Foundry Responses API endpoint
        url = (
            PROJECT_ENDPOINT.rstrip("/")
            + "/openai/v1/responses"
        )


        headers = {
            "api-key": API_KEY,
            "Content-Type": "application/json"
        }


        # Send image to ProductQualityInspector v3
        payload = {

            "input": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "Inspect this product image for visible quality defects."
                        },
                        {
                            "type": "input_image",
                            "image_url": image_url
                        }
                    ]
                }
            ],

            "agent_reference": {
                "name": AGENT_NAME,
                "type": "agent_reference",
                "version": AGENT_VERSION
            }
        }


        print("Sending image to Microsoft Foundry...")


        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=120
        )


        print("Foundry status:", response.status_code)


        # API error
        if response.status_code != 200:

            print(response.text)

            return jsonify({
                "success": False,
                "error": "Foundry API error",
                "details": response.text
            }), response.status_code


        # Get response
        data = response.json()


        # Extract output
        result = extract_text(data)


        return jsonify({
            "success": True,
            "result": result
        })


    except requests.exceptions.Timeout:

        return jsonify({
            "success": False,
            "error": "Microsoft Foundry request timed out."
        }), 504


    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500



def extract_text(data):

    # Direct output_text
    if data.get("output_text"):
        return data["output_text"]


    # Search output
    output = data.get("output", [])

    result = []


    for item in output:

        content = item.get("content", [])

        for part in content:

            if part.get("type") == "output_text":

                if part.get("text"):
                    result.append(part["text"])


    if result:
        return "\n".join(result)


    return "No inspection result was returned."


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )