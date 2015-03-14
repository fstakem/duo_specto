# <-----------------------------------------< Header >----------------------------------------->
#
#       jsonable.py
#       By: Fredrick Stakem
#       Date: 3.3.15
#
#
# <-----------------------------------------<---~~--->----------------------------------------->

"""
This file is used to serialize a class to json.

"""


# Libraries
import json
from datetime import datetime


# Main
class Jsonable(object):
    
    def jsonizable(self):
        return self.__dict__
    
    def to_json(self):
        return json.dumps(self, default=ComplexHandler)
    
    def to_pretty_json(self):
        return json.dumps(self, default=ComplexHandler, sort_keys=True, indent=4)
        
    def __str__(self):
        return self.to_json()
    
    def __repr__(self):
        return self.to_json()
    
def ComplexHandler(obj):
    if isinstance(obj, datetime):
        return str(obj)
    
    if hasattr(obj, 'jsonizable'):
        return obj.jsonizable()
    else:
        raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))


    
    
    