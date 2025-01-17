# import "packages" from flask
from flask import Flask, render_template
from flask import request
from __init__ import app
import requests, random
import json

from crud.app_crud_api import app_crud_api
app.register_blueprint(app_crud_api)

from templates.danielcreate import comparisonInput

# create a Flask instance
# app = Flask(__name__)
from crud.app_crud import app_crud
app.register_blueprint(app_crud)



from templates.nathanreem import nathanreem
app.register_blueprint(nathanreem)

from templates.snakegame import snakegame
app.register_blueprint(snakegame)


from templates.jacob import jacob
app.register_blueprint(jacob)

from templates.jacobgame import jacobgame
app.register_blueprint(jacobgame)

# connects default URL to render index.html
@app.route('/')
def index():
    return render_template("index.html")


fiveStars_list = []
fourStars_list = []
threeStars_list = []
twoStarts_list = []
oneStar_list = []
@app.route('/aboutnathan')
def aboutnathan():
    return render_template("aboutnathan.html")


@app.route('/aboutreem')
def aboutreem():
    return render_template("aboutreem.html")



@app.route('/aboutjacob')
def aboutjacob():
    return render_template("aboutjacob.html")


@app.route('/aboutjames')
def aboutjames():
    return render_template("aboutjames.html")


@app.route('/aboutdaniel')
def aboutdaniel():
    return render_template("aboutdaniel.html")


@app.route('/mainabout/')
def mainabout():
    return render_template("mainabout.html")


@app.route('/worldclock/')
def worldclock():
    return render_template("worldclock.html")


@app.route('/feedback/', methods=['GET', 'POST'])
def feedback():
    if request.form:
        input = request.form.get("feed1")
        name = request.form.get("feed2")
        if len(input) != 0:  # input field has content
            return render_template("layouts/feedback.html", input=input, name=name)
    return render_template("layouts/feedback.html")


@app.route('/translator/', methods=['GET', 'POST'])
def translator():
    url = "https://translated-mymemory---translation-memory.p.rapidapi.com/api/get"
    pairs = ["en|es", "en|it", "en|zh", "en|de", "en|he"]
    text = "Translated text will show here"
    original = text
    master_list = []
    if request.form:
        text = request.form.get("tester2")
        original = text
    for item in pairs:
        querystring = {"langpair":item,"q":text , "mt":"1","onlyprivate":"0","de":"a@b.c"}

        headers = {
            'x-rapidapi-host': "translated-mymemory---translation-memory.p.rapidapi.com",
            'x-rapidapi-key': "00a6319afcmshb59ecb31e0a9dbap1c6de4jsn4b86a9198483"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        print(response.text)
        dictionary = [response.json().get('responseData')]
        master_list = master_list + dictionary
    return render_template("layouts/translator.html", dictionary=master_list, original=original)

@app.route('/crud')
def crud():
    return render_template("crud.html")


@app.route('/population', methods=['GET', 'POST'])
def population():
    urlnm = "https://world-population.p.rapidapi.com/allcountriesname"

    headers = {
        'x-rapidapi-host': 'world-population.p.rapidapi.com',
        'x-rapidapi-key': 'f4480562c7mshcfebe0975d4fd48p16ab77jsnae6575329780'
    }

    # get list of countries
    querystring = {}
    response = requests.request("GET", urlnm, headers=headers, params=querystring)
    list_of_names = response.json().get('body').get('countries')

    # build short list of countries
    short_list = list_of_names[0:10]

    # get all the data for each country
    dictionarymasterlist = []  # this creates an empty list that all the dictionaries go into
    url = "https://world-population.p.rapidapi.com/population"

    for item in short_list:
        querystring = {"country_name": item}
        response = requests.request("GET", url, headers=headers, params=querystring)

        list_of_dictionaries2 = response.json().get('body')
        dictionarymasterlist = dictionarymasterlist + [list_of_dictionaries2]

    return render_template("layouts/population.html", people=dictionarymasterlist)


@app.route('/environmental/', methods=['GET', 'POST'])
def environmental():
    headers = {
        'x-rapidapi-host': 'environment-news-live.p.rapidapi.com',
        'x-rapidapi-key': 'f4480562c7mshcfebe0975d4fd48p16ab77jsnae6575329780'
    }

    # get list of newspapers
    querystring = {}
    urlNewsList = "https://environment-news-live.p.rapidapi.com/newspapers"
    response = requests.request("GET", urlNewsList, headers=headers, params=querystring)

    list_of_papers = []
    list_of_papers = response.json()  # get('body').get('countries')

    # get all the articles of each source
    dictionarymasterlist = []  # this creates an empty list that all the dictionaries go into

    for item in list_of_papers:
      print(item)
      PaperName = item.get('newspaperID')
      if (PaperName != 'latimes' and PaperName != 'telegraph') : continue

      urlPaper= 'https://environment-news-live.p.rapidapi.com/news/%s' % PaperName
      querystring = {"newspaperID": PaperName}
      response = requests.request("GET", urlPaper, headers=headers, params=querystring)

      list_of_articles = response.json()  # get('body').get('countries')
      dictionarymasterlist = dictionarymasterlist + list_of_articles

    print(dictionarymasterlist)
    return render_template("layouts/environmental.html", news=dictionarymasterlist)


@app.route('/crud_api')
def crud_async():
    return render_template("crud_async.html")




@app.route('/search')
def search():
    return render_template("search.html")


@app.route('/gallery')
def gallery():
    return render_template("gallery.html")


@app.route('/seniortask/', methods=['GET', 'POST'])
def seniortask():

    name = "answers "
    input = request.form.get("input")

    # get the list of tries
    tries = comparisonInput(input)

    # convert list to string
    attempts = ' '.join(tries)

    return render_template("layouts/seniortask.html", input=attempts, name=name)


@app.route('/weather/', methods=['GET', 'POST'])
def weather():
    countrycode = ['105391811', '105368361', '105359777', '105341704', '105393052', '105392171']
    dictionarymasterlist = []  # this creates an empty list that all the dictionaries go into
    for item in countrycode:  # this is a for loop for all the country codes so that each one gets a response
        url = "https://foreca-weather.p.rapidapi.com/observation/latest/" + item

        querystring = {"lang": "en"}

        headers = {
            'x-rapidapi-host': "foreca-weather.p.rapidapi.com",
            'x-rapidapi-key': "00a6319afcmshb59ecb31e0a9dbap1c6de4jsn4b86a9198483"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        list_of_dictionaries2 = response.json().get('observations')
        dictionarymasterlist = dictionarymasterlist + list_of_dictionaries2
    print('WEATHER INFO')
    print(dictionarymasterlist)
    return render_template("layouts/weather.html", weather=dictionarymasterlist)
fivestars_list = []
fourstars_list = []
threestars_list = []
twostars_list = []
onestar_list = []


@app.route('/ratingtest/')
def ratingtest():
    total = len(oneStar_list) + len(twoStarts_list) + len(threeStars_list) + len(fourStars_list) + len(fiveStars_list)
    sum = len(oneStar_list) + len(twoStarts_list) * 2 + len(threeStars_list) * 3 + len(fourStars_list) * 4 + len(
        fiveStars_list) * 5
    if total != 0:
        average = sum / total
    else:
        average = 0
    return render_template("ratingtest.html", fiveStarsreview=fiveStars_list, fourStarsreview=fourStars_list,
                           threeStarsreview=threeStars_list, twoStartsreview=twoStarts_list, oneStarreview=oneStar_list,
                           average=average)


@app.route('/fiveStars', methods=['GET', 'POST'])
def fiveStars():
    total = len(oneStar_list) + len(twoStarts_list) + len(threeStars_list) + len(fourStars_list) + len(fiveStars_list)
    sum = len(oneStar_list) + len(twoStarts_list) * 2 + len(threeStars_list) * 3 + len(fourStars_list) * 4 + len(
        fiveStars_list) * 5
    if total != 0:
        average = sum / total
    else:
        average = 0
    if request.form:
        review = request.form.get("review")
        if len(review) != 0:
            fiveStars_list.append(review)
            total = len(oneStar_list) + len(twoStarts_list) + len(threeStars_list) + len(fourStars_list) + len(fiveStars_list)
            sum = len(oneStar_list) + len(twoStarts_list) * 2 + len(threeStars_list) * 3 + len(fourStars_list) * 4 + len(fiveStars_list) * 5
            if total != 0:
                average = sum / total
            else:
                average = 0
            return render_template("ratingtest.html", fiveStarsreview=fiveStars_list, fourStarsreview=fourStars_list,
                                   threeStarsreview=threeStars_list, twoStartsreview=twoStarts_list,
                                   oneStarreview=oneStar_list, average=average)
    return render_template("ratingtest.html", fiveStarsreview=fiveStars_list, fourStarsreview=fourStars_list,
                           threeStarsreview=threeStars_list, twoStartsreview=twoStarts_list, oneStarreview=oneStar_list,
                           average=average)


@app.route('/fourStars', methods=['GET', 'POST'])
def fourStars():
    total = len(oneStar_list) + len(twoStarts_list) + len(threeStars_list) + len(fourStars_list) + len(fiveStars_list)
    sum = len(oneStar_list) + len(twoStarts_list) * 2 + len(threeStars_list) * 3 + len(fourStars_list) * 4 + len(
        fiveStars_list) * 5
    if total != 0:
        average = sum / total
    else:
        average = 0
    if request.form:
        review = request.form.get("review")
        if len(review) != 0:
            fourStars_list.append(review)
            total = len(oneStar_list) + len(twoStarts_list) + len(threeStars_list) + len(fourStars_list) + len(
                fiveStars_list)
            sum = len(oneStar_list) + len(twoStarts_list) * 2 + len(threeStars_list) * 3 + len(fourStars_list) * 4 + len(
                fiveStars_list) * 5
            if total != 0:
                average = sum / total
            else:
                average = 0
            return render_template("ratingtest.html", fiveStarsreview=fiveStars_list, fourStarsreview=fourStars_list,
                                   threeStarsreview=threeStars_list, twoStartsreview=twoStarts_list,
                                   oneStarreview=oneStar_list, average=average)
    return render_template("ratingtest.html", fiveStarsreview=fiveStars_list, fourStarsreview=fourStars_list,
                           threeStarsreview=threeStars_list, twoStartsreview=twoStarts_list, oneStarreview=oneStar_list,
                           average=average)


@app.route('/threeStars', methods=['GET', 'POST'])
def threeStars():
    total = len(oneStar_list) + len(twoStarts_list) + len(threeStars_list) + len(fourStars_list) + len(fiveStars_list)
    sum = len(oneStar_list) + len(twoStarts_list) * 2 + len(threeStars_list) * 3 + len(fourStars_list) * 4 + len(
        fiveStars_list) * 5
    if total != 0:
        average = sum / total
    else:
        average = 0
    if request.form:
        review = request.form.get("review")
        if len(review) != 0:
            threeStars_list.append(review)
            total = len(oneStar_list) + len(twoStarts_list) + len(threeStars_list) + len(fourStars_list) + len(
                fiveStars_list)
            sum = len(oneStar_list) + len(twoStarts_list) * 2 + len(threeStars_list) * 3 + len(fourStars_list) * 4 + len(
                fiveStars_list) * 5
            if total != 0:
                average = sum / total
            else:
                average = 0
            return render_template("ratingtest.html", fiveStarsreview=fiveStars_list, fourStarsreview=fourStars_list,
                                   threeStarsreview=threeStars_list, twoStartsreview=twoStarts_list,
                                   oneStarreview=oneStar_list, average=average)
    return render_template("ratingtest.html", fiveStarsreview=fiveStars_list, fourStarsreview=fourStars_list,
                           threeStarsreview=threeStars_list, twoStartsreview=twoStarts_list, oneStarreview=oneStar_list,
                           average=average)


@app.route('/twoStarts', methods=['GET', 'POST'])
def twoStarts():
    total = len(oneStar_list) + len(twoStarts_list) + len(threeStars_list) + len(fourStars_list) + len(fiveStars_list)
    sum = len(oneStar_list) + len(twoStarts_list) * 2 + len(threeStars_list) * 3 + len(fourStars_list) * 4 + len(
        fiveStars_list) * 5
    if total != 0:
        average = sum / total
    else:
        average = 0
    if request.form:
        review = request.form.get("review")
        if len(review) != 0:
            twoStarts_list.append(review)
            total = len(oneStar_list) + len(twoStarts_list) + len(threeStars_list) + len(fourStars_list) + len(
                fiveStars_list)
            sum = len(oneStar_list) + len(twoStarts_list) * 2 + len(threeStars_list) * 3 + len(fourStars_list) * 4 + len(
                fiveStars_list) * 5
            if total != 0:
                average = sum / total
            else:
                average = 0
            return render_template("ratingtest.html", fiveStarsreview=fiveStars_list, fourStarsreview=fourStars_list,
                                   threeStarsreview=threeStars_list, twoStartsreview=twoStarts_list,
                                   oneStarreview=oneStar_list, average=average)
    return render_template("ratingtest.html", fiveStarsreview=fiveStars_list, fourStarsreview=fourStars_list,
                           threeStarsreview=threeStars_list, twoStartsreview=twoStarts_list, oneStarreview=oneStar_list,
                           average=average)


@app.route('/oneStar', methods=['GET', 'POST'])
def oneStar():
    total = len(oneStar_list) + len(twoStarts_list) + len(threeStars_list) + len(fourStars_list) + len(fiveStars_list)
    sum = len(oneStar_list) + len(twoStarts_list) * 2 + len(threeStars_list) * 3 + len(fourStars_list) * 4 + len(
        fiveStars_list) * 5
    if total != 0:
        average = sum / total
    else:
        average = 0
    if request.form:
        review = request.form.get("review")
        if len(review) != 0:
            oneStar_list.append(review)
            total = len(oneStar_list) + len(twoStarts_list) + len(threeStars_list) + len(fourStars_list) + len(
                fiveStars_list)
            sum = len(oneStar_list) + len(twoStarts_list) * 2 + len(threeStars_list) * 3 + len(fourStars_list) * 4 + len(
                fiveStars_list) * 5
            if total != 0:
                average = sum / total
            else:
                average = 0
            return render_template("ratingtest.html", fiveStarsreview=fiveStars_list, fourStarsreview=fourStars_list,
                                   threeStarsreview=threeStars_list, twoStartsreview=twoStarts_list,
                                   oneStarreview=oneStar_list, average=average)
    return render_template("ratingtest.html", fiveStarsreview=fiveStars_list, fourStarsreview=fourStars_list,
                           threeStarsreview=threeStars_list, twoStartsreview=twoStarts_list, oneStarreview=oneStar_list,
                           average=average)

@app.route('/countries')
def countries():
    return render_template("countries.html")

@app.route('/faq')
def faq():
    return render_template("faq.html")

@app.route('/infopage')
def infopage():
    return render_template("infopage.html")

@app.route('/currency', methods=['GET', 'POST'])
def currency():
    return render_template("layouts/currency.html")

@app.route('/world_instruments', methods=['GET', 'POST'])
def world_instruments():
    return render_template("layouts/world_instruments.html")

@app.route('/quiz')
def quiz():
    return render_template("quiz.html")


# runs the application on the development server
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)








