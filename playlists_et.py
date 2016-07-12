import xml.etree.ElementTree as ET
import sys
import os
import shutil
import urllib2
import logging

logging.basicConfig(filename='PlaylistExport.log',level=logging.DEBUG)

#Kde vytvorit slozku?
export_root_path = "/Users/maara/Desktop/"
#Nazev slozky
export_top_dir = "Rekordbox_Export"
#Cesta k Rekodbox XML
xml_file = "/Users/maara/Documents/rb_test.xml"
#Kopirovat nebo nekopirovat? (1 ANO, 0 NE)
removed_before_flight = 1
#Cislovat tracky ve slozce?
enable_track_counter = 1

#Sem nehrabat!
current_directory = ""
export_dir = export_root_path+export_top_dir
track_counter = 0


def get_playlists(xml_root):
	for playlist_all in xml_root.iter('PLAYLISTS'):
		for node in playlist_all.iter('NODE'):
			playlist_type = node.attrib['Type']
			if int(playlist_type) == 0:
				playlist_dir_name = node.attrib['Name']
				print('Directory :' + node.attrib['Name'])
				global current_directory
				current_directory = playlist_dir_name
				print('Current DIR: ' + current_directory)
				track_counter = 0
				print('Counter reset!')
			elif int(playlist_type) == 1:
				track_counter = 0
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
	global enable_track_counter
	if removed_before_flight == 0:
		logging.info('ONLY PRINTING')
		logging.debug('Track number: ' + str(counter))
		logging.debug('Track file: ' + file)
		logging.debug('Copy from: ' + source + delimiter + file)
		logging.debug('Destination dir: ' + destination)
		print('Track number: ' + str(counter))
		print('Track file: ' + file)
		print('Copy from: ' + source + delimiter + file)
		print('Destination dir: ' + destination)
		if enable_track_counter == 1:
			final_filename = destination + delimiter + str(counter) + "_" + file
			print('Copy to: ' + final_filename )
			logging.debug('Copy to: %s', final_filename )
		else:
			final_filename = destination + delimiter + file
			print('Copy to: ' + final_filename)
			logging.debug('Copy to: %s', final_filename )
	elif removed_before_flight == 1:
		logging.info('WRITING FILES')
		logging.debug('Track number: ' + str(counter))
		logging.debug('Track file: ' + file)
		logging.debug('Copy from: ' + source + delimiter + file)
		logging.debug('Destination dir: ' + destination)
		print('Track number: ' + str(counter))
		print('Track file: ' + file)
		print('Copy from: ' + source + delimiter + file)
		print('Destination dir: ' + destination)
		if enable_track_counter == 1:
			try:
				final_source = source + delimiter + file
				final_filename = destination + delimiter + str(counter) + "_" + file
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
	get_playlists(open_rb_export())

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


if __name__ == "__main__":
	main()



