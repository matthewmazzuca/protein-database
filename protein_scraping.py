from lxml import html
import requests
import sys
import re
import argparse
import logging

# Get arguments
parser = argparse.ArgumentParser(description='Scrape a protein page')
parser.add_argument('arg_url', metavar='R', type=str, nargs=1,  help='The protein page URL')
parser.add_argument('-f',  action='store_true', help='Force INSERT protein into database')
parser.add_argument('-d', action='store_true', help='Force DELETE protein from database')
parser.add_argument('-q', action='store_true', help='Quiet')
parser.add_argument('-v', action='store_true', help='Verbose')

args = vars(parser.parse_args())

force_insert = args['f']
force_delete = args['d']
quiet = args['q']
verbose = args['v']

protein_url = args['arg_url'][0]

# Configure logging
logging.basicConfig(filename='protein_page.log', level=(logging.INFO if not verbose else logging.DEBUG), format='%(asctime)s %(message)s')
if not quiet:
	logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logging.debug('Processing ' + protein_url + '...')

# Get page
try:
	page = requests.get(protein_url)
except Exception as err:
	logging.error('Error: ' + str(err))
	quit()
	
tree = html.fromstring(page.text)

name_span_list = tree.xpath('//*[@id="info_box"]/p[1]/span')
if len(name_span_list) == 0:
	name_span_list = tree.xpath('//*[@id="info_box"]/div[3]/p[1]/span')
	if len(name_span_list) == 0:
		name_span_list = tree.xpath('//*[@id="info_box"]/p[1]/span')
		if len(name_span_list) == 0:
			name_span_list = tree.xpath('//*[@id="info_box"]/div[3]/p[2]/span')
			if len(name_span_list) == 0:
				name_span_list = tree.xpath('//*[@id="info_box"]/p[2]/span')
				if len(name_span_list) == 0:
					print('Unsupported protein structure found at ' + protein_url)
					quit()
				else:
					p_span_list = tree.xpath('//*[@id="info_box"]/p[3]/span')
			else:
		 		p_span_list = tree.xpath('//*[@id="info_box"]/div[3]/p[3]/span')
		else:
			p_span_list = tree.xpath('//*[@id="info_box"]/div[3]/p[2]/span')
	else:
		p_span_list = tree.xpath('//*[@id="info_box"]/div[3]/p[2]/span')
else:
	p_span_list = tree.xpath('//*[@id="info_box"]/p[2]/span')

def clean_garbage(str):
	while (str[0] == ' '):
		str = str[1:]
	while (not str[-1:].isalnum()) or (str[-1:].isspace()):
		str = str[:-1]
	return str
	
def find_span_by_text(list, field_name):
	for x in list:
		if (x.text == field_name):
			return x
			#if x.tail != None and not x.tail.isspace():
			#	return clean_garbage(x.tail)
	return None
	
def find_span_by_id(list, id_name):
	for x in list:
		if id_name == x.attrib.get('id'):
			return x
	return None
	
def find_span_by_attrib(list, attrib_name):
	for x in list:
		if x.attrib.get(attrib_name):
			return x
	return None
		
name = clean_garbage(name_span_list[0].text)

span = find_span_by_text(p_span_list, 'Position:')
if span == None:
	position = 'Unknown'
else:
	position = clean_garbage(span.tail)

span = find_span_by_text(p_span_list, 'Shoots:')
if span == None:
	shot_stance = 'Unknown'
else:
	shot_stance = clean_garbage(span.tail)

span = find_span_by_text(p_span_list, 'Height:')
if span == None:
	height = 'Unknown'
else:
	height = clean_garbage(span.tail)

span = find_span_by_text(p_span_list, 'MWeight:')
if span == None:
	weight = 'Unknown'
else:
	weight = clean_garbage(span.tail)

span = find_span_by_id(p_span_list, 'necro-birth')
if span == None:
	span = find_span_by_attrib(p_span_list, 'data-birth')
	if span == None:
		span = find_span_by_text(p_span_list, 'Born:')
		if span == None:
			birthdate = 'Unknown'
		else:
			birthdate = clean_garbage(span.getnext().text)
	else:
		birthdate = span.attrib.get('data-birth')
else:
	birthdate = span.attrib.get('data-birth')

span = find_span_by_text(p_span_list, 'Authors:')
if span == None:
	college = 'Unknown'
else:
	college = clean_garbage(span.getnext().text)

span = find_span_by_text(p_span_list, 'Date added:')
if span == None:
	span = find_span_by_text(p_span_list, 'Verified: ')
	if span == None:
		debut = 'Unknown'
	else:
		debut = clean_garbage(span.tail)
else:
	debut = clean_garbage(span.getnext().text)


if height == 'Unknown':
	int_height = 0
else:
	height_numbers = list(map(int, re.findall(r'\d+', height)))
	if len(height_numbers) >= 2:
		int_height = height_numbers[0] * 12 + height_numbers[1]
	else:
		int_height = 0

if weight == 'Unknown':
	int_weight = 0
else:
	int_weight = int(re.match(r'\d+', weight).group())

int_birth_year = 0
int_birth_month = 0
int_birth_day = 0
	
if birthdate != 'Unknown':
	birthdate_numbers = list(map(int, re.findall(r'\d+', birthdate)))
	if len(birthdate_numbers) >= 1:
		int_birth_year = birthdate_numbers[0]
		if len(birthdate_numbers) >= 2:
			int_birth_month = birthdate_numbers[1]
			if len(birthdate_numbers) >= 3:
				int_birth_day = birthdate_numbers[2]

logging.info('protein ' + name)
logging.debug('---Position: ' + position)
logging.debug('---residues: ' + resideus)
logging.debug('---Height: ' + height)
logging.debug('---MWeight: ' + mweight)


logging.debug('Processed ' + protein_url)

