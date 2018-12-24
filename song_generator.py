from pages import *


get_lyrs = GetLyricsPage('Get Lyrics', 'l', [])
gen_song = MarkovPage('Generate Song', 'g', [])
get_art  = GetArtistPage('Get Artist', 'a', [gen_song])
home_pg  = Page('Home', 'h', [get_lyrs, get_art, gen_song])
home_pg.show_options()
