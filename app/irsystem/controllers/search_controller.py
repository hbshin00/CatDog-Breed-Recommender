from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import numpy as np

project_name = "Catdog"
net_id = "Tricia Park: tp294, Jarrett Coleman: jjc368, Hali Shin: hbs59, Matteo Savarese: mgs249, Junlin Yi: jy683"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('apartment')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query
		data = range(5)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)

def cosine(inVector, isDog, k):
	#TODO: make vectors a property of catslist and dogslist or convert
	vectors = CatsList.vectors
	if isDog:
		vectors = DogsList.vectors

	toReturn = []

	for row in vectors:
		#TODO: make vector be the relevant parts of the database row
		vector = row[3:15]
		cosine = np.dot(inVector,vector)/(np.linalg.norm(inVector)*np.linalg.norm(vector))
		#TODO: return tuple of cosine and breed name
		toReturn.append((row[0],cosine))
	toReturn = (sorted(toReturn, key = lambda x: -x[1]))
	return [x[0] for x in toReturn[:k]]



