from pandas import DataFrame, concat, Series, isna
DEBUG = False

def __expand_subdict__(df_col):
    """
    Expand a column of dictionaries into a Series
    Drop any all nan columns
    """
    return df_col.apply(Series).dropna(axis=1, how='all')
    

def __values_are_dict_like__(col):
    """
    Check if a is a dictionary
    """
    if col.dtype == 'object':
        
        if hasattr(col,'str') and col.str.contains(r'\{.*\}').any():
            return True
        elif col.apply(lambda x: isinstance(x, dict)).any():
            return True
        else:
            return False
    else:
        return False

def __values_are_list_like__(col):
    """
    Check if any element in a column is a list
    """
    return col.apply(lambda x: isinstance(x, list)).any()

def __convertable_to_DataFrame__(x):
    """
    Check if a value can be expanded to a dataframe
    """
    return __values_are_dict_like__(x) or __values_are_list_like__(x)
    
def flatten(df, parent = '', delimiter = '.', fname = None,  tab = 0):
    """
    Recursively flat a pandas DataFrame with nested dictionaries
    """
    markdown_string = lambda col: '  ' * tab+ '- {}'.format(col.replace(parent,'').lstrip(delimiter)) + '\n'
    
    if isinstance(df, Series) or __values_are_list_like__(df):
        new_df = __expand_subdict__(df).add_prefix(parent + delimiter)
        return flatten(new_df, parent = parent, delimiter = delimiter,  fname = fname, tab = tab + 1)
    else:
        for col in df.columns:
            if fname is not None: fname.write(markdown_string(col))
            
            if __convertable_to_DataFrame__(df[col]):
                df = df.join(flatten(df[col], parent = col, delimiter = delimiter,  fname = fname, tab = tab + 1))
                df.drop(col, axis=1, inplace=True)

    return df  