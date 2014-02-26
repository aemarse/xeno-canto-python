from urllib2 import Request, build_opener, HTTPError, URLError, urlopen
import simplejson

# Global variables
BASE_URL = "http://xeno-canto.org/api/recordings.php?query="
NUM_R = "numRecordings"
NUM_SP = "numSpecies"
PG = "page"
NUM_PG = "numPages"
RECS = "recordings"

# Class that contains all params and methods for querying the db
class XenoCantoObject:
	
	# Initialize some empty parameters
	def __init__(self):
		self.name = ""
		self.tags = {
			"gen"	: "",
			"rec"	: "",
			"cnt"	: "",
			"loc"	: "",
			"rmk"	: "",
			"lat"	: "",
			"lon"	: "",
			"box"	: "",
			"also"	: "",
			"type"	: "",
			"nr"	: "",
			"lic"	: "",
			"q"		: "",
			"q<"	: "",
			"q>"	: "",
			"area"	: "",
			"since"	: "",
			"year"	: "",
			"month" : "",
		}
		self.query_url = ""

	# Sets the "name" parameter
	def setName(self, name):
		self.name = name;

	# Sets a "tag" parameter
	def setTag(self, key, val):
		self.tags[key] = val

	# Makes a query url from the "name" and "tag"
	def makeUrl(self):
		name_url = self.name

		tag_url = ""
		for key, value in self.tags.iteritems():
			if value != "":
				tag_url += "%20" + key + ":\"" + value + "\""

		self.query_url = BASE_URL + name_url + tag_url
		print self.query_url

	# Performs HTTP GET request, returns JSON object
	def get(self):
		try:
			request = Request(self.query_url)
		except HTTPError as e:
			print e.code
			print e.read
		except URLError as e:
			print 'We failed to reach a server.'
			print 'Reason: ', e.readon
		else:
			opener = build_opener()
			f = opener.open(request)
			json_obj = simplejson.load(f)
			return json_obj

	# Decodes JSON object into its components and sets them as class variables
	def decode(self, json):
		self.num_recs = json[NUM_R]
		self.num_sp = json[NUM_SP]
		self.page = json[PG]
		self.num_pages = json[NUM_PG]
		self.recs = json[RECS]

	# Downloads all audio files in the 'recs' class variable
	def download_audio(self, audio_dir):
		for idx, rec in enumerate(self.recs):

			rec_url = rec['file']
			
			conn = urlopen(rec_url)
			file_name = audio_dir + rec['en'] + '_' + rec['id'] + '.mp3'
			f = open(file_name, 'wb')
			size = int(conn.info().getheaders("Content-Length")[0])

			block_size = 8192
			while True:
				buf = conn.read(block_size)
				
				if not buf:
					break

				f.write(buf)
				
			f.close()
			print "Wrote %d/%s" % (idx + 1, self.num_recs)
