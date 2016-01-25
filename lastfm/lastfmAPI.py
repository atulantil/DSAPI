#
# http://www.last.fm/api/show/geo.getTopTracks
#
from pprint import pprint
import urllib, urllib2
import inspect
try:
    import json
except ImportError:
    import simplejson as json

class LastFM:
    def __init__(self ):
        self.API_URL = "http://ws.audioscrobbler.com/2.0/"
        self.API_KEY = "57ee3318536b23ee81d6b27e36997cde"
    
    def send_request(self, args, **kwargs):
        #Request specific args
        kwargs.update( args )
        #Global args
        kwargs.update({
          "api_key":  self.API_KEY,
          "format":   "json"
        })
        try:
            #Create an API Request
            url = self.API_URL + "?" + urllib.urlencode(kwargs)
            print "url:", url
            #Send Request and Collect it
            data = urllib2.urlopen( url )
            #Print it
            response_data = json.load( data )
            #Close connection
            data.close()
            return response_data
        except urllib2.HTTPError, e:
            print "HTTP error: %d" % e.code
        except urllib2.URLError, e:
            print "Network error: %s" % e.reason.args[1]

    def get_top_artists(self, method, dict ):
        #find the key          
        args = {
            "method":	method,
            "limit":	10
        }
        for key in dict.keys():
          args[key] = dict[key]
          print "----------------------------------"
          print key, dict[key]
        
        response_data = self.send_request( args )
        #print response_data
        
        print "~~~~~~~~~~~~~~" + str( args["method"] ) + "~~~~~~~~~~~~~~"
        
        #Get the first artist from the JSON response and print their name
        for artist in response_data["topartists"]["artist"]:
          print artist["name"]
        
    def get_top_tags(self, method, dict ):
        #find the key          
        args = {
            "method":	method,
            "limit":	10
        }
        for key in dict.keys():
          args[key] = dict[key]
          print "----------------------------------"
          print key, dict[key]
        
        response_data = self.send_request( args )
        #print response_data
        
        print "~~~~~~~~~~~~~~" + str( args["method"] ) + "~~~~~~~~~~~~~~"
        
        #Get the first artist from the JSON response and print their name
        for artist in response_data["toptags"]["tag"]:
          print artist["name"]    
        
        
    def get_hyped_artists(self, method ):
      args = {
          "method":	method,
          "limit":	3
      }
      response_data = self.send_request( args )
      print "~~~~~~~~~~~~~~" + str( args["method"] ) +"~~~~~~~~~~~~~~"
      #Get the first artist from the JSON response and print their name
      for artist in response_data["artists"]["artist"]:
        print artist["name"]
        
    def get_similar_tracks(self, method, dict ):
      args = {
          "method":	method,
          "limit":	10
      }
      for key in dict.keys():
        args[key] = dict[key]
        print "----------------------------------"
        print key, dict[key]
        
      response_data = self.send_request( args )
      print "~~~~~~~~~~~~~~" + str( args["method"] ) +"~~~~~~~~~~~~~~"
      #Get the first artist from the JSON response and print their name

      for artist in response_data["similartracks"]["track"]:
        print artist["name"], artist["artist"]["name"]

def main():
    last_request = LastFM()
    last_request.get_top_artists( "tag.gettopartists", { "tag": "classical" } )
    last_request.get_top_artists( "geo.gettopartists", { "country": "United States" } )
    last_request.get_top_tags( "artist.gettoptags", { "artist": "Glenn Gould" } )
    #last_request.get_hyped_artists( "chart.getHypedArtists" )
    last_request.get_similar_tracks( "track.getsimilar", {
                                    "track": "Ray of Light",
                                    "artist": "Madonna"})

if __name__ == "__main__": main()