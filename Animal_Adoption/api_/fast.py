import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

# example url http://127.0.0.1:8000/predict?vgg_cat_or_dog='Cat'&vgg_color='Black'&vgg_breed='Sheperd'&sex='Female'&condition='Normal'&age_animal=2&castraded='Yes'
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
        sex=['sex_animal'],
        condition=['condition_animal'],
        age_animal=['age_animal'],
        castraded=['castraded']))

    y_pred = 12

 #   model = load_model()  // this is where I will load the model
    # assert model is not None

    # X_processed = preprocess_features(X_pred)
    # y_pred = model.predict(X_processed)
    return {'days_in_shelter':float(y_pred)}

@app.get("/")
def root():
    return {'greeting': 'Hello'}
