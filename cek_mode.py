from tensorflow.keras.models import load_model

model = load_model("model/model_regresi.keras")

print(model.output_shape)