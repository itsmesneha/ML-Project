import os
import sys
from src.logger import logging

from src.exception import CustomException
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass # type: ignore

## Step1: Create path variables to store the files are raw csv
@dataclass
class DataIngestionconfig:
    train_data_path:str=os.path.join('artifacts','train.csv')
    test_data_path:str=os.path.join('artifacts','test.csv')
    raw_data_path:str=os.path.join('artifacts','raw.csv')

## create a class for Data Ingestion
class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionconfig()

    def initiate_data_ingestion(self):
        logging.info('Data Ingestion methods Starts')
        try:
            # Check and log the path where the artifacts folder will be created
            artifacts_folder_path = os.path.dirname(self.ingestion_config.raw_data_path)
            logging.info('Artifacts folder path: %s', artifacts_folder_path)

            # Create the parent directories if they do not exist
            logging.info('Creating parent directories...')
            os.makedirs(artifacts_folder_path, exist_ok=True)
            logging.info('Parent directories created successfully.')

            df=pd.read_csv(os.path.join('Notebooks\Data','gemstone.csv'))
            logging.info('Dataset read as pandas Dataframe')

            df.to_csv(self.ingestion_config.raw_data_path,index=False)
            logging.info('Raw data saved')

            logging.info('Train test split')
            train_set,test_set=train_test_split(df,test_size=0.30,random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info('Ingestion of Data is completed')

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
  
        except Exception as e:
            logging.error('Exception occurred during Data Ingestion: %s', e)
            raise CustomException(e, sys)
