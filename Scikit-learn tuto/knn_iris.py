from sklearn import datasets

"""
    Load the data
"""
iris = datasets.load_iris()

print "Iris shape",iris.data.shape 

print "Iris target shape",iris.target.shape 

import numpy as np 

print "unique target",np.unique(iris.target)

"""    
    Create classifier
"""
from sklearn import neighbors
knn = neighbors.KNeighborsClassifier()
knn.fit(iris.data, iris.target)

"""
    Test Classifier
"""
print knn.predict([[0.1, 0.2, 0.3, 0.4]])

"""
    Score classifier
"""
perm = np.random.permutation(iris.target.size)
iris.data = iris.data[perm]
iris.target = iris.target[perm]
knn.fit(iris.data[:100], iris.target[:100]) 

print knn.score(iris.data[100:], iris.target[100:]) 
