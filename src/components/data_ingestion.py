import os
import sys

# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Append the project's base directory to the Python path
project_base_dir = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.append(project_base_dir)
import os
os.environ['NUMEXPR_MAX_THREADS'] = '4'
os.environ['NUMEXPR_NUM_THREADS'] = '2'
import numexpr as ne 

from src import *
from src.pipeline.exception import CustomException

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig
import sys
from pathlib import Path

import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    train_data_path: str= os.path.join('artifacts',"train.csv")
    test_data_path: str= os.path.join('artifacts',"test.csv")
    raw_data_path: str= os.path.join('artifacts',"data.csv")


class DataIngestion:
    def __init__(self) -> None:
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("enter data ingestion method or component")

        try:
            df=pd.read_csv('C:\\Users\\jyojy\\OneDrive\\Desktop\\MLproject\\notebook\\data\\StudentsPerformance.csv') 
            
            logging.info('read the datatset as df') 

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True) 

            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            logging.info("Train test split start")
            train_set,test_set = train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)

            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            logging.info("Ingestion of data is completed")

            return(

                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )



        except Exception as e:
        # Raise a custom exception
         raise CustomException("Custom exception message", e, type(e))


    #data_transformation=DataTransformation()
    #data_transformation.initiate_data_transformation(train_data,test_data)


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
    obj = DataIngestion()
    obj.initiate_data_ingestion
    logging.info("Logging has started")                     