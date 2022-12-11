from flask import Flask
from utils import get_movie_by_title, get_movie_by_year, get_movie_by_rating
from flask import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


# вьюшка для маршрута /movie/<title> , которая выводит данные про фильм
@app.get('/movie/<title>')
def api_movie_page(title):
    data = get_movie_by_title(title)
    return app.response_class(
        response=json.dumps(data,
                            ensure_ascii=False,
                            indent=4),
        status=200,
        mimetype="application/json"
    )


# вьюшка для маршрута /movie/year/to/year, которая выводит список словарей
@app.get('/movie/<int:year1>/to/<int:year2>')
def api_movie_year_page(year1, year2):
    data = get_movie_by_year(year1, year2)
    return app.response_class(
        response=json.dumps(data,
                            ensure_ascii=False,
                            indent=4),
        status=200,
        mimetype="application/json"
    )


# вьюшка, которая обрабатывает несколько маршрутов в соответствии с рейтингом
@app.get("/rating/<rating>")
def api_movie_rating_page(rating):
    data = get_movie_by_rating(rating)
    return app.response_class(
        response=json.dumps(data,
                            ensure_ascii=False,
                            indent=4),
        status=200,
        mimetype="application/json"
    )


# вьюшка /genre/<genre> которая возвращает список 10 самых свежих фильмов
@app.get("/genre/<genre>")
def api_movie_genre(genre):
    data = get_movie_by_rating(genre)
    return app.response_class(
        response=json.dumps(data,
                            ensure_ascii=False,
                            indent=4),
        status=200,
        mimetype="application/json"
    )


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)