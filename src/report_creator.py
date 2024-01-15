# Looks for PDF export of the model along with
# the CSV files for entities and attributes,
# and produces a report with the model diagram
# plus an alphabetical list of the each entity
# with its attributes shown below it.

import pandas as pd
from weasyprint import HTML, CSS
from io import BytesIO
from PyPDF2 import PdfReader, PdfMerger

class ReportCreator:

    def perform(account, model_name, date):

        entities_filename = f"{account}-{model_name}-entities"
        if date:
            entities_filename += "-{date}"
        entities_filename += ".csv"
        entities_df = pd.read_csv(entities_filename, sep=';', na_filter=False)

        attributes_filename = f"{account}-{model_name}-attributes"
        if date:
            attributes_filename += f"-{date}"
        attributes_filename += ".csv"
        attributes_df = pd.read_csv(attributes_filename, sep=';', na_filter=False)

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

        css = CSS(string="@page { size: A4 landscape; }")
        html_string = ''.join(lines)
        pdf_bytes = HTML(string=html_string).write_pdf(stylesheets=[css])
        pdf_buffer = BytesIO(pdf_bytes)

        input_filename = f"{account}-{model_name}"
        output_filename = f"{account}-{model_name}"
        if date:
          input_filename += f"-{date}"
          output_filename = f"-{date}"
        input_filename += ".pdf"
        output_filename += "-report.pdf"

        merger = PdfMerger()
        merger.append(PdfReader(input_filename))
        merger.append(pdf_buffer)
        merger.write(output_filename)
