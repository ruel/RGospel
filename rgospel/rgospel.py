#!/usr/bin/python

'''
	rgospel.py
	Copyright (c) 2011 Ruel Pagayon <http://ruel.me>

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
	
'''

from xml.dom.minidom import parseString
import os
import datetime
import urllib2

class RGospelTZ:
	'''
		Class for getting the current date
		based on the timezone of the country
		of the visitor's IP
		
		Note that you must supply your ipinfodb.com
		API Key. It's free, and you just have to
		register.
	'''
	
	apiKey = 'NULL'
	
	def __init__(self, api):
		'''
			Constructor: API Key
			must be passed
		'''
		self.apiKey = api
		
	def getCurrentDate(self, ipAddress):
		'''
			Returns a tuple containing the current
			year, month (numeric), and date.
			
			IP Address is a required parameter
		'''
		
		# Fetch the xml data containing the timezone
		xdata = urllib2.urlopen('http://api.ipinfodb.com/v2/ip_query.php?key=%s&ip=%s&timezone=true' % (self.apiKey, ipAddress)).read()
		xdom = parseString(xdata)
		status = xdom.getElementsByTagName('Status')[0].firstChild.data
		
		# Check to see if the result is successful
		if status != 'OK':
			raise Exception('Request Not Valid: %s' % status)
			exit(-1)
			
		# Get the GMT offset in seconds
		try:
			gmtoffset = xdom.getElementsByTagName('Gmtoffset')[0].firstChild.data
		except:
			gmtoffset = 0
		
		# Add the offset to the current UTC time
		utctime = datetime.datetime.utcnow()
		iptime = utctime + datetime.timedelta(0, int(gmtoffset))
		
		# Return the year, month and date
		return iptime.year, iptime.month, iptime.day
		

class RGospel:
	'''
		This class parses the gospel file database.
		This is the main class of this module.
		The default date is based on the current UTC Time.
		The passage contains the bible verse(s) and the
		passage itself in HTML format.
	'''
	
	# Date when the class is created.
	_year 	= 2011
	_month 	= 2
	_day 	= 10
	passage = ''

	def __init__(self):
		'''
			Constructor. Sets the date to the current
			UTC time.
		'''
		utctime = datetime.datetime.utcnow()
		self._year = utctime.year
		self._month = utctime.month
		self._day = utctime.day
	
	def changeDate(self, cYear, cMonth, cDay):
		'''
			Changes the current date variables
		'''
		self._year = cYear
		self._month = cMonth
		self._day = cDay
		
	def getPassage(self):
		'''
			Private Function*
			Gets the passage of the current date
		'''
		
		# Open the file and split the lines
		ghandle = open('%s.txt' % self._year, 'r')
		content = ghandle.read().split('\n')
		
		# Loop through each line
		for line in content:
			if line == '':
				# Skip if the line is empty
				continue
			
			# Remove whitespaces
			line = line.strip()
			
			# Split the data (separated by a pipe '|')
			gId, gMn, gMonth, gDay, gYear, gPassage = line.split('|', 6)
			# Check for the passage of the given date
			if (int(gYear) == self._year) and (int(gMn) == self._month) and (int(gDay) == self._day):
				self.passage = gPassage
				break
		
