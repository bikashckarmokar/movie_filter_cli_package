import typer

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

    if genre:
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


app = typer.Typer()


@app.command()
def downloaddata():
    download_data()
    print('Download Complete.')


@app.command()
def showfiles():
    show_files()


@app.command()
def filtermovie(movieid: int, output: str = typer.Argument("csv")):
    result = filter_by_movie_id(movieid, output)

    print(result)


@app.command()
def filterrating(ratingvalue: float,
           userid: int = typer.Argument(None),
           movieid: int = typer.Argument(None),
           output: str = typer.Argument("csv")
           ):
    result = filter_by_rating(ratingvalue, userid, movieid, output)

    print(result)


@app.command()
def filterrows(genre: str = typer.Argument(None),
                year: int = typer.Argument(None),
                movieid: int = typer.Argument(None),
                output: str = typer.Argument("csv")
               ):
    result = filter_rows(genre, year, movieid, output)

    print(result)


if __name__ == "__main__":
    app()
