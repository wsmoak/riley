from report_creator import ReportCreator
from file_sorter import FileSorter
import argparse

parser = argparse.ArgumentParser(prog='riley')
parser.add_argument("command", choices=["report","sort"], help="report: produce a pdf report of the model, entities, and attributes. sort: sort the csv files so git diff is useful")
parser.add_argument('-a', '--account', help="your Ellie.ai account name, the prefix of the export files")
parser.add_argument('-m', '--model', help="the name of your Ellie model, with dashes instead of spaces, to construct the filenames")
parser.add_argument('-d', '--date', default="", help="the date in YYYY-MM-DD format, to construct the filenames")
args = parser.parse_args()

if args.command == "report":
    ReportCreator.perform(args.account, args.model, args.date)

if args.command =="sort":
    FileSorter(args.account, args.model, args.date).perform()
