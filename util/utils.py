
"""
from constants import *
from models.item import Item
from models.room import Room
"""

import random
import textwrap

#region Define help funcs and essential funcs

def return_val_in_list(ar_to_search,val_to_find):
    for i in ar_to_search:
        if i == val_to_find:
            return True

    return False

#endregion
