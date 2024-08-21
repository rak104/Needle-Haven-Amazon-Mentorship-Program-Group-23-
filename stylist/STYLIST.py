import base64
import boto3
import json
import os

class ImageGenerator:
    def __init__(self, region_name="us-east-1", model_id="amazon.titan-image-generator-v2:0"):
        # Initialize the Bedrock Runtime client in the specified AWS Region.
        self.client = boto3.client("bedrock-runtime", region_name=region_name)
        self.model_id = model_id

    def read_image(self, image_path):
        # Read the image file and encode it in base64.
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def generate_image(self, model, item, image_path, size="medium"):
        """
        Generate an image variation based on the provided model, item, and size.

        :param model: The model description (e.g., "man", "woman").
        :param item: The item of clothing (e.g., "t-shirt", "shorts").
        :param image_path: The path to the input image.
        :param size: The size of the person (e.g., "small", "medium", "large").
        """
        # Read the input image and encode it.
        encoded_image = self.read_image(image_path)

        # Create a prompt that includes the model, item, size, and professional photo specification.
        prompt = (f"A professional photo of a {model} of {size} size wearing the {item} "
                  "in the image, with a suitable background that complements the outfit.")

        # Create the request payload.
        native_request = {
            "imageVariationParams": {
                "images": [encoded_image],
                "text": prompt
            },
            "taskType": "IMAGE_VARIATION",
            "imageGenerationConfig": {
                "cfgScale": 10,
                "seed": 0,
                "width": 1024,
                "height": 1024,
                "numberOfImages": 1
            }
        }

        # Convert the native request to JSON.
        request = json.dumps(native_request)

        # Invoke the model with the request.
        response = self.client.invoke_model(modelId=self.model_id, body=request)

        # Decode the response body.
        model_response = json.loads(response["body"].read())

        # Extract the generated image data.
        base64_image_data = model_response["images"][0]

        # Ensure the output directory exists.
        if not os.path.exists("output"):
            os.makedirs("output")

        # Determine the output file name.
        output_image_path = os.path.join("output", "output_image.jpg")

        # Decode the base64 image data and save it as a JPEG file.
        image_data = base64.b64decode(base64_image_data)
        with open(output_image_path, "wb") as file:
            file.write(image_data)

        print(f"The generated image has been saved to {output_image_path}.")
