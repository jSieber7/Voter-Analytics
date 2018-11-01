from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score

def recur_dictify(frame):
    '''Recursive function to turn the meta data dataframe into a dictionary for remapping values'''
    
    # Base Case
    if len(frame.columns) == 1:
        if frame.values.size == 1: return frame.values[0][0]
        return frame.values.squeeze()
    
    # Recursive Case
    grouped = frame.groupby(frame.columns[0])
    dictionary = {name: recur_dictify(group.iloc[:,1:]) for name,group in grouped}
    return dictionary



class DataFrameSelector(BaseEstimator, TransformerMixin):
    '''Selects columns given a list of column names and turns into Numpy Array'''
    def __init__(self, attribute_names):
        self.attribute_names = attribute_names
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return X[self.attribute_names].values
    
class BinaryEncoding(BaseEstimator,TransformerMixin):
    '''Ensures that binary attirbutes are properly encoded while still retaining NaNs'''
    def fit(self,X,y=None):
        return self
    def transform(self,X, y=None):
        for col in  X.T:
            # While not a necessary feature in this instance, this is robust to missing values.
            col[(~np.isnan(col)) & (col!=np.nanmax(col))] = 0
            col[col==np.nanmax(col)] = 1
        return X
    
    
class DataFrameSelectorAndRecode(BaseEstimator, TransformerMixin):
    '''Same as DataFrameSelector, but also turns numbers into strings'''
    def __init__(self, attribute_names, remap_dict):
        self.attribute_names = attribute_names
        self.remap_dict = remap_dict 
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        X = X[self.attribute_names]
        X = X.replace(self.remap_dict)
        return X.values

# Note: These classes are different from the other classes. They expect a dataframe input and output a dataframe.

class UniqueThreshold(BaseEstimator, TransformerMixin):
    '''Drops columns that exceed a given amount of unqiues'''
    def __init__(self, threshold = 20, ignore_columns=None):
        self.max_unique = threshold
        self.keep_cols = ignore_columns
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        # We must code carefully to avoid getting rid of ordinal column values
    
        # Makes a list of all columns in X
        columns = list(X.columns)
        
        # Selects all of the columns that we want to filter for unique values 
        # (i.e. non-ordinal b/c it will inflate the amount of columns)
        non_ordinal_columns = [x for x in columns if x not in self.keep_cols]
        
        non_ordinal_columns = list()
        for x in columns:
            if x not in self.keep_cols:
                non_ordinal_columns.append(x)
        
        
        # Selects the columns that we want to filter 
        X_filtered = X.loc[:,non_ordinal_columns]
        
        # Sets a boolean index and uses it to filter our columns
        critera = (X_filtered.nunique() <= self.max_unique)
        under_thresh = list(critera.index[critera])
        
        # Gets the filtered columns and also puts in all ordinal columns
        X_filtered = X.loc[:, under_thresh + self.keep_cols]
        return X_filtered
    
class FilterNAs(BaseEstimator, TransformerMixin):
    '''Drops columns that exceed a given amount of NAs'''
    def __init__(self, threshold = .5):
        self.d_per = 1-threshold
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        new_thresh = self.d_per * X.shape[0]
        X.dropna(thresh=new_thresh, inplace=True, axis = 1)
        return X    

def QuickModel(ml_algo,names,X,y, scoring = 'r2'):
    '''Quick modeling and cross validation for multiple models'''
    for algo,name in zip(ml_algo,names):
        Model = algo
        Model = Model.fit(X,y)
        print(name, 'Cross Validation:', cross_val_score(Model,X,y,cv=5,scoring=scoring))