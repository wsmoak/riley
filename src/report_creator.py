# Looks for PDF export of the model along with
# the entities, attributes, and relationships CSV files
# and produces a report with the model diagram
# plus all of the entities and attributes sorted alphabetically
class ReportCreator:

  def perform(account, model_name, date):
      print( f"called report method with {account}, {model_name}, and {date}")

