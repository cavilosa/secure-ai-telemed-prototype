import spacy


class NNPModel():
    def __inti__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def find_pii_in_output(self, text:str):
        pass

    def is_pii_extraction_attempt(self, text:str):
        pass