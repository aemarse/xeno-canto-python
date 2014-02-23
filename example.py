from xeno_canto.__init__ import *
import os

# Parameters of the query
# (see __init__.py.XenoCantoObject.tags for options)
name = "Tinamou" 	# The name of the species to search for
cnt = "Brazil" 		# Country tag
q = "A" 			# Audio recording quality tag

# Instantiate XenoCantoObject
xc_obj = XenoCantoObject()

# Set the class variables using these methods
xc_obj.setName(name)
xc_obj.setTag('cnt', cnt)
xc_obj.setTag('q', q)

# Create the query url based on the set parameters
xc_obj.makeUrl()

# Makes the HTTP GET request, returns the JSON response
json_obj = xc_obj.get()

# Sets the individual component of JSON response as class variables
xc_obj.decode(json_obj)

# Print out the class variables (JSON data)
print "numRecs    : " + xc_obj.num_recs
print "numSpecies : " + xc_obj.num_sp
print "page       : %d" % xc_obj.page
print "numPages   : %d" % xc_obj.num_pages

# Access individual recordings this way
recs = xc_obj.recs
curr = recs[0]
curr_id = curr['id']
print curr_id

# Download all audio files in the response like this
rec_dir = os.path.dirname(os.path.realpath(__file__)) + "/audio/"
xc_obj.download_audio(rec_dir)
