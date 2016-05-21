from time import time 
t = time()
def libsvm2list(filename):
    vector = []
    fichier= open(filename)
    label = []
    for i in fichier:
         vector_temp = []
         sp = i.split()
         label.append(sp[0])
         for j in sp[1:]:
             vector_temp.append(float(j.split(":")[1]))
         vector.append(vector_temp)
    print vector[:10],label[:10]
    return vector, label

# print count 
filename = "C:\Users\i\Downloads"

train, train_label = libsvm2list(filename+"\ijcnn1.tr")
test, test_label = libsvm2list(filename+"\ijcnn1")

from sklearn import svm
clf = svm.SVC()
print clf
clf.fit(train, train_label)

print [ i for i in clf.predict(test) if i != "-1.0" ]  
# print (map(float,test_label[:10]))  

print clf.score(test,map(str,map(float, test_label)))
print time() - t 