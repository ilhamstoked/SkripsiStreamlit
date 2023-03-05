import streamlit as st
import numpy as np
import tensorflow as tf
from tcp_latency import measure_latency

# Measure Latency
latency = measure_latency(host='35.201.127.49', port=443)

# Load TensorFlow Lite model
interpreter = tf.lite.Interpreter(model_path="InceptionResNetV2Skripsi.tflite")
interpreter.allocate_tensors()

# Get input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Define a function to resize the input image
def resize_image(image):
    # Resize the image to 150x150 pixels
    resized_image = tf.image.resize(image, [150, 150])
    return resized_image.numpy()

# Define a function to run inference on the TensorFlow Lite model
def classify_image(image):
    # Pre-process the input image
    resized_image = resize_image(image)
    input_data = np.expand_dims(resized_image, axis=0).astype(np.float32)
    interpreter.set_tensor(input_details[0]['index'], input_data)

    # Run inference
    with st.spinner('Classifying...'):
        interpreter.invoke()

    # Get the output probabilities
    output_data = interpreter.get_tensor(output_details[0]['index'])
    return output_data[0]

# Define the labels for the 7 classes
labels = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'nv', 'vasc']

from PIL import Image
# Define the main Streamlit app
def main():
    st.title("Skin Cancer Classification")

    st.write("Please note that this model still has room for academic revision as it can only classify the following 7 classes")
    st.text("'akiec' - squamous cell carcinoma (actinic keratoses dan intraepithelial carcinoma),")
    st.text("'bcc' - basal cell carcinoma, 'bkl' - benign keratosis (serborrheic keratosis),")
    st.text("'df' - dermatofibroma, 'nv' - melanocytic nevi, 'mel' - melanoma,")
    st.text("'vasc' - vascular skin lesions (Cherry Angiomas, Angiokeratomas, Pyogenic Granulomas.")
    st.write("Due to imperfection of the model and a room of improvement for the future, if the probabilities shown are less than 70%, the skin is either healthy or the input image is unclear. This means that the model can be the first diagnostic of your skin illness. As precautions for your skin illness, it is better to do consultation with dermatologist. ")
    st.write(latency[0])
    
    # Get the input image from the user
    image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    # Show the input image
    if image is not None:
        image = np.array(Image.open(image))
        st.image(image, width=150)

        # Run inference on the input image
        probs = classify_image(image)

        # Display the top 3 predictions
        top_3_indices = np.argsort(probs)[::-1][:3]
        st.write("Top 3 predictions:")
        for i in range(3):
            st.write("%d. %s (%.2f%%)" % (i + 1, labels[top_3_indices[i]], probs[top_3_indices[i]] * 100))

if __name__ == '__main__':
    main()
