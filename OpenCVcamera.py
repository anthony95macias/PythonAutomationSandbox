import cv2
import numpy as np
import tensorflow as tf

# Load a pre-trained MobileNetV2 model
model = tf.keras.applications.MobileNetV2(weights="imagenet")

# Function to process each frame and check for human face
def process_frame(frame):
    resized_frame = cv2.resize(frame, (224, 224))
    input_frame = tf.keras.applications.mobilenet_v2.preprocess_input(resized_frame)
    predictions = model.predict(np.expand_dims(input_frame, axis=0))
    
    # Get the index and confidence of the top prediction
    top_index = np.argmax(predictions)
    confidence = predictions[0][top_index]
    
    # Note: 837 is not necessarily the class index for humans in MobileNetV2
    is_human = top_index == 837
    
    return is_human, confidence

# Initialize webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open camera.")
else:
    print("Camera is successfully opened.")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Check if frame is captured successfully
    if not ret:
        print("Failed to grab frame")
        break
    
    # Process the frame to detect humans
    is_human, confidence = process_frame(frame)
    
    # Label the frame based on detection
    label = f"Human Detected: {confidence:.2f}" if is_human else "No Human"
    cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Draw a bounding box around the face if a human is detected
    if is_human:
        height, width, _ = frame.shape
        cv2.rectangle(frame, (width//4, height//4), (3*width//4, 3*height//4), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Human Detection', frame)

    # Press 'q' to quit the application
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
