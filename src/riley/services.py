import csv
from inflection import underscore
from io import BytesIO
import pandas as pd
from PyPDF2 import PdfReader, PdfMerger
from weasyprint import HTML, CSS

# Sorts the entities, attributes, and relationships files so that
# they can be committed to the code repository to see differences.
# the order of lines within the export csv file may change.
class FileSorter:

    def __init__(self, model, date):
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
        filename = f"{self.model}_{item}"
        if self.date:
            filename += f"_{self.date}"
        filename += ".csv"
        return filename





# Looks for PDF export of the model along with
# the CSV files for entities and attributes,
# and produces a report with the model diagram
# plus an alphabetical list of the each entity
# with its attributes shown below it.


class ReportCreator:

    def perform(model_name, date, filter_attributes_by_model):

        entities_filename = f"{model_name}_entities"
        if date:
            entities_filename += f"_{date}"
        entities_filename += ".csv"
        entities_df = pd.read_csv(entities_filename, sep=';', na_filter=False)

        attributes_filename = f"{model_name}_attributes"
        if date:
            attributes_filename += f"_{date}"
        attributes_filename += ".csv"
        attributes_df = pd.read_csv(attributes_filename, sep=';', na_filter=False)

        lines = []
        for _index, row in entities_df.iterrows():
            entity_name = row['Label']
            examples = row['Examples']
            synonyms = row['Synonyms']
            lines.append(f"<h1>{entity_name}</h1>")
            lines.append(f"<p>{row['Description']}</p>")
            if examples:
                lines.append(f"<p>Examples: {examples}</p>")
            if synonyms:
                lines.append(f"<p>Synonyms: {synonyms}</p>")
            lines.append("<hr>")

            filtered_attributes_df = attributes_df.loc[attributes_df['Entity label'] == entity_name]
            if filter_attributes_by_model:
                filtered_attributes_df = filtered_attributes_df.loc[attributes_df["Notes"].str.contains(underscore(model_name))]

            for _index, row in filtered_attributes_df.iterrows():
                label = row['Attribute label']
                format = row['Format']
                description = row['Description']
                note_parts = [part.strip() for part in row['Notes'].split('|') if part.strip().startswith('Note:')]
                note_part = note_parts[0].replace("Note: ", "") if note_parts else None
                table = row['Source table']
                column = row['Source column']
                constraints = row['Constraints']
                lines.append("<p>")
                lines.append(f"{label}")
                if format:
                    lines.append(f" ({format}) ")
                if not format and description:
                    lines.append(" - ")
                lines.append(f"{description}")
                if table and column:
                    lines.append(f" | From {column} in {table}")
                    if constraints:
                        lines.append(f" as {constraints}")
                    lines.append(".")
                if note_part:
                    lines.append(f" | {note_part}")
                lines.append("</p>")

        css = CSS(string="@page { size: A4 landscape; }")
        html_string = ''.join(lines)
        pdf_bytes = HTML(string=html_string).write_pdf(stylesheets=[css])
        pdf_buffer = BytesIO(pdf_bytes)

        input_filename = output_filename = f"{model_name}"
        if date:
          input_filename += f"_{date}"
          output_filename += f"_{date}"
        input_filename += ".pdf"
        output_filename += "-report.pdf"

        merger = PdfMerger()
        merger.append(PdfReader(input_filename))
        merger.append(pdf_buffer)
        merger.write(output_filename)
        print("Success!")
