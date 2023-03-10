import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle
from Animal_Adoption.preproc.transformers import ColorTransformer

app = FastAPI()
#app.state.model = your_model_library.load_model("path/to/model/file")

# Optional, good practice for dev purposes. Allow all middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# example url http://127.0.0.1:8000/predict?vgg_cat_or_dog=Cat&vgg_color=Black&vgg_breed=Sheperd&sex=Female&condition=Normal&age_animal=2&castraded=true
@app.get("/predict")
def predict(vgg_cat_or_dog: str,  # 'Cat' or 'Dog' (from vgg)
            vgg_color: str,    # 'Black' // color of the animal (from vgg)
            vgg_breed: str,     # 'Sheperd' // breed of the animal (from vgg)
            sex: str,   # 'Male' or 'Female'
            condition: str,    # 'Normal' // Condition of the animal
            age_animal: float,    # '4' // Age in years given in floats
            castraded: bool):      # 'Yes' or 'No'
    """
    Make a single prediction.
    VGG provides 3 conditions that are used as features for main model.
    User inputs the rest for the prediction.
    Results given in 'days inside the shelter'
        """
    """"    possivelmente é o que tem q acompanhar a linha 8 pra faster predictions
    prediction = app.state.model.predict(input_data)
    return {"prediction": prediction}
    """

    X_pred = pd.DataFrame(dict(
        vgg_cat_or_dog=['animal_type'],
        vgg_color=['color'],
        vgg_breed=['breed'],
        sex=['sex'],
        condition=['intake_condition'],
        age_animal=['age_upon_intake_(years)'],
        castraded=['sex_type']))
    print(X_pred)
    file = open('pipeline_best_model.pkl','rb')
    pipeline = pickle.load(file)
    # assert model is not None
    y_pred = pipeline.predict(X_pred)
    return {'days_in_shelter':float(y_pred)}

@app.get("/")
def root():
    return {'greeting': 'Hello'}
