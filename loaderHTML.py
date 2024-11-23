import sys

sys.path.append(r"C:\Users\temp\Desktop\gen-ai-business-case-recruiting-nov-2024_versão_final")

from src.ingestion.loaders.loaderBase import LoaderBase
import logging
from bs4 import BeautifulSoup

class LoaderHTML(LoaderBase):

    def __init__(self,filepath:str):
        self.filepath=filepath
        
    def get_soup(self, page_content: str):
        return BeautifulSoup(page_content, "html.parser")
    
    def extract_metadata(self, page_content: str):
        soup = self.get_soup(page_content=page_content)
        try:
            meta_tag = soup.find('meta')
            if not meta_tag:
                raise Exception("No metadata found!")
            
            return {
                'metadata': meta_tag.get_text()
            }
        except Exception as e:
            logging.error(e)
            return None
    
    def extract_text(self):

        try:
            text_content: str = ""
            with open(self.filepath, "r", encoding="utf-8") as html_file:
                text_content = html_file.read()

            if len(text_content) == 0:
                raise Exception("Error reading HTML file!")

            soup = self.get_soup(text_content)
            html_content = soup.get_text()
            if len(html_content) == 0:
                raise Exception("Error reading HTML file!")
            
            return html_content
        except Exception as e:
            logging.error(e)
            return None