import numpy as np
from numpy.linalg import norm
import math

def cosin_sim(reference_vector, other_vector):
    reference_array = reference_vector.toarray().flatten()
    other_array = other_vector.toarray().flatten()

    dot_product = np.dot(reference_array, other_array)
    return dot_product / (norm(reference_array) * norm(other_array))

def calc_cosine_similarity(reference_vector, other_vectors):
    similarities=[cosin_sim(reference_vector,vector)for vector in other_vectors]
    return np.array(similarities)


