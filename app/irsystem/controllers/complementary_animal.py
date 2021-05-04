import numpy as np
import pandas as pd
import pickle
import math
import csv

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
cat_vectors[56] = np.asarray([1,0,0,0,0,0,0,0])
dog_vectors[150][25] = 4

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

# max diffrence 28
num_dogs = len(altered_dog_vectors)
num_cats = len(cat_vectors)
good_companion_matrix = np.zeros((num_dogs,num_cats))
for i in range(num_dogs):
    dv = altered_dog_vectors[i]
    dv1 = dv[:7]
    dv2 = dv[7]
    for j in range(num_cats):
        cv = cat_vectors[j]
        cv1 = cv[:7]
        cv2 = cv[7]
        a = cv1-dv1
        b = np.absolute(a)
        c = np.sum(b)
        sim1 = (22-c)/22
        # pet_social_score is the combined value of both animals Pet Friendly value
        pet_social_score = dv2 + cv2
        if pet_social_score == 2:
            sim2 = -0.5
        elif pet_social_score == 3:
            sim2 = -0.3
        elif pet_social_score == 4:
            sim2 = -0.1
        elif pet_social_score == 5:
            sim2 = 0
        elif pet_social_score == 6:
            sim2 = 0.25
        elif pet_social_score == 7:
            sim2 = 0.5
        elif pet_social_score == 8:
            sim2 = 0.75
        elif pet_social_score == 9:
            sim2 = 0.9
        elif pet_social_score == 10:
            sim2 = 1.1
        else:
            sim2 = 0
        sim3 = (sim1*0.65) + (sim2 * 0.35)
        if sim3 < 0.05:
            sim4 = 0.05
        else:
            sim4 = sim3
        sim = round(sim4,2)
        good_companion_matrix[i,j] = sim

df = pd.DataFrame(good_companion_matrix)
df.to_csv('data/matrix.csv')

# with open("good_companion_matrix.pickle","wb") as fp:
#     pickle.dump(good_companion_matrix, fp)


# Affectionate with Family [6],Amount of Shedding [10],General Health [13],
# Potential for Playfulness [25],Kid-Friendly [7],Easy to Groom [12],Intelligence [17], Pet Friendly [8]

# Adapts Well To Apartment Living 0 ,Good For Novice Owners 1,Sensitivity Level 2 ,Tolerates Being Alone 3,
# Tolerates Cold Weather 4 ,Tolerates Hot Weather 5, Affectionate With Family 6, Kid-Friendly 7,Dog Friendly 8,
# Friendly Toward Strangers 9,Amount Of Shedding 10 ,Drooling Potential 11, Easy To Groom 12,General Health 13,
# Potential For Weight Gain 14 ,Size 15,Easy To Train 16, Intelligence 17, Potential For Mouthiness 18,
# Prey Drive 19, Tendency To Bark Or Howl 20, Wanderlust Potential 22 ,Energy Level 23,
# Intensity 23, Exercise Needs 24, Potential For Playfulness 25







