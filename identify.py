
import tensorflow as tf
import json
import pathlib
from settings import IDENTIFCATION_PATH, INFECTION_MODEL_PATH, IS_INFECTED_MODEL_PATH, PLANT_MODEL_PATH
IMAGE_SHAPE = (224, 224)

label_lookups = {}
decease_remedies = {}
with open("image_labels.json","r") as fp:
  label_lookups = json.load(fp)

with open("disease.json","r") as fp:
  decease_remedies = json.load(fp)

def load_plant_model():
  model = tf.keras.models.load_model(PLANT_MODEL_PATH)
  print("#########PLANT Model Loaded ######")
  return model

def load_infection_model():
  model = tf.keras.models.load_model(INFECTION_MODEL_PATH)
  print("#########INFECTION Model Loaded ######")
  return model

def load_is_infected_model():
  model = tf.keras.models.load_model(IS_INFECTED_MODEL_PATH)
  print("#########IS INFECTED Model Loaded ######")
  return model

plant_model,infection_model,is_infected_model = load_plant_model(),load_infection_model(),load_is_infected_model()

def prepare_input_data():
  data_dir = pathlib.Path(IDENTIFCATION_PATH)
  image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1/255)
  image_data = image_generator.flow_from_directory(str(data_dir), target_size=IMAGE_SHAPE)
  return image_data
# print(image_data)

def return_image_batch(image_data):
  for image_batch, label_batch in image_data:
    print("Image batch shape: ", image_batch.shape)
    print("Label batch shape: ", label_batch.shape)
    break
  return image_batch

def predict_from_model(image_batch):
  plant_index =plant_model.predict(image_batch).argmax(axis=-1)[0]
  plant_name = label_lookups['plant'][str(plant_index)].replace("_"," ")
  is_infected_index =is_infected_model.predict(image_batch).argmax(axis=-1)[0]
  health_status = "Healthy"
  remedy = ["Keep your plant enough ventileted and moist and inspect it regualarly."]
  if is_infected_index == 0:
    infection_index = infection_model.predict(image_batch).argmax(axis=-1)[0]
    health_status = "Infected with {}".format(label_lookups['infection'][str(infection_index)].replace("_"," "))
    remedy = decease_remedies[label_lookups['infection'][str(infection_index)]]
  # print(result_batch)
  # index = result_batch.argmax(axis=-1)[0]
  return plant_name,health_status,remedy



# image_data = prepare_input_data()
# image_batch = return_image_batch(image_data)
# plant_name = predict_from_model(image_batch)
# print(plant_name)
# print("PLANT NAME: ", plant_name)
# print("PLANT HEALTH:", decease_name)
# if "healthy" not in decease_name:
#   print("Below are treatment you can take")
#   print("\n".join(remedies))


