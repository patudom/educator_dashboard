import numpy as np

from typing import List, Dict



def list_of_dicts_to_dict_of_lists(list_of_dicts: List[Dict], fill_val = None) -> Dict:
        """
        convert list of dictionaries to a dictionary of lists
        
        Parameters
        ----------
        list_of_dicts : list of dictionaries
            list of dictionaries to convert
            
        Returns
        -------
        dict_of_lists : dictionary of lists
            dictionary of lists
            
        Examples:
        >>> l2d([{'a': 1, 'b': 2}, {'a': 3, 'b': 4}])
        {'a': array([1, 3]), 'b': array([2, 4])}
        
        
        """
        # keys = list_of_dicts[0].keys()
        keys = []
        for d in list_of_dicts:
            if isinstance(d, dict):
                keys.extend([k for k in d.keys() if (k not in keys) and (k is not None)])
        
        dict_of_lists = {k: [o[k] if (hasattr(o,'keys') and (k in o.keys())) else fill_val for o in list_of_dicts] for k in keys}
        return dict_of_lists
    
def l2d(list_of_dicts: List[Dict], fill_val = None) -> Dict:
    """
        convert list of dictionaries to a dictionary of lists
        
        Parameters
        ----------
        list_of_dicts : list of dictionaries
            list of dictionaries to convert
        
        fill_val : any
            value to fill in for missing keys
            
        Returns
        -------
        dict_of_lists : dictionary of lists
            dictionary of lists
            
        Examples:
        >>> l2d([{'a': 1, 'b': 2}, {'a': 3, 'b': 4}])
        {'a': array([1, 3]), 'b': array([2, 4])}
        
        
        """
    return list_of_dicts_to_dict_of_lists(list_of_dicts, fill_val)


from pandas import to_datetime
def convert_column_of_dates_to_datetime(dataframe_column):
    return to_datetime(dataframe_column).dt.tz_convert('US/Eastern').dt.strftime("%Y-%m-%d %H:%M:%S (Eastern)")


def get_or_none(d: Dict | None, key: str, default = None):
    """
    get a value from a dictionary, or return None if it doesn't exist
    """
    
    if d is None:
        return None
    return d.get(key, default)