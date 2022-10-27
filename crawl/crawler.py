import twint
import typer

def __init__():
    c = twint.Config()
    c.Store_csv = True
    c.Output = "tweets_es.csv"
    c.Lang = "es"
    # c.Translate = True
    # c.TranslateDest = "en"
    c.Since = "2020-05-01"
    c.Until = "2020-12-31"
    c.Geo = "40.4165,-3.70256,600km"
    return c

def search(c: twint.Config):
    twint.run.Search(c)


if __name__ == "__main__":
    c = __init__()
    typer.run(search(c))