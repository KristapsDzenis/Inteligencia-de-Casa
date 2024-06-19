''' NO need to run this code. 
    This is just an example. 
    No images have been inserted to train the model
'''

import cv2
import random
import string
import boto3 as AmazonAPI

def detect_milk_level(image):
    # The computer vision images needs to be placed here to detect the milk level
    return milk_level

def generate_random_api_key(length=20):
    #Generate a random API key
    characters = string.ascii_letters + string.digits
    api_key = ''.join(random.choice(characters) for _ in range(length))
    return api_key

# Example usage
api_key = generate_random_api_key()
secret_key = generate_random_api_key()
associate_tag = generate_random_api_key(5)

def make_amazon_purchase():
    # Implement your logic to interact with the Amazon API and make a purchase
    # Make sure to handle authentication and authorization properly
    amazon_api = AmazonAPI(api_key, secret_key, associate_tag)
    
    # Example: Purchase the milk (adjust product details accordingly)
    product_id = 'B00EXAMPLE'  # Replace with the actual product ID
    quantity = 1
    amazon_api.purchase_product(product_id, quantity)


# Open the camera
cap = cv2.VideoCapture(0)

while True:
    # Capture a frame from the camera
    ret, frame = cap.read()

    # Perform milk level detection
    milk_level = detect_milk_level(frame)

    # Display the milk level on the screen
    cv2.putText(frame, f'Milk Level: {milk_level}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Milk Level Detector', frame)

    # If almost empty, make an Amazon purchase
    if milk_level == 'almost empty':
        make_amazon_purchase()
        print("Milk is almost empty. Making a purchase on Amazon.")

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the OpenCV window
cap.release()
cv2.destroyAllWindows()

