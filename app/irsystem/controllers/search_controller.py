from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "Catdog"
net_id = "Tricia Park: tp294, Jarrett Coleman: jjc368, Hali Shin: hbs59, Matteo Savarese: mgs249, Junlin Yi: jy683"

@irsystem.route('/', methods=['GET'])
def search():

	# make_vector(request.args)
	# render_results(results)

	# print(request.args)

	query = request.args.get('apartment')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query
		data = range(5)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)


def make_vector(traits):
	"""
	Input: traits (dictionary of integer traits that user inputs, different based on dog or cat)
	Example: [('apartment', '3'), ('novice', '3'), ('sensitivity', '3'), ('alone', '3'), ('cold', '3'), ('hot', '3'), ('family-dog', '3'), ('kids-dog', '3'), ('dog-friendly', '3'), ('strangers', '3'), ('shedding-dog', '3'), ('drool', '3'), ('groom-dog', '3'), ('health-dog', '3'), ('weight-gain', '3'), ('size', '3'), ('train', '3'), ('intelligence-dog', '3'), ('mouthiness', '3'), ('prey', '3'), ('noise', '3'), ('wander', '3'), ('energy', '3'), ('intensity', '3'), ('exercise', '3'), ('playful', '3')]
	
	Output: vector (list of ints, different based on dog or cat)
	Example: [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]

	The "dog-selected" or "cat-selected" field will be in the input traits 
	depending on if the dog form or if the cat form was selected
	"""
	output = []
	if request.args.get('dog-selected') is not None:
		# process input for dog form
		continue
	elif request.args.get('cat-selected') is not None:
		# process input for cat form
		continue
	return output

def render_results(results):
	"""
	Input: results (list of top k breeds)
	Example: ["breed1", "breed2", "breed3"]

	Output: render_template(?)
	"""
	# return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)
	raise NotImplementedError()