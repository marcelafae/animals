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

#https://animal-api-gzsqtwobpa-lz.a.run.app/predict?age_upon_intake_y=0.08333333333333333&animal_type=Dog&intake_condition=Normal&breed=Common&sex=0&sex_type=0&color=Black

@app.get("/predict")
def predict(age_upon_intake_y: float,
            animal_type: str,
            breed: str,
            intake_condition: str,
            sex: str,
            sex_type: str): #I removed 'color: str' but should I???

    """"    possivelmente é o que tem q acompanhar a linha 8 pra faster predictions
    prediction = app.state.model.predict(input_data)
    return {"prediction": prediction}
    """

    X_pred = pd.DataFrame.from_dict({
        "age_upon_intake_(years)": [age_upon_intake_y],
        "animal_type": [animal_type],
        "breed": [breed],
        "intake_condition": [intake_condition],
        "sex": [sex],
        "sex_type": [sex_type]
    })
    #for now, color is being ignore until pipeline is correct
    X_pred[['beige', 'black', 'brown',
       'gray', 'orange', 'point', 'smoke', 'spotted', 'striped',
       'tricolor', 'white']] = [1,0,0,0,0,0,0,0,0,0,0]

    print(X_pred)

    file = open('./Animal_Adoption/api/pipeline_best_model.pkl','rb')
    pipeline = pickle.load(file)
    print(pipeline.feature_names_in_)
    # assert model is not None
    y_pred = pipeline.predict(X_pred)
    return {'days_in_shelter':float(y_pred)}

@app.get("/")
def root():
    return {'I say jump': 'How high?'}



#------------------------------------------ code for when there's 2 models

    # if animal_type == "Dog":
    #     X_pred = pd.DataFrame.from_dict({
    #         "age_upon_intake_(years)": [age_upon_intake_y],
    #         "animal_type": [animal_type],
    #         "breed": [breed],
    #         "intake_condition": [intake_condition],
    #         "sex": [sex],
    #         "sex_type": [sex_type]
    #     })
    #     #for now, color is being ignore until pipeline is correct
    #     X_pred[['beige', 'black', 'brown',
    #     'gray', 'orange', 'point', 'smoke', 'spotted', 'striped',
    #     'tricolor', 'white']] = [1,0,0,0,0,0,0,0,0,0,0]

    #     print(X_pred)

    #     file = open('./Animal_Adoption/api/pipeline_best_model.pkl','rb')
    #     pipeline = pickle.load(file)
    #     print(pipeline.feature_names_in_)
    #     # assert model is not None
    #     y_pred = pipeline.predict(X_pred)
    #     return {'days_in_shelter':float(y_pred)}
    # else:
