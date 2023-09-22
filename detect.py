import cv2
import imutils
import easyocr

# Load the original image
image_path = 'images/7.jpg'
original_img = cv2.imread(image_path)

# Resize the original image for better processing speed
original_img = imutils.resize(original_img, width=500)

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])

# Perform text detection and recognition
results = reader.readtext(original_img)

# Initialize variables to store recognized text and number plate region
recognized_text = ""
number_plate_region = None

# Loop through the results to find the number plate
for (bbox, text, prob) in results:
    (top_left, top_right, bottom_right, bottom_left) = bbox
    (x1, y1) = map(int, top_left)  # Cast to integers
    (x2, y2) = map(int, bottom_right)  # Cast to integers

    # Filter regions that are likely to be the number plate
    if len(text) >= 5 and prob >= 0.5:
        number_plate_region = original_img[y1:y2, x1:x2]
        recognized_text = text

# Display the original image
cv2.imshow("Original Image", original_img)

# If a number plate region is found, display it and print the recognized text
if number_plate_region is not None:
    cv2.imshow("Number Plate", number_plate_region)
    print("Recognized Text:", recognized_text)
else:
    print("Number plate not found in the image.")

# Wait for a key press and close OpenCV windows
cv2.waitKey(0)
cv2.destroyAllWindows()