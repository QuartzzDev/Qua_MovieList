class Movie:
    def __init__(self, title, genre, watched=False, rating=0):
        self.title = title
        self.genre = genre
        self.watched = watched
        self.rating = rating
    
    def toggle_watched(self):
        self.watched = not self.watched
        if not self.watched:
            self.rating = 0

    def set_rating(self, rating):
        self.rating = rating