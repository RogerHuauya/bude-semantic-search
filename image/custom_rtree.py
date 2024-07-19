import numpy as np
from django.db.models import QuerySet
from rtree import index
import heapq
from sklearn.decomposition import PCA
from image.models import Image


class XRtree:
    def __init__(self):
        self.idx = None
        self.id_map = {}
        self.pca = None
        self.dimensions = None

    def fit_pca(self, embeddings, n_components=10):
        self.pca = PCA(n_components=n_components)
        reduced_embeddings = self.pca.fit_transform(embeddings)
        self.dimensions = n_components
        p = index.Property()
        p.dimension = self.dimensions
        self.idx = index.Index(properties=p)
        return reduced_embeddings

    def batch_insert(self, images: QuerySet[Image]):
        embeddings = np.array([img.embedding for img in images])
        ids = [img.id for img in images]
        reduced_embeddings = self.fit_pca(embeddings)
        for id, reduced_embedding in zip(ids, reduced_embeddings):
            self.insert(id, reduced_embedding)

    def insert(self, id, embedding):
        if len(embedding) != self.dimensions:
            raise ValueError(
                f"Embedding must be of dimension {self.dimensions}")
        self.idx.insert(id, (*embedding, *embedding))
        self.id_map[id] = embedding

    def euclidean_distance(self, point1, point2):
        return np.sqrt(np.sum((np.array(point1) - np.array(point2)) ** 2))

    def transform_pca(self, embedding):
        return self.pca.transform([embedding])[0]

    def top_k_nearest(self, point, k):
        transformed_point = self.transform_pca(point)

        if len(transformed_point) != self.dimensions:
            raise ValueError(
                f"Query point must be of dimension {self.dimensions}")

        nearest = list(self.idx.nearest((*transformed_point, *transformed_point), k))
        return nearest