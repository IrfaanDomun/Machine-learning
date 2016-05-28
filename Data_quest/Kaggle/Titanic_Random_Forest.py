import pandas
import re
import operator
import matplotlib.pyplot as plt
import numpy as np

from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import GradientBoostingClassifier


# A function to get the title from a name.
def get_title(name):
    # Use a regular expression to search for a title.  Titles always consist of capital and lowercase letters, and end with a period.
    title_search = re.search(' ([A-Za-z]+)\.', name)
    # If the title exists, extract and return it.
    if title_search:
        return title_search.group(1)
    return ""

# A function to get the id given a row
def get_family_id(row):
    # Find the last name by splitting on a comma
    last_name = row["Name"].split(",")[0]
    # Create the family id
    family_id = "{0}{1}".format(last_name, row["FamilySize"])
    # Look up the id in the mapping
    if family_id not in family_id_mapping:
        if len(family_id_mapping) == 0:
            current_id = 1
        else:
            # Get the maximum id from the mapping and add one to it if we don't have an id
            current_id = (max(family_id_mapping.items(), key=operator.itemgetter(1))[1] + 1)
        family_id_mapping[family_id] = current_id
    return family_id_mapping[family_id]

if __name__=='__main__':
    """    Load data    """
    titanic = pandas.read_csv("C:\\Users\\i\\Downloads\\titanic_train.csv")
    
    # Print the first 5 rows of the dataframe.
    print(titanic.head(5))
    print(titanic.describe())  
    
    """     Clean the train data  """
    # clean the NaN
    titanic["Age"] = titanic["Age"].fillna(titanic["Age"].median())
    
    # Convert non numerical data
    print(titanic["Sex"].unique())
    titanic.loc[titanic["Sex"] == "male", "Sex"] = 0
    titanic.loc[titanic["Sex"] == "female", "Sex"] = 1
    
    print(titanic["Embarked"].unique())
    titanic["Embarked"] = titanic["Embarked"].fillna("S")
    titanic.loc[titanic["Embarked"] == "S", "Embarked"] = 0
    titanic.loc[titanic["Embarked"] == "C", "Embarked"] = 1
    titanic.loc[titanic["Embarked"] == "Q", "Embarked"] = 2
    
    """    fit the data into the model and predict the outcome  """
    # The columns we'll use to predict the target
    predictors = ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"]
    
    """    Clean the test data    """
    titanic_test = pandas.read_csv("C:\\Users\\i\\Downloads\\titanic_test.csv")
    
    titanic_test["Age"] = titanic_test["Age"].fillna(titanic["Age"].median())
    titanic_test.loc[titanic_test["Sex"] == 'male',"Sex"] = 0
    titanic_test.loc[titanic_test["Sex"] == 'female',"Sex"] = 1
    
    titanic_test["Embarked"] = titanic_test["Embarked"].fillna("S")
    titanic_test.loc[titanic_test["Embarked"] == "S","Embarked"] = 0
    titanic_test.loc[titanic_test["Embarked"] == "C","Embarked"] = 1
    titanic_test.loc[titanic_test["Embarked"] == "Q","Embarked"] = 2
    
    titanic_test["Fare"] = titanic_test["Fare"].fillna(titanic_test["Fare"].median())
    
    predictors = ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"]
    
    # Initialize our algorithm with the default paramters
    # n_estimators is the number of trees we want to make
    # min_samples_split is the minimum number of rows we need to make a split
    # min_samples_leaf is the minimum number of samples we can have at the place where a tree branch ends (the bottom points of the tree)
    alg = RandomForestClassifier(random_state=1, n_estimators=10, min_samples_split=2, min_samples_leaf=1)
    scores = cross_validation.cross_val_score(alg, titanic[predictors], titanic["Survived"], cv=3)
    print(scores.mean())
    
    """     Generating new features     """
    # Generating a familysize column
    titanic["FamilySize"] = titanic["SibSp"] + titanic["Parch"]
    
    # The .apply method generates a new series
    titanic["NameLength"] = titanic["Name"].apply(lambda x: len(x))
    
    # Get all the titles and print how often each one occurs.
    titles = titanic["Name"].apply(get_title)
    print(pandas.value_counts(titles))
    
    # Map each title to an integer.  Some titles are very rare, and are compressed into the same codes as other titles.
    title_mapping = {"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Dr": 5, "Rev": 6, "Major": 7, "Col": 7, "Mlle": 8, "Mme": 8, "Don": 9, "Lady": 10, "Countess": 10, "Jonkheer": 10, "Sir": 9, "Capt": 7, "Ms": 2}
    for k,v in title_mapping.items():
        titles[titles == k] = v
    
    # Verify that we converted everything.
    print(pandas.value_counts(titles))
    
    # Add in the title column.
    titanic["Title"] = titles
        
    # A dictionary mapping family name to id
    family_id_mapping = {}
    
    # Get the family ids with the apply method
    family_ids = titanic.apply(get_family_id, axis=1)
    
    # There are a lot of family ids, so we'll compress all of the families under 3 members into one code.
    family_ids[titanic["FamilySize"] < 3] = -1
    
    # Print the count of each unique id.
    print(pandas.value_counts(family_ids))
    
    titanic["FamilyId"] = family_ids
    
    
    predictors = ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked", "FamilySize", "Title", "FamilyId"]
    
    # Perform feature selection
    selector = SelectKBest(f_classif, k=5)
    selector.fit(titanic[predictors], titanic["Survived"])
    
    # Get the raw p-values for each feature, and transform from p-values into scores
    scores = -np.log10(selector.pvalues_)

    # Plot the scores.  See how "Pclass", "Sex", "Title", and "Fare" are the best?
    plt.bar(range(len(predictors)), scores)
    plt.xticks(range(len(predictors)), predictors, rotation='vertical')
    plt.show()
    
    # Pick only the four best features.
    predictors = ["Pclass", "Sex", "Fare", "Title"]
    
    alg = RandomForestClassifier(random_state=1, n_estimators=150, min_samples_split=8, min_samples_leaf=4)
    scores = cross_validation.cross_val_score(alg, titanic[predictors], titanic["Survived"], cv=3)
    print(scores.mean())
    
