from baseAPI import LastFM
import re
from collections import defaultdict
import csv, sys

def read_csv_dict(path):
    """reads in the csv file where the first col is key and rest cols are value and return the dict"""
    csv.field_size_limit(sys.maxsize)
    csv_file_object= csv.reader(open(path, 'rU'))

    dic=defaultdict(list)
    for row in csv_file_object:
        if len(row)>1:
            dic[row[0]]=row[1:]
    return dic



def check_comma(list):
    """return true if there is a comma in any string of the list"""
    for artist in list:
        if re.search("\,",artist):
            return True
    return False

#serialize the results of the art_sim_dic so far
def write_to_csv(key,value_list,path):
    """input is a key and its value, a list of strings to be written on one line of csv """
    with open(path, "a") as myfile:
        top = ",".join(value_list)
        #add key to the first column
        top = key + ","+top
        myfile.write(top.encode('utf-8'))
        #myfile.write(top)
        myfile.write('\n')




#try: get friends of a user
#note that the starter code is a class, but here I am not doing it within a class context
def get_frds(method, dict ):
    last_request = LastFM()
    friends=[]
    #find the key          
    args = {
        "method":	method,
    }
    for key in dict.keys():
      args[key] = dict[key]
    response_data = last_request.send_request( args )
    for user in response_data["friends"]["user"]:
        #print user["name"]
        friends.append(user['name'])
    return friends



def traverse_data(seed):
    all_users=seed[:]
    for user in seed:
        this_usr_friends=get_frds("user.getfriends", { "user": user } )
        all_users.extend(this_usr_friends)
        num_users=len(all_users)
        if num_users<20:
            traverse_data(this_usr_friends)
        print num_users
    return all_users
    
    
    
    
def get_user_top_artists(method, dict ):
    last_request = LastFM()
    artist_names=[]
    artist_mbid=[]
    #find the key          
    args = {
        "method":	method,
        #"limit":	10
    }
    for key in dict.keys():
      args[key] = dict[key]

    response_data = last_request.send_request( args )


    #print "~~~~~~~~~~~~~~" + str( args["method"] ) + "~~~~~~~~~~~~~~"
    #print response_data
    #print "------------------"
    #Get the first artist from the JSON response and print their name
    for art in response_data["topartists"]["artist"]:
        artist_names.append(art["name"])
        artist_mbid.append(art["mbid"])
    return artist_names,artist_mbid
    
    
def get_similar_artists(method, dict ):
    last_request = LastFM()
    artist_names=[]
    #somehow the returned similar artists for this doesn't contain mbid.
    #artist_mbid=[]
    #find the key          
    args = {
        "method":	method,
        "limit":	20
    }
    
    for key in dict.keys():
      args[key] = dict[key]
    
    
    response_data = defaultdict(lambda:None,last_request.send_request( args ))


    #print "~~~~~~~~~~~~~~" + str( args["method"] ) + "~~~~~~~~~~~~~~"
    #print response_data
    #print "------------------"
    #Get the first artist from the JSON response and print their name
    if response_data["similarartists"]:
        for art in response_data["similarartists"]["artist"]:
            #print art["name"]
            artist_names.append(art["name"])
    else:
        print "key error on response data: no similar artist for ", dict['artist']

    #artist_mbid.append(art["mbid"])
    return artist_names
    
    
    
#get all similar artists for one artist
def get_all_sim_artists(artist):
    """takes an artist as input and returns a dict with the artist name as key and a list of sim artists as value"""
    sim_arti=get_similar_artists( "artist.getSimilar", { "artist": artist } )
    #sim_dict={artist:sim_arti}
    return sim_arti
    
    
def add_to_artist(seen,data):
    """mainatin a set of unique artist in seen, by adding un-seen artists to seen from data"""
    seen.update(data)                        # add the new values to the set
    #print(seen)
    return seen
    
def compute_sim_score(artists,art_sim_dic_read):
    """give a list of 50 top artists of a user, compute the total similarity score"""
    score=0
    for art in artists:
        #if art_sim_dic_read != []:
        sim_artists=art_sim_dic_read[art]
        lar=artists[:]
        for arti in lar:
            if arti in sim_artists and arti!=art:
                score+=1
                lar.remove(arti)
                #print artists
    return score
