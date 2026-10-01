import json
import base64
from pathlib import Path

# Project folders
BASE_DIR = Path(__file__).parent
IMAGE_DIR = BASE_DIR / "images"

# Images we want to use for evaluation
test_images = [
    "bottle.jpg",
    "car_damage.jpg",
    "car_r.jpg",
    "phone_damage.jpg"
]

# Output JSONL file
output_file = BASE_DIR / "product_quality_evaluation.jsonl"


def get_mime_type(filename):
    extension = Path(filename).suffix.lower()

    if extension in [".jpg", ".jpeg"]:
        return "image/jpeg"
    elif extension == ".png":
        return "image/png"
    elif extension == ".webp":
        return "image/webp"
    else:
        raise ValueError(f"Unsupported image type: {extension}")


with open(output_file, "w", encoding="utf-8") as file:

    for image_name in test_images:

        image_path = IMAGE_DIR / image_name

        if not image_path.exists():
            print(f"Image not found: {image_name}")
            continue

        # Read image
        image_bytes = image_path.read_bytes()

        # Convert image to Base64
        encoded_image = base64.b64encode(image_bytes).decode("utf-8")

        mime_type = get_mime_type(image_name)

        # Create evaluation record
        record = {
            "query": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Inspect this product image and determine whether the product should PASS or FAIL."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{encoded_image}"
                            }
                        }
                    ]
                }
            ]
        }

        # Write one JSON object per line
        file.write(json.dumps(record) + "\n")

        print(f"Added: {image_name}")


print("\nEvaluation dataset created successfully!")
print(f"File: {output_file}")