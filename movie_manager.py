from movie import Movie

class MovieManager:
    def __init__(self):
        self.movies = []
        self.load_from_file()

    def load_from_file(self):
        try:
            with open("movie_list.txt", "r") as f:
                for line in f.readlines():
                    title, genre, status, rating = line.strip().split("|")
                    watched = (status == "watched")
                    movie = Movie(title, genre, watched, int(rating) if rating else None)
                    self.movies.append(movie)
        except FileNotFoundError:
            pass

    def save_to_file(self):
        with open("movie_list.txt", "w") as f:
            for movie in self.movies:
                status = "watched" if movie.watched else "unwatched"
                rating = str(movie.rating) if movie.rating is not None else "0"
                f.write(f"{movie.title}|{movie.genre}|{status}|{rating}\n")

    def add_movie(self, title, genre):
        new_movie = Movie(title, genre)
        self.movies.append(new_movie)
        self.save_to_file()

    def delete_movie(self, index):
        if 0 <= index < len(self.movies):
            del self.movies[index]
            self.save_to_file()

    def toggle_watched(self, index):
        if 0 <= index < len(self.movies):
            self.movies[index].toggle_watched()
            self.save_to_file()
