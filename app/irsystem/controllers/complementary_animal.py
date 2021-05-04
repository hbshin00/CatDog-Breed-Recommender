# from . import *
import numpy as np
import pandas as pd
import pickle

df1 = pd.read_csv("data/dogs.csv")
dog_data = df1.values.tolist()
df2 = pd.read_csv("data/cats.csv")
cat_data = df2.values.tolist()

dog_vectors = []
cat_vectors = []
for dog in dog_data:
    vector_list = dog[7:]
    dog_vectors.append(vector_list)
for cat in cat_data:
    vector_list = cat[7:]
    vector = np.asarray(vector_list)
    cat_vectors.append(vector)

altered_dog_vectors = []
# Affectionate with Family [6],Amount of Shedding [10],General Health [13],
# Potential for Playfulness [25],Kid-Friendly [7],Easy to Groom [12],Intelligence [17], Pet Friendly [8]
for vector in dog_vectors:
    a = vector[6]
    b = vector[10]
    c = vector[13]
    d = vector[25]
    e = vector[7]
    f = vector[12]
    g = vector[17]
    h = vector[8]
    new_vector_list = [a,b,c,d,e,f,g,h]
    new_vector = np.asarray(new_vector_list)
    altered_dog_vectors.append(new_vector)

num_dogs = len(altered_dog_vectors)
num_cats = len(cat_vectors)
good_companion_matrix = np.zeros((num_dogs,num_cats))
for i in range(num_dogs):
    dv = altered_dog_vectors[i]
    for j in range(num_cats):
        cv = cat_vectors[j]
        a = cv-dv
        b = np.absolute(a)
        c = np.sum(b)
        sim = (32-c)/32
        good_companion_matrix[i,j] = sim

df = pd.DataFrame(good_companion_matrix)
df.to_csv('data/matrix.csv')

# with open("good_companion_matrix.pickle","wb") as fp:
#     pickle.dump(good_companion_matrix, fp)

# pickle.load rb


# Affectionate with Family [6],Amount of Shedding [10],General Health [13],
# Potential for Playfulness [25],Kid-Friendly [7],Easy to Groom [12],Intelligence [17], Pet Friendly [8]

# Adapts Well To Apartment Living 0 ,Good For Novice Owners 1,Sensitivity Level 2 ,Tolerates Being Alone 3,
# Tolerates Cold Weather 4 ,Tolerates Hot Weather 5, Affectionate With Family 6, Kid-Friendly 7,Dog Friendly 8,
# Friendly Toward Strangers 9,Amount Of Shedding 10 ,Drooling Potential 11, Easy To Groom 12,General Health 13,
# Potential For Weight Gain 14 ,Size 15,Easy To Train 16, Intelligence 17, Potential For Mouthiness 18,
# Prey Drive 19, Tendency To Bark Or Howl 20, Wanderlust Potential 22 ,Energy Level 23,
# Intensity 23, Exercise Needs 24, Potential For Playfulness 25







