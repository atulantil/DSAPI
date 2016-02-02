from mainGetTopArt import *
import matplotlib.pyplot as plt

art_sim_dic_read=read_csv_dict('newSimArt3.csv')
user_top_art_dic = read_csv_dict('user_top_artist.csv')
aus=compute_all_sim_score(art_sim_dic_read,user_top_art_dic)
plt.clf()
plt.plot(sorted(aus))
plt.savefig('sort.png')
plt.clf()
plt.hist(aus,bins=100)
plt.savefig('hist.png')
