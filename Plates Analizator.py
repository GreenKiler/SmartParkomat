import os
import time
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

# Set the environment variables using os.environ
os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY'] = '36482fdvPI1YFLBNB85GUHTHokmGOPTm0OfXerMs0kzuKkdhAWUqJQQJ99ALAC5RqLJXJ3w3AAAFACOGkYUg'
os.environ['COMPUTER_VISION_ENDPOINT'] = 'https://image-analizator.cognitiveservices.azure.com/'

# Read the environment variables using os.environ
subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
endpoint = os.environ['COMPUTER_VISION_ENDPOINT']

# subscription_key = '96a5175a532f4c7e876c576e00cbc3fe'
# endpoint = 'https://vehiclenp.cognitiveservices.azure.com/'
credentials = CognitiveServicesCredentials(subscription_key)
client = ComputerVisionClient(endpoint, credentials)
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# Load the image to extract text from
image_url = "https://tablica-rejestracyjna.pl/images/photos/20181201110703_1.jpg"

# Call the OCR method on the image
read_response = computervision_client.read(image_url, raw=True)

# Get the operation location (URL with an ID at the end) from the response
read_operation_location = read_response.headers["Operation-Location"]

# Grab the ID from the URL
operation_id = read_operation_location.split("/")[-1]

# Call the "GET" API and wait for it to retrieve the results
while True:
    read_result = computervision_client.get_read_result(operation_id)
    if read_result.status not in ['notStarted', 'running']:
        break
    time.sleep(1)

# Print the detected text and bounding box for each line
if read_result.status == OperationStatusCodes.succeeded:
    for text_result in read_result.analyze_result.read_results:
        for line in text_result.lines:
            # Check if the line contains a license plate number
            if any(char.isdigit() for char in line.text) and any(char.isalpha() for char in line.text):
                # Print the license plate number and bounding box
                print("License plate number:", line.text)
                # Exit the loop if a license plate number is found
                break
        print()

# End of code
print("End of Computer Vision quickstart.")