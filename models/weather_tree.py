from sklearn import tree
from sklearn.externals.six import StringIO
from IPython.display import Image
import pydotplus
import csv

# declare vars
features = []
features_names = ['precipIntensity', 'precipProbability', 
            'temperature', 'apparentTemperature', 'dewPoint', 
            'humidity', 'pressure', 'windSpeed', 'windBearing', 
            'cloudCover', 'uvIndex', 'visibility']
label_names = []
labels = []

# get data in json
# with open('weather_data.json') as json_file:
#     data = json.load(json_file)
#     # print(data['daily']['data'][0])
#     for d in data['daily']['data']:
#         l = d['summary']
#         if l not in label_names:
#             label_names.append(l)
#         labels.append(label_names.index(l))
#         f = []
#         for name in features_names:
#             f.append(d[name])
#         features.append(f)

#get data in csv
with open('weather_data_temp.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            l = row[1]
            if l not in label_names:
                label_names.append(l)
            labels.append(label_names.index(l))
            f = []
            for i in range(2,14):
                f.append(row[i])
            features.append(f)
            line_count += 1

# make decision tree
clf = tree.DecisionTreeClassifier()
clf = clf.fit(features, labels)

#print decision tree
# from sklearn.externals.six import StringIO
# from IPython.display import Image
# import pydotplus
dot_data = StringIO()
tree.export_graphviz(clf, 
                    out_file=dot_data,
                    feature_names=features_names,
                    class_names=label_names,
                    filled=True,
                    rounded=True,
                    impurity=False)

graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
graph.write_pdf("weather_tree.pdf")
