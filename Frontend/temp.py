from flask import Flask, request, render_template
from elasticsearch import Elasticsearch
from flask_cors import CORS, cross_origin

es = Elasticsearch()
app = Flask(__name__)
CORS(app, support_credentials=True)


def topleftquery(lon1, lat1, lon2, lat2):
    return es.search(index="tweets", body={"query": {
        "bool": {
            "filter": [{
                "geo_bounding_box": {
                    "geo": {
                        "top_left": {
                            "lat": lat1,
                            "lon": lon1
                        },
                        "bottom_right": {
                            "lat": lat2,
                            "lon": lon2
                        }
                    }
                }
            }]
        }
    }
    })


def toprightquery(lon1, lat1, lon2, lat2):
    return es.search(index="tweets", body={"query": {
        "bool": {
            "filter": [{
                "geo_bounding_box": {
                    "geo": {
                        "top_right": {
                            "lat": lat1,
                            "lon": lon1
                        },
                        "bottom_left": {
                            "lat": lat2,
                            "lon": lon2
                        }
                    }
                }
            }]
        }
    }
    })


@app.route('/', methods=['GET'])
def func():
    return render_template("MAP.html")


@app.route('/plot', methods=['POST'])
@cross_origin(supports_credentials=True)
@cross_origin(origin='*')
def search():
    print('Date 1 value: ', request.form['T1'])
    print('Date 2 value: ', request.form['T2'])

    lat1 = float(request.form['lat1'])
    lng1 = float(request.form['lng1'])
    lat2 = float(request.form['lat2'])
    lng2 = float(request.form['lng2'])
    search_word = request.form['keyword']
    try:
        mon1 = int(request.form['T1'])
    except ValueError:
        print("Failure w/ value " + val)
    try:
        mon2 = int(request.form['T2']) + 1
    except ValueError:
        print("Failure w/ value " + val)
    print(lat1, lng1, lat2, lng2, search_word, mon1, mon2)
    tweets = []
    x = es.search(index="tweets", body={
        "query": {
            "bool": {
                "filter": [{"match": {"content": search_word}},
                  {"range": {
                      "created_at_m": {
                          "gte": mon1,
                          "lte": mon2 + 1,
                      }
                  }}]
            }
        }
    })
    #y = toprightquery(lng1, lat1, lng2, lat2)
    """ if lat1 > lat2:
        if lng1 > lng2:
            y = toprightquery(lng1, lat1, lng2, lat2)
        else:
            y = topleftquery(lng1, lat1, lng2, lat2)
    else:
        if lng1 > lng2:
            y = topleftquery(lng2, lat2, lng1, lat1)
        else:
            y = toprightquery(lng2, lat2, lng1, lat1) """
    array = []
    for i in range(mon1, mon2):
        array.append([i, 0])
    for obj1 in x['hits']['hits']:
        tweets.append(obj1)
    for j in tweets:
        for i in array:
            if i[0] == (j['_source']['created_at_m']):
                i[1] += 1
    array1 = []
    tempArray1 = []
    tempArray2 = []
    for i in array:
        tempArray1.append(i[0])
        tempArray2.append(i[1])
    data = {'xValues': tempArray1,
            'yValues': tempArray2}
    return data


@app.route('/insights', methods=['POST'])
@cross_origin(supports_credentials=True)
@cross_origin(origin='*')
def return_tweets():
    lat1 = float(request.form['lat1'])
    lng1 = float(request.form['lng1'])
    lat2 = float(request.form['lat2'])
    lng2 = float(request.form['lng2'])
    search_word = request.form['keyword']
    mon1 = int(request.form['T1'])
    mon2 = int(request.form['T2'])
    x = es.search(index="tweets", body={
        "query": {
            "bool": {
                "filter": [{"match": {"content": search_word}},
                  {"range": {
                      "created_at_m": {
                          "gte": mon1,
                          "lte": mon2,
                      }
                  }}]
            }
        }
    })
    """ if lat1 > lat2:
        if lng1 > lng2:
            y = toprightquery(lng1, lat1, lng2, lat2)
        else:
            y = topleftquery(lng1, lat1, lng2, lat2)
    else:
        if lng1 > lng2:
            y = topleftquery(lng2, lat2, lng1, lat1)
        else:
            y = toprightquery(lng2, lat2, lng1, lat1) """
    tweets = []
    for obj1 in x['hits']['hits']:
        tweets.append(obj1['_source']['content'])

    return render_template("insights.html", len=len(tweets), tweets=tweets)


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
