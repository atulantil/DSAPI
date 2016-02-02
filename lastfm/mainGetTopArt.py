from modules import *
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

#get the artist similarity dict:
#art_sim_dic_read=read_csv_dict('artist_sim100.csv')
#get the user top artist dict:
#user_top_art_dic = read_csv_dict('user_top_artist.csv')
#########################################for each user, get top artists (50)    
#usage: getting the top artist for each user in the user list

#call get frds and get a seed list
def main_get_top_artist():
    print "getting seed users..."
    seed=get_frds( "user.getfriends", { "user": "damarys_eira" } )
    print "creating user list of 2000...."
    user_list=traverse_data(seed)

    user_top_artist_dict={}
    all_artists=set()
    print "getting all users top artists..."
    for user in user_list:
        top_names,top_mbid=get_user_top_artists( "user.getTopArtists", { "user": user } )
        user_top_artist_dict[user]=top_names
        add_to_artist(all_artists,top_names)
    print 'finished....'
    return user_top_artist_dict,all_artists

def main_write_top_artist(path,user_top_artist_dict,limit):
    """use limit to write only consistent number of cols in a row, such as limit=50 then for each user we have 50 top artists"""
    #write user list to the csv, write only those lines where there are 50 top artists, without comma in their names
    #path="user_top_artist.csv"
    f=open(path,"w")
    f.write("")
    f.close()
    for key in user_top_artist_dict:
        if len(user_top_artist_dict[key])==limit:
            if not check_comma(user_top_artist_dict[key]):
                write_to_csv(key,user_top_artist_dict[key],path)





########################################get similar artists for all artist, now at limit=20
#get the dict of artist similarity 
#there is a unicode problem with API, so I ignored all names with non-ascii chars
#initially we're doing 100 sim artists, seems to much to handle. now limit 20
def main_get_sim_art(all_artists):
    art_sim_dict={}
    for artist in all_artists:
        a=artist.encode('ascii', 'ignore')
        if a!='':
            sim_art=get_all_sim_artists(a)
            art_sim_dict[artist]=sim_art
    return art_sim_dict

def main_write_sim_art(path,art_sim_dict,limit):
    """use limit to write only consistent number of cols in a row, such as limit=50 then for each user we have 20 sim artists"""

    #write the whole dict to file
    #path='artist_sim100.csv'
    f=open(path,"w")
    f.write("")
    f.close()
    for key in art_sim_dict:
        if len(art_sim_dict[key])==limit:
            if not check_comma(art_sim_dict[key]):
                write_to_csv(key,art_sim_dict[key],path)


def main_get_write_sim_art(path,all_artists):
    c=0
    art_sim_dict={}
    for artist in all_artists:
        c+=1

        if c%5000==0:
            print "processed:",c


        #a=artist.encode('ascii', 'ignore')
        
        #if a!='':
        sim_art=get_all_sim_artists(artist)
        write_to_csv(artist,sim_art,path)
