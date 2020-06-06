# Random Forest Regression

# Importing the libraries
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
# dataset = pd.read_csv('userdata.csv')
# x = dataset.iloc[:, 1:-1].values
# Y = dataset.iloc[:, -1].values
# X = []
# y = []
# for val in x:
#     y.append([float(val[0][1:-1])])

# for val in Y:
#     X.append([int(val[1:-1])])

def expected_value(scores):
    dic = {}
    for score in scores:
        if score[0] in dic:
            dic[score[0]] += 1
        else:
            dic[score[0]] = 1

    exp_val = 0
    LEN = len(scores)
    for key in dic:
        exp_val += (key * (dic[key]/LEN))

    return round(exp_val*100, 1)

# print(expected_value(y))



def bar_graph(X, y):
    import matplotlib
    matplotlib.use('Agg')

    temp = []
    for val in y:
        temp.append(val[0])
    y = temp

    dic = {}
    for ind, time in enumerate(X):
        if time[0] in dic:
            dic[time[0]].append(y[ind])
        else:
            dic[time[0]] = [y[ind]]

    x_axis = []
    y_axis = []
    for item in sorted(dic.items()):
        x_axis.append(item[0])
        y_axis.append(sum(item[1])/ len(item[1]))

    plt.xlabel("Time since memory uploaded (mins)")
    plt.ylabel("Average memory score")
    plt.ylim(0, 1.1)

    plt.bar(x_axis, y_axis)
    # plt.show()
    import base64
    import io
    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='jpg')
    my_stringIObytes.seek(0)
    my_base64_jpgData = base64.b64encode(my_stringIObytes.read())
    plt.clf()
    return my_base64_jpgData

# bar_graph(X, y)



def random_forest(X, y):
    import matplotlib
    matplotlib.use('Agg')

    X = np.array(X)
    y = np.array(y)

    # Training the Random Forest Regression model on the whole dataset
    regressor = RandomForestRegressor(n_estimators=10, random_state=0)
    regressor.fit(X, y.ravel())

    # # Visualising the Random Forest Regression results (higher resolution)
    X_grid = np.arange(min(X)[0], max(X)[0], 0.01)
    X_grid = X_grid.reshape((len(X_grid), 1))
    # plt.scatter(X, y, color='red')
    plt.plot(X_grid, regressor.predict(X_grid), color='blue')
    plt.title('Random Forest Regression')
    plt.xlabel('Time between upload and redescription (mins)')
    plt.ylabel('Memory Score (0-1)')
    plt.ylim(0, 1.1)
    # plt.show()
    import base64
    import io
    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='jpg')
    my_stringIObytes.seek(0)
    my_base64_jpgData = base64.b64encode(my_stringIObytes.read())
    plt.clf()
    return my_base64_jpgData

# random_forest(X, y)


def svr(X, y):
    import matplotlib
    matplotlib.use('Agg')
    from sklearn.preprocessing import StandardScaler
    sc_X = StandardScaler()
    sc_y = StandardScaler()
    X = sc_X.fit_transform(X)
    y = sc_y.fit_transform(y)

    from sklearn.svm import SVR
    regressor = SVR(kernel = 'rbf')
    regressor.fit(X, y.ravel())

    X_grid = np.arange(min(sc_X.inverse_transform(X)), max(sc_X.inverse_transform(X)), 0.1)
    X_grid = X_grid.reshape((len(X_grid), 1))
    # print(X_grid)
    # plt.scatter(sc_X.inverse_transform(X), sc_y.inverse_transform(y), color = 'red')
    plt.plot(X_grid, sc_y.inverse_transform(regressor.predict(sc_X.transform(X_grid))), color = 'blue')
    plt.title('Support Vector Regression')
    plt.xlabel('Time between upload and redescription (mins)')
    plt.ylabel('Memory score (0-1)')
    plt.ylim(0, 1.1)
    
    # plt.show()
    import base64
    import io
    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='jpg')
    my_stringIObytes.seek(0)
    my_base64_jpgData = base64.b64encode(my_stringIObytes.read())
    plt.clf()
    return my_base64_jpgData

def svr_overtime(X, y):
    import matplotlib
    matplotlib.use('Agg')
    from sklearn.preprocessing import StandardScaler
    sc_X = StandardScaler()
    sc_y = StandardScaler()
    X = sc_X.fit_transform(X)
    y = sc_y.fit_transform(y)

    from sklearn.svm import SVR
    regressor = SVR(kernel = 'rbf')
    regressor.fit(X, y.ravel())

    X_grid = np.arange(min(sc_X.inverse_transform(X)), max(sc_X.inverse_transform(X)), 0.1)
    X_grid = X_grid.reshape((len(X_grid), 1))
    # print(X_grid)
    # plt.scatter(sc_X.inverse_transform(X), sc_y.inverse_transform(y), color = 'red')
    plt.plot(X_grid, sc_y.inverse_transform(regressor.predict(sc_X.transform(X_grid))), color = 'blue')
    plt.title('Support Vector Regression')
    plt.xlabel('Memory Number (Chronological Order)')
    plt.ylabel('Memory score (0-1)')
    plt.ylim(0, 1.1)
    
    
    # plt.show()
    import base64
    import io
    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='jpg')
    my_stringIObytes.seek(0)
    my_base64_jpgData = base64.b64encode(my_stringIObytes.read())
    plt.clf()
    return my_base64_jpgData

def rf_overtime(X, y):
    import matplotlib
    matplotlib.use('Agg')

    X = np.array(X)
    y = np.array(y)

    # Training the Random Forest Regression model on the whole dataset
    regressor = RandomForestRegressor(n_estimators=10, random_state=0)
    regressor.fit(X, y.ravel())

    # # Visualising the Random Forest Regression results (higher resolution)
    X_grid = np.arange(min(X)[0], max(X)[0], 0.01)
    X_grid = X_grid.reshape((len(X_grid), 1))
    # plt.scatter(X, y, color='red')
    plt.plot(X_grid, regressor.predict(X_grid), color='blue')
    plt.title('Random Forest Regression')
    plt.xlabel('Memory Number (Chronological Order)')
    plt.ylabel('Memory Score (0-1)')
    plt.ylim(0, 1.1)
    # plt.show()
    import base64
    import io
    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='jpg')
    my_stringIObytes.seek(0)
    my_base64_jpgData = base64.b64encode(my_stringIObytes.read())
    plt.clf()
    return my_base64_jpgData

# X = [[5], [3], [5], [5], [5], [5], [5], [5], [5], [4], [5], [5], [5], [1], [7], [7], [7], [6], [6], [6], [6], [6], [6], [5], [27], [27], [26], [26], [26], [1], [1], [1], [1], [1], [1], [1], [1], [0], [0], [2], [2], [2], [2], [2], [2], [2], [1], [4], [3], [3], [4], [4], [4], [4], [3], [4], [4], [3], [10], [10], [10], [11], [11], [11], [11], [10], [12], [12], [12], [12], [12], [12], [12], [11], [11], [11], [11], [11], [10], [10], [11], [11], [10], [10], [10], [10], [9], [13], [12], [12], [12], [11], [11], [10], [10], [13], [13], [14], [11], [16], [20], [20], [20], [20], [20], [19]]
# y = [[0.73], [0.9], [0.64], [0.62], [0.79], [0.9], [0.62], [0.93], [0.82], [0.64], [0.43], [0.89], [1.0], [1.0], [0.86], [1.0], [1.0], [1.0], [1.0], [1.0], [0.8], [0.95], [1.0], [0.97], [0.96], [1.0], [1.0], [0.99], [1.0], [1.0], [0.92], [0.72], [0.57], [0.74], [0.95], [0.56], [0.88], [0.77], [0.81], [1.0], [0.98], [0.9], [1.0], [1.0], [0.9], [0.96], [0.86], [0.82], [1.0], [0.95], [0.9], [0.92], [1.0], [0.86], [1.0], [0.75], [0.81], [1.0], [1.0], [0.59], [0.41], [1.0], [0.6], [1.0], [0.58], [0.83], [0.64], [1.0], [0.78], [0.89], [0.69], [0.44], [0.4], [0.64], [0.83], [0.53], [0.9], [0.73], [0.84], [0.86], [0.55], [0.76], [0.28], [0.84], [0.57], [0.43], [0.51], [0.67], [0.81], [0.53], [0.67], [0.6], [1.0], [0.23], [0.72], [0.36], [0.84], [1.0], [0.3], [0.89], [0.85], [0.43], [0.75], [0.92], [1.0], [0.28]]

# print(svr(X, y))
# print(bar_graph(X, y))
# svr(X, )

# y = [[1], [1]]
# X = [[0.89], [0.78]]
# print(svr(X, y))

# X = [[1.0], [1.0], [0.7], [0.56]]
# y = [[0], [0], [0], [0]]
# print(svr(X, y))