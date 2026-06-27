from tensorflow.keras.models import load_model
import numpy as np
from preprocess import preprocess_image

MODEL_PATH = "model/model_final.keras"

model = load_model(MODEL_PATH)


CLASS_NAMES = [

    "Drone",

    "Non Drone"

]


def predict_image(img_path):

    img = preprocess_image(img_path)

    prediction = model.predict(img, verbose=0)

    if prediction.shape[1] == 2:

        index = np.argmax(prediction)

        confidence = float(prediction[0][index])

        status = CLASS_NAMES[index]

    else:

        value = float(prediction[0][0])

        if value > 0.5:

            status = "Non Drone"

            confidence = value

        else:

            status = "Drone"

            confidence = 1 - value

    result = {

        "status": status,

        "confidence": round(confidence * 100, 2),

        "distance": "-"

    }

    return result