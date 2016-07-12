import xml.etree.ElementTree as ET
import sys
import os
import shutil
import urllib2

xml_file = ET.parse("/Users/maara/Documents/rb_test2.xml")
xml_root = xml_file.getroot()

export_root_path = "/Users/maara/Desktop/"
export_top_dir = "Rekordbox_Export"
export_dir = export_root_path+export_top_dir

if not os.path.exists(export_dir):
    os.makedirs(export_dir)

for playlist_all in xml_root.iter('PLAYLISTS'):
	for playlist in playlist_all:
		for node in playlist:
			playlist_name = node.attrib['Name']
			print("---PLAYLIST: " + playlist_name)
			playlist_dir = export_dir + "/" + playlist_name
			if not os.path.exists(playlist_dir):
				os.makedirs(playlist_dir)
			for track_in_playlist in node:
				track_in_playlist_id = track_in_playlist.attrib['Key']
				print('--------ID list: ' + track_in_playlist_id)
				for track_in_collection in xml_file.iterfind('COLLECTION/TRACK[@TrackID="%s"]' % track_in_playlist_id):
					track_file = track_in_collection.attrib['Location']
					track_file = track_file.replace('file://localhost','')
					track_filename_mark = track_file.rfind('/')
					track_path = track_file[0:track_filename_mark]
					track_filename = track_file[track_filename_mark+1:len(track_file)]
					print("----------" + track_in_collection.attrib['Artist'].encode('utf-8').strip() + " - " + track_in_collection.attrib['Name'].encode('utf-8').strip())
					print("----------FULL:" + track_file)
					print("----------KUS: " + track_path)
					print("----------ZBYTEK: " + track_filename)
					#shutil.copy(urllib2.unquote(track_file), playlist_dir + "/" + urllib2.unquote(track_filename))








