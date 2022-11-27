from io import BytesIO
from zipfile import ZipFile
import pandas as pd
import requests
import os
import glob

path = os.getcwd()


def download_data():
    url = "https://files.grouplens.org/datasets/movielens/ml-25m.zip"
    content = requests.get(url)
    zf = ZipFile(BytesIO(content.content))

    for s in zf.namelist():
        if ".csv" in s:
            df = pd.read_csv(zf.open(s), low_memory=False)
            file_name = s.split("/")[1]
            df.to_csv(path + '/' + file_name, index=False)

    print('Download Complete.')


def show_files():
    csv_files = glob.glob(os.path.join(path, "*.csv"))
    for f in csv_files:
        print('File Name:', f.split("\\")[-1])


def filter_by_movie_id(movie_id: int, output: str = 'json'):
    file_name = 'tags.csv'
    df = pd.read_csv(path + '/' + file_name)
    df = df[df['movieId'] == movie_id]

    filter_list = ['tag', 'movieId']
    df = df.loc[:, df.columns.isin(filter_list)]

    if output == 'json':
        df.to_json(f'movie_id_{movie_id}.json')
    elif output == 'csv':
        df.to_csv(f'movie_id_{movie_id}.csv')

    return df


def filter_by_rating(rating_value: float, user_id: int = None, movie_id: int = None, output: str = 'csv'):
    file_name = 'ratings.csv'
    df = pd.read_csv(path + '/' + file_name)
    df = df[df['rating'] == rating_value]

    filter_list = ['rating', 'userId', 'movieId']
    df = df.loc[:, df.columns.isin(filter_list)]

    if user_id and movie_id:
        df = df[(df['userId'] == user_id) & (df['movieId'] == movie_id)]
    elif user_id:
        df = df[(df['userId'] == user_id)]
    elif movie_id:
        df = df[(df['movieId'] == movie_id)]

    if output == 'json':
        df.to_json(f'rating_{rating_value}.json')
    elif output == 'csv':
        df.to_csv(f'rating_{rating_value}.csv')

    return df


def filter_rows(genre: str = None, year: int = None, movie_id: int = None, output: str = 'csv'):
    file_name = 'movies.csv'
    df = pd.read_csv(path + '/' + file_name)

    # if genre:
    #     df = df[df['genres'] == genre]
    # elif year:
    #     df = df[df['title'].str.contains(str(year))]
    # elif movie_id:
    #     df = df[df['movieId'] == movie_id]

    if genre and year:
        df = df[(df['genres'] == genre) & (df['title'].str.contains(str(year)))]
    elif genre:
        df = df[df['genres'] == genre]
    elif year:
        df = df[df['title'].str.contains(str(year))]
    elif movie_id:
        df = df[df['movieId'] == movie_id]

    if output == 'json':
        df.to_json(f'genre_{genre}.json')
    elif output == 'csv':
        df.to_csv(f'genre_{genre}.csv')

    return df


if __name__ == '__main__':
    # print(filter_by_movie_id(216))
    # print(filter_by_rating(5, 296, 527))
    # print(filter_rows("Adventure", 1995, 1))
    # print(filter_rows(year=1995))
    print(filter_rows("Adventure", year=1995))