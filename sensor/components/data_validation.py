from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from sensor.entity.config_entity import DataValidationConfig
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import read_yaml_file
import os, sys
import pandas as pd

class DataValidation:


    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                        data_validation_config:DataValidationConfig):

        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e, sys) from e


    @staticmethod
    def read_data(file_path)-> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e, sys) from e

    def detect_datadrift(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys) from e

    def is_numerical_column_exist(self, dataframe:pd.DataFrame) -> bool:
        try:
            numerical_columns=self._schema_config['numerical_columns']
            dataframe_columns = dataframe.columns

            numerical_columns_present = True
            missing_numerical_columns =[]
            for num_column in numerical_columns:
                if num_column not in dataframe_columns:
                    numerical_columns_present=False
                    missing_numerical_columns.append(num_column)


            logging.info(f"Missing Numerical columns : [{missing_numerical_columns}]")
            return numerical_columns_present



        except Exception as e:
            raise SensorException(e, sys) from e

    def validate_number_of_column(self, dataframe:pd.DataFrame)-> bool:
        try:
            number_of_columns=self._schema_config['columns']

            if len(dataframe.columns)== number_of_columns:
                logging.info("validation of Number of Columns is Successfully Done")
                return True
            logging.info("validation of Number of Columns is Failed")
            return False

        except Exception as e:
            raise SensorException(e, sys) from e

    def initiate_data_validation(self)-> DataValidationArtifact:
        try:
            error_message= ""
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.trained_file_path
            train_dataframe=DataValidation.read_data(train_file_path)
            test_dataframe=DataValidation.read_data(test_file_path)

            # validatte number of columns

            status=self.validate_number_of_column(dataframe=train_dataframe)
            if not status:
                error_message=f"{error_message}Train dataframe does not contain all columns.\n"
            status=self.validate_number_of_column(dataframe=test_dataframe)
            if not status:
                error_message=f"{error_message}Test dataframe does not contain all columns.\n"

            # validate numerical columns

            status = self.is_numerical_column_exist(dataframe=train_dataframe)
            if not status:
                error_message=f"{error_message}Train dataframe does not contain all numerical columns.\n"

            status = self.is_numerical_column_exist(dataframe=test_dataframe)
            if not status:
                error_message=f"{error_message}Test dataframe does not contain all numerical columns.\n"

            if len(error_message)>0:

                raise Exception(error_message)

            ### data drift 


        except Exception as e:
            raise SensorException(e, sys) from e




