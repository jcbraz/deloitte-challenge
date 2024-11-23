from src.ingestion.loaders.loaderBase import LoaderBase
import pandas as pd
import os 
import time


class LoaderCSV(LoaderBase):

    def __init__(self,filepath:str):
        self.filepath=filepath
    
    def extract_text(self):
        df = pd.read_csv(self.filepath)
        
        # Create a list to store the concatenated strings for each row
        row_texts = []
        
        # Iterate through each row in the DataFrame
        for index, row in df.iterrows():
            row_text = ""
            for column in df.columns:
                # Concatenate the column name and its corresponding value
                row_text += f"{column}: ({row[column]}) "
            
            # Append the concatenated string for this row to the list
            row_texts.append(row_text.strip())  # Use .strip() to remove trailing space
        
        return row_texts
    
    def extract_metadata(self):
        # Read the CSV file
        df = pd.read_csv(self.filepath)

        # Get basic metadata
        metadata = {
            "file_name": os.path.basename(self.filepath),
            "file_size": os.path.getsize(self.filepath),  # Size in bytes
            "creation_time": time.ctime(os.path.getctime(self.filepath)),
            "last_modified_time": time.ctime(os.path.getmtime(self.filepath)),
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": df.columns.tolist(),
            "column_data_types": df.dtypes.to_dict(),  # Data types of each column
            "null_values": df.isnull().sum().to_dict()  # Null value count for each column
        }
        
        return metadata