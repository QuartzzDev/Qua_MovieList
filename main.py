import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QDialog, QRadioButton, QButtonGroup, QDialogButtonBox
from movie_manager import MovieManager

class RateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Filmi Puanlama")
        self.setGeometry(200, 200, 300, 200)

        self.radio_buttons = []
        self.button_group = QButtonGroup()

        layout = QVBoxLayout()

        self.label = QLabel("Filmi Ne Kadar Beğendiniz ?")
        layout.addWidget(self.label)

        for i in range(1, 6):
            radio_button = QRadioButton(str(i))
            layout.addWidget(radio_button)
            self.radio_buttons.append(radio_button)
            self.button_group.addButton(radio_button)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def get_selected_rating(self):
        for i, radio_button in enumerate(self.radio_buttons):
            if radio_button.isChecked():
                return i + 1

        return None

class MovieListApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.movie_manager = MovieManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Qua Film İzleme Listesi")
        self.setGeometry(100, 100, 400, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.movie_list_widget = QListWidget()
        self.movie_list_widget.itemDoubleClicked.connect(self.toggle_watched_status)
        self.layout.addWidget(self.movie_list_widget)

        self.title_input = QLineEdit()
        self.genre_input = QLineEdit()

        self.add_button = QPushButton("Film Ekle")
        self.add_button.clicked.connect(self.add_movie)

        self.delete_button = QPushButton("Film Sil")
        self.delete_button.clicked.connect(self.delete_movie)

        self.rate_button = QPushButton("Filmi Puanla")
        self.rate_button.clicked.connect(self.rate_movie)

        self.layout.addWidget(QLabel("Filmin Adı:"))
        self.layout.addWidget(self.title_input)
        self.layout.addWidget(QLabel("Filmin Türü:"))
        self.layout.addWidget(self.genre_input)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.rate_button)

        self.central_widget.setLayout(self.layout)

        self.load_movies()

    def load_movies(self):
        self.movie_list_widget.clear()
        for movie in self.movie_manager.movies:
            status = "İzlenmedi" if not movie.watched else "İzlendi"
            self.movie_list_widget.addItem(f"{movie.title} - {movie.genre} ({status})")

    def add_movie(self):
        title = self.title_input.text()
        genre = self.genre_input.text()
        if title and genre:
            self.movie_manager.add_movie(title, genre)
            self.title_input.clear()
            self.genre_input.clear()
            self.save_to_file()
            self.load_movies()

    def delete_movie(self):
        selected_items = self.movie_list_widget.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            index = self.movie_list_widget.indexFromItem(selected_item).row()
            self.movie_manager.delete_movie(index)
            self.save_to_file()
            self.load_movies()

    def rate_movie(self):
        selected_items = self.movie_list_widget.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            index = self.movie_list_widget.indexFromItem(selected_item).row()

            if not self.movie_manager.movies[index].watched:
                QMessageBox.warning(self, "QuaDev - Hata", "Film izlenmediği için puanlama yapılamaz.")
                return

            rate_dialog = RateDialog(self)
            if rate_dialog.exec_() == QDialog.Accepted:
                rating = rate_dialog.get_selected_rating()
                if rating is not None:
                    self.movie_manager.movies[index].rating = rating
                    self.save_to_file()
                    self.load_movies()

    def toggle_watched_status(self, item):
        index = self.movie_list_widget.indexFromItem(item).row()
        self.movie_manager.toggle_watched(index)
        self.save_to_file()
        self.load_movies()

    def save_to_file(self):
        with open("movie_list.txt", "w") as f:
            for movie in self.movie_manager.movies:
                status = "watched" if movie.watched else "unwatched"
                f.write(f"{movie.title}|{movie.genre}|{status}|{movie.rating}\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MovieListApp()
    window.show()
    sys.exit(app.exec_())
