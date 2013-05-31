# -*- coding: utf-8 -*-

# Interface web pour les favoris et afficher le contenu (style export jekyll ?)
# export direct dans drive ?

import json
import sys
import os.path
import csv
import datetime
from template import *
from item import *

def print_usage():
	''' Prints usage instructions for the script'''
	print "Usage : starred.py csv|web."
	print "starred.json must be in the same folder as the script."

	
def f7(seq):
	''' Function grabbed from internet to remove duplicates'''
	#http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order
	seen = set()
	seen_add = seen.add
	return [ x for x in seq if x not in seen and not seen_add(x)]

	
def csv_export(data):
	''' Exports data into starred.csv'''
	# Open csv file to write into
	with open("starred.csv", "wb") as csv_file:
		# Initiate the csv writer with specific delimiter
		csv_writer = csv.writer(csv_file, delimiter=";")

		for item in data['items']:
			#Create Item object for the specific item
			item = Item(item)
			# Write output to csv file
			csv_writer.writerow(item.genstring_csv())
	print "Done."

	
def web_export(data):
	'''Exports data into a static website'''
	# initialize renderer
	render = Render()
	# initialize item_list
	item_list = ItemList()
	# the date list will be used to regroup items in the webpage
	date_list = []
	
	for item in data['items']:
		item = Item(item)
		date_list.append(item.date)
		item_list.add(item)

	out_string = []
	# deduplicate the date list
	date_list = f7(date_list)
	
	# Iterate over all dates
	for date in date_list:
		# Insert date as a header for more readability
		out_string.append("<h2>{0}</h2></br>\n".format(date))
		# Iterate over the items that are on the same date as the current iteration
		for item in item_list.grab_date(date):
			# Generate the output string for the current item
			out_string.append(item.genstring_web())
	
	# Apply the template to the generated string
	output = render.render_index(out_string)
	# Write results
	with open("web/index.html", "w") as web_file:
		web_file.write(output)	
	print "Done."
	
def read_star_file():
	''' Reads starred.json file and returns data (struct)'''
	with open("starred.json") as json_data:
		data = json.load(json_data)
	return data

	
def main():
	''' Main : checks that there are arguments and prints usage if not'''
	
	# check for starred.json presence
	if os.path.isfile("starred.json"):
		pass
	else:
		print_usage()
		exit(0)
	
	# check for the parameters
	try:
		script, action = sys.argv
		
		data = read_star_file()
		
		if action == "csv":
			csv_export(data)
		elif action == "web":
			web_export(data)
		else:
			print_usage()
	except ValueError:
		print_usage()


main()

