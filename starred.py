# Interface web pour les favoris et afficher le contenu (style export jekyll ?)
# export direct dans drive ?
# check starred.json existence and print usage instructions

import json
import sys
import csv

def print_usage():
	''' Prints usage instructions for the script'''
	print "Usage : starred.py csv|web."
	print "starred.json must be in the same folder as the script."


def csv_export(data):
	''' Exports data into starred.csv'''
	with open("starred.csv", "wb") as csv_file:
		csv_writer = csv.writer(csv_file)

		for item in data['items']:
			title = item['title'].encode("utf-8")
			# error handling in case canonical is not defined for the specific element
			try:
				url = item['canonical'][0]['href']
				
			except KeyError:
				url = item['alternate'][0]['href']
				
			csv_writer.writerow([title, url])

	print "Done."


def web_export(data):
	'''Exports data into a static website'''
	pass
	
	
def read_star_file():
	''' Reads starred.json file and returns data (struct)'''
	with open("starred.json") as json_data:
		data = json.load(json_data)
	return data

	
def main():
	''' Main : checks that there are arguments and prints usage if not'''
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

