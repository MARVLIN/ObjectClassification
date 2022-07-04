import json
import numpy
from json import JSONEncoder
from main import x, y, w, h
numpyArray = x, y, w, h


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


numpyData = {'array': numpyArray}
encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)
print('Printing JSON')
print(encodedNumpyData)




