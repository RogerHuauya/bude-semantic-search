from django.core.management.base import BaseCommand
from image.models import Image
from image.custom_rtree import XRtree
import numpy as np


class Command(BaseCommand):
    help = 'Test command for XRtree with CPA'

    def handle(self, *args, **kwargs):
        print("Rtree with CPA!")

        # Obtener los primeros 10 registros de la base de datos
        queryset = Image.objects.all()[:3000]
        var = []
        for img in queryset:
            var.append({"title": img.title, "vector": img.embedding, "id": img.id})

        
        BudeRtree = XRtree()
        print(var[9])

         # Extract embeddings and IDs
        embeddings = np.array([item["vector"] for item in var])
        ids = [item["id"] for item in var]

        # Fit PCA
        reduced_embeddings = BudeRtree.fit_pca(embeddings)

        # Insert reduced embeddings into R-Tree
        for id, reduced_embedding in zip(ids, reduced_embeddings):
            BudeRtree.insert(id, reduced_embedding)

        # Query the R-Tree (Prueba)

        query_embedding = embeddings[9]

        nearest_ids = BudeRtree.top_k_nearest(query_embedding, 3)

        print(f"Top 3 nearest neighbors to image 0: {nearest_ids}")