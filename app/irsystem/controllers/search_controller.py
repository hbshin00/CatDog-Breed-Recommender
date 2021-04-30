from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd

project_name = "Catdog"
net_id = "Tricia Park: tp294, Jarrett Coleman: jjc368, Hali Shin: hbs59, Matteo Savarese: mgs249, Junlin Yi: jy683"
rocchioText = ''
rocchioVector = None
rocchioRel = []
rocchioNonRel = []

@irsystem.route('/', methods=['GET'])
def search():

	if request.args.get('dog-selected') != None or request.args.get('cat-selected') != None:
		dogs = pd.read_csv("data/dogs.csv")
		cats = pd.read_csv("data/cats.csv")

		v = make_vector(request.args)
		rocchioVector = v
		rocchioText = request.args.get('physical')
		results = sim(v,request.args.get('physical'),5,dogs,cats)
		return render_results(results,dogs,cats)
	elif request.args.get('rocchio-selected')!= None:
		v = rocchio(rocchioVector,rocchioRel,rocchioNonRel)
		t = rocchioText
		results = sim(v,t,5,dogs,cats)
		return render_results(results,dogs,cats)
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

def rocchio(input,rel, nonrel):
	#used these from assignment 5
	a = .3
	b = .3
	c = .8
	relSum = None
	nonrelSum = None
	bterm = None
	cterm = None

	if len(rel) != 0:
		relSum = np.zeros(len(rel[0]))
		nonrelSum = np.zeros(len(rel[0]))
		bterm = np.zeros(len(rel[0]))
		cterm = np.zeros(len(rel[0]))
	else:
		relSum = np.zeros(len(nonrel[0]))
		nonrelSum = np.zeros(len(nonrel[0]))
		bterm = np.zeros(len(nonrel[0]))
		cterm = np.zeros(len(nonrel[0]))
	
	for r in rel:
		relSum += r
	for nr in nonrel:
		nonrelSum += nr

	if len(rel) != 0:
        bTerm = b*relSum/len(rel)
    if len(nonrel) != 0:
        cTerm = c*nonrelSum/len(rel)
	
	toReturn = a*input + bterm - cterm
	return np.clip(toReturn,0,None)

def makeTFIDF(csv, input):
	vectorizer = TfidfVectorizer(
    stop_words="english",
    max_df=0.8,
    min_df=10
	)
	descriptions = csv["description"].tolist()
	descriptions.append(input)
	return vectorizer.fit_transform(descriptions).toarray()

def sim(inVector, intext, k, dogs, cats):
	#TODO: make vectors a property of catslist and dogslist or convert
	vectors = None
	matrix = None
	if request.args.get('dog-selected') is not None:
		vectors = dogs.to_numpy()
		matrix = makeTFIDF(dogs, intext)
	else:
		vectors = cats.to_numpy()
		matrix = makeTFIDF(cats, intext)
	intextVector = matrix[-1]

	toReturn = {}
	ranking = []
	textRank = []
	rankShift = {}
	for i in range(len(vectors)):
		row = vectors[i]
		#makes vector be the relevant parts of the database row
		vector = (row[7:])
		textVector = matrix[i]
		rank = row[2]
		# print(i)
		# print(rank)
		#divide rank into 8 groups, then turn shift into float based on max value
		rankShift[row[1]] = 1-float(int(rank*8/200))/200

		# print(len(vector))
		# print(len(inVector))
		if len(vector) != len(inVector):
			raise Exception("Vector lengths do not match")

		similarity = np.linalg.norm(inVector-vector)
		textSim = 0
		if np.linalg.norm(intextVector) != 0 and np.linalg.norm(textVector) != 0:
			textSim = np.dot(intextVector,textVector)/np.linalg.norm(intextVector)/np.linalg.norm(textVector)

		#returns tuple of similarity and breed name
		ranking.append((row[1],similarity))
		textRank.append((row[1],textSim))

	ranking = (sorted(ranking, key = lambda x: x[1]))
	textRank = (sorted(textRank, key = lambda x: -x[1]))

	for i in range(len(ranking)):
		if ranking[i][0] in toReturn:
			toReturn[ranking[i][0]] = (toReturn[ranking[i][0]] + i)/2 + rankShift[ranking[i][0]]
		else:
			toReturn[ranking[i][0]] = i
		if textRank[i][0] in toReturn:
			toReturn[textRank[i][0]] = (toReturn[textRank[i][0]] + i)/2 + rankShift[textRank[i][0]]
		else:
			toReturn[textRank[i][0]] = i
	toReturnSorted = [k for k,v in sorted(toReturn.items(),key = lambda x: x[1])]
	#returns list of top k breed names sorted by similarity score
	return [x for x in toReturnSorted[:k]]



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
