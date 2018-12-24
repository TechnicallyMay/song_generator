import get_lyrics
from markov import MarkovChain

class Page():
    def __init__(self, name, key, to):
        #Name of page
        self.name = name
        #Which key leads to this page
        self.key = key
        #A list of options of where the page can go to
        self.to = to
        #Where the page came from, set by other page objects
        self.back = None

    def show_options(self):
        for p in self.to:
            print("Press '%s' for %s" % (p.key.upper(), p.name))

        if self.back != None:
            print("Press 'B' to return to %s" % self.back.name)

        if 'prompt' in dir(self):
            print("Press 'F' to %s" % self.name)

        self.get_page_input()

    def get_page_input(self):
        print()
        #All keys that lead to an option
        options = [key for page in self.to for key in page.key]
        choice  = input().lower()

        if choice == 'b' and self.back != None:
            self.go_back()

        elif choice == 'f' and 'prompt' in dir(self):
            self.prompt()
            self.show_options()

        for i in range(len(options)):
            if choice == options[i]:
                self.to[i].back = self
                self.to[i].show_options()
                self.back = None
                break
        else:
            print('Invalid choice, try again')
            self.show_options()

    def go_back(self):
        self.back.show_options()

class GetLyricsPage(Page):
    def __init__(self, name, key, to):
        super().__init__(name, key, to)

    def prompt(self):
        print()
        artist = input('Which artist? ')
        song   = input('Which song? ')
        print()
        print(get_lyrics.get_song(song, artist))
        print()

class GetArtistPage(Page):
    def __init__(self, name, key, to):
        super().__init__(name, key, to)

    def prompt(self):
        print()
        artist = input('Which artist? ')
        print()
        all_lyrics = get_lyrics.get_all_songs(artist)
        for song, lyrics in all_lyrics.items():
            print(song + '-')
            print(lyrics)
            print()

class MarkovPage(Page):
    def __init__(self, name, key, to):
        super().__init__(name, key, to)
        self.new_chain()

    def prompt(self):
        print()
        prompting = True
        while prompting:
            artist = input('Which artist would you like to generate from? ')
            self.add_artist(artist)
            choice = input('Would you like to add another artist? (Y/N) ').lower()
            if choice == 'y':
                continue
            elif choice == 'n':
                prompting = False
                continue
            else:
                print('Invalid choice')
        self.options()

    def options(self):
        choice = input("Would you like to generate lyrics (G), clear artists (C), add new artists (A), or go back (B)? ").lower()

        if choice == 'g':
            self.gen_song()
        elif choice == 'c':
            self.new_chain()
            print("Cleared!")
            self.options()
        elif choice == 'a':
            self.prompt()
        elif choice == 'b':
            self.go_back()
        else:
            print("Invalid choice")
            self.options()

    def add_artist(self, artist):
        lyrics = get_lyrics.get_all_songs(artist)
        for song in lyrics.values():
            self.mc.add_string(song)
        print()
        print("Lyrics added!")

    def gen_song(self):
        new_song = " ".join(self.mc.generate_text())
        print()
        print(new_song)
        print()
        self.options()

    def new_chain(self):
        self.mc = MarkovChain()
