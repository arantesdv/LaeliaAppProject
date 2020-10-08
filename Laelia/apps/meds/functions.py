import csv

with open('/Users/danielarantes/LaeliaAppProject/static/cd-drug-presentation.csv') as presentations:
	dict = csv.DictReader(presentations)
	for row in dict:
		print(f'{row}')