from movie import Movie

class Watchlist:
    def __init__(self):
        self.watchlist = []

    def add_to_watchlist(self, movie):
        self.watchlist.append(movie)
        print("Film izleme listesine eklendi!")

    def remove_from_watchlist(self, movie):
        if movie in self.watchlist:
            self.watchlist.remove(movie)
            print("Film izleme listesinden kaldırıldı!")
