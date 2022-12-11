import sqlite3
import json


# подключение к БД
def get_data_from_db(sql):
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        result = cursor.execute(sql).fetchall()
        return result


# функция, которая принимает title и возвращает данные в формате словаря
def get_movie_by_title(movie_title):
    sql = f"""  SELECT title, country, release_year, listed_in, description 
                FROM netflix 
                WHERE title LIKE {movie_title}
                ORDER BY release_year desc
                LIMIT 1 """
    result = get_data_from_db(sql)
    for item in result:
        return dict(item)


# функция, которая принимает два года и возвращает бы данные в формате списка словарей
def get_movie_by_year(year1, year2):
    sql = f"""  SELECT title, release_year 
                FROM netflix 
                WHERE release_year BETWEEN {year1} AND {year2}
                LIMIT 100
                """
    result = get_data_from_db(sql)
    data = []
    for item in result:
        data.append(dict(item))
    return data


# функция, которая принимает список допустимых рейтингов и возвращает данные в формате списка словарей
def get_movie_by_rating(rating):
    data = {
        "children": ("G", "PG"),
        "family": ("G", "PG", "PG-13"),
        "adult": ("R", "NC-17")
    }
    sql = f"""  SELECT title, rating, description
                FROM netflix 
                WHERE rating IN {data.get(rating, ("G", "PG"))}
                """
    data = get_data_from_db(sql)
    result = []
    for item in data:
        result.append(dict(item))
    return result


# функция, которая получает название жанра в качестве аргумента и возвращает 10 самых свежих фильмов в формате json
def get_movie_by_genre(genre):
    sql = f"""      SELECT title, description
                    FROM netflix 
                    WHERE listed_in like '%{str(genre)[1:]}%'
                    ORDER BY release_year desc
                    LIMIT 10
                    """
    data = get_data_from_db(sql)
    result = []
    for item in data:
        result.append(dict(item))
    return result


# функция, которая получает в качестве аргумента имена двух актеров
def get_movie_by_cast(name1, name2):
    sql = f"""  SELECT "cast" 
                FROM netflix
                WHERE "cast" LIKE "%{name1}%" 
                AND "cast" LIKE "%{name2}%"
                """
    data = get_data_from_db(sql)

# сохраняет всех актеров из колонки cast
    result = []
    names_dict = {}
    for item in data:
        names = set(dict(item).get("cast").split(", ")) - set([name1, name2])
        for name in names:
            names_dict[name.strip()] = names_dict.get(name.strip(), 0) + 1

# возвращает список тех, кто играет с ними в паре больше 2 раз
    for key, value in names_dict.items():
        if value > 2:
            result.append(key)

    return result


# функция, с помощью которой можно будет передавать тип картины (фильм или сериал), год выпуска и ее жанр
# и получать на выходе список названий картин с их описаниями в JSON
def get_movie_by_qualities(movie_type, year, genre):
    sql = f"""  SELECT title, description 
                FROM netflix
                WHERE "type" = '{movie_type.title()}'
                AND release_year = '{year}'
                AND listed_in LIKE '%{str(genre)[1:]}%'
                """
    data = get_data_from_db(sql)
    result = []
    for item in data:
        result.append(dict(item))
    return json.dumps(result,
                      ensure_ascii=False,
                      indent=4)



