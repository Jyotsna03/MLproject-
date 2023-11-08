from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer 
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
import os
import sys

# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Append the project's base directory to the Python path
project_base_dir = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.append(project_base_dir)

from src import *
from src.pipeline.utils import save_object

from src.pipeline.exception import CustomException
import logging 

from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_path =os.path.join(os.getcwd(),"logs",LOG_FILE)
os.makedirs(logs_path,exist_ok=True)

LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

logging.basicConfig(
    filename = LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s -%(message)s",
    level= logging.INFO,

)
if __name__== "__main__":
    logging.info("Logging has started")

class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join("artifacts","preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            numerical_columns = ["writing_score","reading_score"]
            categorical_columns=[
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            num_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                ])
            cat_pipeline= Pipeline(
                steps=[(
                    "imputer",SimpleImputer(strategy="most_frequent"),
                    ("one_hot_encoder",OneHotEncoder()),
                    ("scaler",StandardScaler())
                )]

            )

            logging.info("Numerical columns standard scaling completed")

            logging.info(" Categorical columns encoding completed")

            preprocessor=ColumnTransformer(
                [(
                    "num_pipeline",num_pipeline,numerical_columns),
                    ("cat_pipelines",cat_pipeline,categorical_columns)
                ]



            )

            return preprocessor




            
        except Exception as e:
            raise CustomException((sys,e))
            

    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df = pd.read_scv(train_path)
            test_df =pd.read_csv(test_path)

            logging.info("read train and test data")
            logging.info("obtaining preprocessing object")

            preprocessing_obj = self.get_data_transformer_object()

            target_column_name = "math_score"
            numerical_columns = ["writing_score","reading_score"]

            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)

            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info(f"applying preprocessing object on training dataframe and testing dataframe ")

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)

            input_feature_test_arr= preprocessing_obj.fit_transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr,np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr,np.array(target_feature_test_df)]

            logging.info(f"saved processing object. ")

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,obj=preprocessing_obj
            )

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
                                                   


        except Exception as e:
            raise CustomException(e,sys)
