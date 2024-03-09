import numpy as np
from numpy.linalg import norm

# def calc_cosine_similarity(reference_vector, other_vectors):
#     # Ensure vectors have the correct shapes
#     reference_vector = reference_vector.toarray()
#     other_vectors = other_vectors.toarray()
#     print(reference_vector)
#     print("-----------")
#     print(other_vectors)
#     dot_products = np.dot(other_vectors, reference_vector.T)
#     norm_products = norm(other_vectors, axis=1) * norm(reference_vector)

#     # Avoid division by zero
#     norm_products[norm_products == 0] = 1

#     similarities = dot_products / norm_products
#     print(similarities)
#     return similarities
def cosin_sim(reference_vector, other_vector):
    reference_array = reference_vector.toarray().flatten()
    other_array = other_vector.toarray().flatten()

    dot_product = np.dot(reference_array, other_array)
    return dot_product / (norm(reference_array) * norm(other_array))

def calc_cosine_similarity(reference_vector, other_vectors):
    similarities=[cosin_sim(reference_vector,vector)for vector in other_vectors]
    return np.array(similarities)
    

