from sklearn import tree
import math
import numpy as np

x = [i for i in range(500)]
y = [math.sin(i) for i in x]


clf = tree.DecisionTreeRegressor()
clf = clf.fit(np.array(x).reshape(-1, 1), y)

print(clf.predict([[5.0]]))
