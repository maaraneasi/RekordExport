##Marek Pleskac 2016


import xml.etree.ElementTree as ET
import sys
import os
import shutil
import urllib2
import logging
from os.path import expanduser

#If having issues, comment the following line
logging.basicConfig(filename='PlaylistExport.log',level=logging.WARNING)
#...and uncomment this one below:
#logging.basicConfig(filename='PlaylistExport.log',level=logging.DEBUG)


#Path to the export parent dir
export_root_path = os.getenv("HOME") + "/Desktop/"
#Export directory name
export_top_dir = "Rekordbox_Export"
#Where is the Rekodbox XML?
xml_file = os.getenv("HOME") + "/Documents/rb_test.xml"
#Dry run only - if set to 0, no files are written. If set to 1, files will be copied.
removed_before_flight = 1
#Prefix track number for each playlist?
#Each copied track filename will prepended with number (01_ , 02_, 03_) to maintain playlist position
enable_track_counter = 1

#Don't touch this one.
current_directory = ""
export_dir = export_root_path+export_top_dir
track_counter = 0

def print_structure(xml_root):
	playlist_arr = []
	for elem in xml_root.iter('NODE'):
		for playlist in elem.iterfind('NODE[@Type="1"]'):
			playlist_arr.append(playlist.attrib['Name'])
	playlist_count = len(playlist_arr)
	print(str(playlist_count) + ' playlists found:')
	counter = 0
	for i in playlist_arr:
		print(str(counter) + " - " + i)
		counter = counter +1
	print("E - Return")
	playlist_selector(playlist_arr)
	return


def playlist_selector(playlist_array):
	user_choice = raw_input("Select playlist number to export: ")
	if user_choice =='E' or user_choice == 'e':
		main_menu()
	else:
		try:
			user_choice_check = int(user_choice)
			print("Playlist chosen: " + playlist_array[int(user_choice)])
			list_single_playlist(xml_file,playlist_array[int(user_choice)])
		except ValueError:
			print("Not valid playlist number")

def list_single_playlist(xml_root,playlist_name):
	print('Searching: ' + playlist_name)
	for elem in xml_root.iter('NODE'):
		for playlist in elem.iterfind('NODE[@Name="%s"]' % playlist_name):
			print('Playlist: ' + playlist.attrib['Name'])
			logging.debug('Single playlist found: %s', playlist.attrib['Name'])
			track_counter = 0
			logging.debug('Counter reset')
			playlist_path = set_playlist_path(playlist_name,current_directory)
			for playlist_track in playlist:
				print('---TRACK START---')
				track_counter = track_counter + 1
				file_name = get_track_from_collection(playlist_track.attrib['Key'])[0]
				file_current_path = get_track_from_collection(playlist_track.attrib['Key'])[1]
				copy_file(file_name,file_current_path,playlist_path,track_counter,0)
				#print('Track ID :' + get_tracks())
				#get_track_from_collection(get_tracks(playlist_track))
				print('---TRACK END---')


def add_zero(track_number):
	if track_number <= 9:
		track_number = "0" + str(track_number)
		print(int(track_counter))
		return int(track_number)
	else:
		return track_number


def get_playlists(xml_root):
	for playlist_all in xml_root.iter('PLAYLISTS'):
		for node in playlist_all.iter('NODE'):
			playlist_type = node.attrib['Type']
			if int(playlist_type) == 0:
				playlist_dir_name = node.attrib['Name']
				print('Directory :' + node.attrib['Name'])
				logging.debug('Directory: %s', node.attrib['Name'])
				global current_directory
				current_directory = playlist_dir_name
				print('Current DIR: ' + current_directory)
				logging.debug('Current DIR: %s', current_directory)
				track_counter = 0
				print('Counter reset!')
				logging.debug('Counter reset')
			elif int(playlist_type) == 1:
				track_counter = 0
				logging.debug('Counter reset')
				playlist_name = node.attrib['Name']
				print('Playlist: ' + node.attrib['Name'])
				playlist_path = set_playlist_path(playlist_name,current_directory)
				for playlist_track in node:
					print('---TRACK START---')
					track_counter = track_counter + 1
					file_name = get_track_from_collection(playlist_track.attrib['Key'])[0]
					file_current_path = get_track_from_collection(playlist_track.attrib['Key'])[1]
					copy_file(file_name,file_current_path,playlist_path,track_counter,0)
					#print('Track ID :' + get_tracks())
					#get_track_from_collection(get_tracks(playlist_track))
					print('---TRACK END---')
			else:
				print('Other: ' + node.attrib['Name'] + " " + node.attrib['Type'])

def copy_file(file,source,destination,counter,safe):
	delimiter = "/"
	counter_z = str(counter).zfill(2)
	global enable_track_counter
	if removed_before_flight == 0:
		logging.info('ONLY PRINTING')
		logging.debug('Track number: ' + str(counter_z))
		logging.debug('Track file: ' + file)
		logging.debug('Copy from: ' + source + delimiter + file)
		logging.debug('Destination dir: ' + destination)
		print('Track number: ' + str(counter_z))
		print('Track file: ' + file)
		print('Copy from: ' + source + delimiter + file)
		print('Destination dir: ' + destination)
		if enable_track_counter == 1:
			final_filename = destination + delimiter + str(counter_z) + "_" + file
			print('Copy to: ' + final_filename )
			logging.debug('Copy to: %s', final_filename )
		else:
			final_filename = destination + delimiter + file
			print('Copy to: ' + final_filename)
			logging.debug('Copy to: %s', final_filename )
	elif removed_before_flight == 1:
		logging.info('WRITING FILES')
		logging.debug('Track number: ' + str(counter_z))
		logging.debug('Track file: ' + file)
		logging.debug('Copy from: ' + source + delimiter + file)
		logging.debug('Destination dir: ' + destination)
		print('Track number: ' + str(counter_z))
		print('Track file: ' + file)
		print('Copy from: ' + source + delimiter + file)
		print('Destination dir: ' + destination)
		if enable_track_counter == 1:
			try:
				final_source = source + delimiter + file
				final_filename = destination + delimiter + str(counter_z) + "_" + file
				shutil.copy(final_source, final_filename)
				print('Copy to: ' + final_filename )
				logging.debug('Copy to: %s', final_filename )
			except IOError:
				print('IO Error')
				logging.error('IO error while writing %s', final_filename)
			else:
				logging.debug('Written OK - %s', final_filename)
		else:
			try:
				final_source = source + delimiter + file
				final_filename = destination + delimiter + file
				shutil.copy(final_source, final_filename)
				print('Copy to: ' + final_filename)
				logging.debug('Copy to: %s', final_filename )
			except IOError:
				print('IO Error')
				logging.error('IO error while writing %s', final_filename)
			else:
				logging.debug('Written OK - %s', final_filename)
	else:
		logging.error('WTF?')		
	return


def get_tracks(playlist_name):
	track_playlist_id = track.attrib['Key']
	print("Track ID _ pl :" + track_playlist_id)
	return track_playlist_id

def get_track_from_collection(trackid):
	for track in xml_file.iterfind('COLLECTION/TRACK[@TrackID="%s"]' % trackid):
		track_file = track.attrib['Location']
		track_file = track_file.replace('file://localhost','')
		track_filename_mark = track_file.rfind('/')
		track_path = urllib2.unquote(track_file[0:track_filename_mark])
		track_filename = urllib2.unquote(track_file[track_filename_mark+1:len(track_file)])
		#print('Track Location: ' + track_filename)
		#print('Track Path: ' + track_path)
		print('Track Path raw: ' + track_file)
		return (track_filename, track_path)

def set_playlist_path(playlist_name, current_directory):
	print('Playlist DIR: ' + export_dir + "/" +current_directory + "/" + playlist_name)
	path = export_dir + "/" +current_directory + "/" + playlist_name
	if not os.path.exists(path):
		print('Creating directory ' + path)
		os.makedirs(path)
	return path

def main():
	#get_playlists(open_rb_export())
	#print_structure(open_rb_export())
	#list_single_playlist(open_rb_export(),'Akropole')
	main_menu()

def open_rb_export():
	global xml_file
	if os.path.isfile(xml_file):
		logging.info('XML File found: %s', xml_file)
		xml_file = ET.parse(xml_file)
		return xml_file
	else:
		logging.critical('XML File not found in %s', xml_file)
		sys.exit()

def find_export_root(parsed_file):
	xml_root = xml_file.getroot()
	print('XML ROOT FOUND: ' + xml_root)
	logging.warning('XML ROOT FOUND: ' + xml_root)
	return xml_root	

def create_export_dir():
	global export_dir
	if not os.path.exists(export_dir):
		logging.info('Creating export directory %s', export_dir)
		os.makedirs(export_dir)

def main_menu():
	logging.debug('Waiting for user input S or A')
	user_choice = raw_input("Export [S]ingle or [A]ll playlists or [Q]uit?: ")
	if user_choice == 'S' or user_choice == 's':
		logging.debug('Main menu selection S')
		print("Selected to export single playlist.")
		print_structure(open_rb_export())
	elif user_choice == 'A' or user_choice == 'a':
		logging.debug('Main menu selection A')
		double_check = raw_input("Selected to export all playlists. Are you sure? [yes|no]:")
		if double_check == 'yes':
			get_playlists(open_rb_export())
		else:
			main_menu()
	elif user_choice == 'Q' or user_choice == 'q':
		sys.exit()
	else:
		print("%s is an invalid option")
		main_menu()


if __name__ == "__main__":
	main()



