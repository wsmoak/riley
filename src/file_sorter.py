import csv
import pandas as pd

# Sorts the entities, attributes, and relationships files so that
# they can be committed to the code repository to see differences.
# the order of lines within the export csv file may change.
class FileSorter:

    def __init__(self,account,model,date):
        self.account = account
        self.model = model
        self.date = date
        self.entities_filename = self.filename("entities")
        self.attributes_filename = self.filename("attributes")
        self.relationships_filename = self.filename("relationships")

    def perform(self):
        entities_df = pd.read_csv(self.entities_filename, sep=';')
        entities_df.sort_values('Label', inplace=True)
        entities_df.to_csv(self.entities_filename, index=False, sep=';', quoting=csv.QUOTE_ALL)

        attributes_df = pd.read_csv(self.attributes_filename, sep=';')
        attributes_df.sort_values(['Entity label', 'Attribute label'], inplace=True)
        attributes_df.to_csv(self.attributes_filename, index=False, sep=';', quoting=csv.QUOTE_ALL)

        relationships_df = pd.read_csv(self.relationships_filename, sep=';')
        relationships_df.sort_values(['Source entity label', 'Target entity label'], inplace=True)
        relationships_df.to_csv(self.relationships_filename, index=False, sep=';', quoting=csv.QUOTE_ALL)
        print("Success!")

    def filename(self,item):
        filename = f"{self.account}-{self.model}-{item}"
        if self.date:
            filename += f"-{self.date}"
        filename += ".csv"
        return filename





