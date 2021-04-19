from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import numpy as np
import pandas as pd

project_name = "Catdog"
net_id = "Tricia Park: tp294, Jarrett Coleman: jjc368, Hali Shin: hbs59, Matteo Savarese: mgs249, Junlin Yi: jy683"


@irsystem.route('/', methods=['GET'])
def search():

	if request.args.get('dog-selected') != None or request.args.get('cat-selected') != None:
		dogs = pd.read_csv("data/dogs.csv")
		cats = pd.read_csv("data/cats.csv")

		v = make_vector(request.args)
		# v = (cats.to_numpy()[0][6:])
		results = cosine(v,5,dogs,cats)
		# print(len(results))
		# print(results)
		return render_results(results,dogs,cats)
		# print("hello")
	
	else:
		data = []
		output_message = ''
		return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)


	# query = request.args.get('apartment')
	# if not query:
	#     data = []
	#     output_message = ''
	# else:
	#     output_message = "Your search: " + query
	#     data = range(5)
	# return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)

def cosine(inVector, k, dogs, cats):
	#TODO: make vectors a property of catslist and dogslist or convert
	vectors = None
	if request.args.get('dog-selected') is not None:
		vectors = dogs.to_numpy()
	else:
		vectors = cats.to_numpy()

	print(len(vector))
	print(len(inVector))

	toReturn = []

	for row in vectors:
		#makes vector be the relevant parts of the database row
		vector = (row[6:])
		# print(len(vector))
		# print(len(inVector))
		if len(vector) != len(inVector):
			raise Exception("Vector lengths do not match")

		cosine = 0
		if np.linalg.norm(inVector) != 0 and np.linalg.norm(vector) != 0:
			cosine = np.dot(inVector,vector)/(np.linalg.norm(inVector)*np.linalg.norm(vector))
		#returns tuple of cosine and breed name
		toReturn.append((row[1],cosine))

	toReturn = (sorted(toReturn, key = lambda x: -x[1]))

	#returns list of top k breed names sorted by cosine score
	return [x[0] for x in toReturn[:k]]


def make_vector(traits):
	"""
	Input: traits (dictionary of integer traits that user inputs,
		different based on dog or cat)
	Example: {'apartment': '3', 'novice': '3', 'sensitivity': '3',
		'alone': '3', 'cold': '3', 'hot': '3', 'family-dog': '3',
		'kids-dog': '3', 'dog-friendly': '3', 'strangers': '3',
		'shedding-dog': '3', 'drool': '3', 'groom-dog': '3',
		'health-dog': '3', 'weight-gain': '3', 'size': '3',
		'train': '3', 'intelligence-dog': '3', 'mouthiness': '3',
		'prey': '3', 'noise': '3', 'wander': '3', 'energy': '3',
		'intensity': '3', 'exercise': '3', 'playful': '3'}

	Output: vector (list of ints, different based on dog or cat)
	Example: [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
	output must be in order that traits appear in dataset/website

	The "dog-selected" or "cat-selected" field will be in the input traits
	depending on if the dog form or if the cat form was selected
	"""
	output = []
	if traits.get('dog-selected') is not None:
		traits_lst = ['apartment','novice','sensitivity','alone','cold','hot',
			'family-dog','kids-dog','dog-friendly','strangers','shedding-dog',
			'drool','groom-dog','health-dog','weight-gain','size','train',
			'intelligence-dog','mouthiness','prey','noise','wander','energy',
			'intensity','exercise','playful']
	elif traits.get('cat-selected') is not None:
		traits_lst = ['family-cat','shedding-cat','health-cat','playful-cat','kids-cat',
			'groom-cat','intelligence-cat','pet-friendly']
	else:
		raise Exception("Neither dog nor cat is selected")
	for trait in traits_lst:
		int_str = traits.get(trait)
		int_int = int(int_str)
		output.append(int_int)
	return output

def render_results(results, dogs, cats):
	"""
	Input: results (list of top k breeds)
	Example: ["breed1", "breed2", "breed3"]

	Output: render_template(?)
	"""

	df = None
	if request.args.get('dog-selected') is not None:
		df = dogs
	else:
		df = cats

	output_message = "Your top " + str(len(results)) + " breeds are: "
	data = []
	for i in results:
		rel_breeds = df.loc[df['breed'] == i]
		entry = [rel_breeds["intro"]]
		entry = list(rel_breeds.to_records(index=False))
		entry.insert(0, i)
		data.append([entry[1][1], entry[1][3], entry[1][5], entry[1][4]])
		data.append([])
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)
