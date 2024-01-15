# Looks for PDF export of the model along with
# the entities, attributes, and relationships CSV files
# and produces a report with the model diagram
# plus all of the entities and attributes sorted alphabetically

import pandas as pd
from weasyprint import HTML, CSS

class ReportCreator:

    def perform(account, model_name, date):

        entities_filename = f"{account}-{model_name}-entities-{date}.csv"
        entities_df = pd.read_csv(entities_filename, sep=';', na_filter=False)
        entities_df.sort_values('Label', inplace=True)

        attributes_filename = f"{account}-{model_name}-attributes-{date}.csv"
        attributes_df = pd.read_csv(attributes_filename, sep=';', na_filter=False)
        attributes_df.sort_values(['Entity label', 'Attribute label'], inplace=True)

        lines = []
        for _index, row in entities_df.iterrows():
            entity_name = row['Label']
            lines.append(f"<h1>{entity_name}</h1>")
            lines.append(f"<p>{row['Description']}</p>")
            lines.append("<hr>")

            filtered_attributes_df = attributes_df.loc[attributes_df['Entity label'] == entity_name]
            for _index, row in filtered_attributes_df.iterrows():
                label = row['Attribute label']
                format = row['Format']
                description = row['Description']
                notes = row['Notes']
                table = row['Source table']
                column = row['Source column']
                constraints = row['Constraints']
                lines.append("<p>")
                lines.append(f"{label} ({format}) {description}")
                if table and column:
                    lines.append(f" | From {column} in {table}")
                    if constraints:
                        lines.append(f" as {constraints}")
                    lines.append(".")
                if notes:
                    lines.append(f" | {notes}")
                lines.append("</p>")

        html_string = ''.join(lines)
        css = CSS(string="@page { size: A4 landscape; }")
        HTML(string=html_string).write_pdf("output.pdf", stylesheets=[css])