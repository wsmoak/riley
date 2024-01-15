# Looks for PDF export of the model along with
# the entities, attributes, and relationships CSV files
# and produces a report with the model diagram
# plus all of the entities and attributes sorted alphabetically

import pandas as pd

class ReportCreator:

    def perform(account, model_name, date):

        entities_filename = f"{account}-{model_name}-entities-{date}.csv"
        entities_df = pd.read_csv(entities_filename, sep=';')
        entities_df.sort_values('Label', inplace=True)

        attributes_filename = f"{account}-{model_name}-attributes-{date}.csv"
        attributes_df = pd.read_csv(attributes_filename, sep=';')
        attributes_df.sort_values(['Entity label', 'Attribute label'], inplace=True)

        for _index, row in entities_df.iterrows():
            entity_label = row['Label']
            description = row['Description']
            print(f"Entity label: {entity_label}, Description: {description}")
            filtered_attributes_df = attributes_df.loc[attributes_df['Entity label'] == entity_label]
            for _index, row in filtered_attributes_df.iterrows():
                print(f"     Entity label: {row['Entity label']}, Attribute label: {row['Attribute label']}")

