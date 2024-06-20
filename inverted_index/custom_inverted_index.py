import os
import json
import heapq
import csv
import pandas as pd
import numpy as np
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from collections import Counter, defaultdict

from typing import List, Any, Dict, DefaultDict, Tuple
from pandas.io.parsers import TextFileReader
from django.core.files.base import ContentFile

from .models import IndexFile



src_dir = os.path.abspath(
    os.path.dirname(__file__))  # Directorio del archivo actual
data_dir = os.path.join(src_dir, os.pardir, 'data')  # Directorio de los datos
blocks_dir = os.path.join(data_dir, 'blocks')  # Directorio de los bloques

tf_idf_json = os.path.join(data_dir, 'tf_idf.json')  # Archivo de los tf-idf
doc_norms_json = os.path.join(data_dir,
                              'doc_norms.json')  # Archivo de las normas de los documentos


class InvertedIndex:  # Clase que representa el índice invertido
    def __init__(self, file_name: str, index_col: str, block_size: int,
                 lang: str = "english") -> None:
        nltk.download('stopwords')  # Descargar stopwords
        nltk.download('punkt')  # Descargar tokenizer
        self.file_name: str = file_name  # Nombre del archivo
        self.block_size: int = block_size  # Tamaño de los bloques
        self.stemmer = SnowballStemmer(lang)  # Stemmer
        self.stoplist: List[str] = stopwords.words(lang)  # Stopwords

        self.df: Dict[str, int] = defaultdict(int)  # Frecuencia de documentos
        # self.n_blocks: int = 0 # tmp
        self.n_blocks: int = 5  # tmp # Número de bloques
        self.block_size_list: List[int] = []  # Lista de tamaños de los bloques
        self.build_index(index_col, lang)  # Construir el índice invertido
        self.compute_doc_norms()  # Compute and save document norms

    def build_index(self, index_col: str, lang: str) -> None:
        read_path = os.path.join(self.file_name)
        chunks: TextFileReader = pd.read_csv(read_path,
                                             chunksize=self.block_size,
                                             usecols=[index_col, 'language'])
        os.makedirs(os.path.join(data_dir, 'blocks'), exist_ok=True)
        num_documents = 0
        for i, chunk in enumerate(chunks, start=1):
            BM = (chunk['language'] == lang[:2]) & (pd.notna(chunk[index_col]))
            partial_index: DefaultDict[str, Counter] = defaultdict(Counter)
            for idx, doc in chunk[BM].iterrows():
                num_documents += 1
                try:
                    partial_counter = self.preprocess(doc.iloc[0])
                except Exception as e:
                    print(f"Error at {idx = },{i = }")
                for word, tf in partial_counter.items():
                    partial_index[word][idx] = tf
                    self.df[word] += 1

            ordered_partial_index: Dict[str, Dict[str, int]] = {}
            self.block_size_list.append(0)
            for term, posting in sorted(partial_index.items()):
                ordered_partial_index[term] = dict(sorted(posting.items()))
                self.block_size_list[i - 1] += len(posting)

            self.write_block(ordered_partial_index, block_num=i, height=0)

        with open(os.path.join(data_dir, 'block_sizes.json'), 'w',
                  encoding='utf-8') as file:
            json.dump(self.block_size_list, file, indent=4)
        # print(f"Blocks created: {i = }")
        self.n_blocks = i
        self.merge_blocks()
        self.compute_idf(num_documents)

    def merge_blocks(self) -> None:
        # self.block_size_list = json.load(open(os.path.join(data_dir, 'block_sizes.json'), 'r', encoding='utf-8'))
        # esa carga no debería estar
        # print(f"{self.n_blocks = }")
        self.mergesort(1, self.n_blocks)

    def mergesort(self, p: int, r: int) -> int:
        if p > r:
            return -1
        if p == r:
            return -1
        q = (p + r) // 2
        left_h: int = self.mergesort(p, q)
        right_h: int = self.mergesort(q + 1, r)
        h: int = max(left_h, right_h) + 1
        self.merge(p, q, r, h)
        return h

    def merge(self, p: int, q: int, r: int, height: int) -> None:
        nl: int = q - p + 1
        nr: int = r - q

        i_ext: int = 0
        j_ext: int = 0

        while i_ext < nl and j_ext < nr:
            d1, blockl_k, blockl_v, sizel = self.load_block(
                block_num=p + i_ext, height=height)
            d2, blockr_k, blockr_v, sizer = self.load_block(
                block_num=q + j_ext, height=height + 1)
            new_block: Dict[str, Dict[str, int]] = self.merge_dicts(d1, d2)

            split_size = (sizel + sizer) // 2
            block1, block2 = self.split_dict(new_block, split_size)

            self.write_block(block1, p + i_ext, height + 1)
            self.write_block(block2, q + j_ext, height + 1)

            i_ext += 1
            j_ext += 1

        while i_ext < nl:
            d1, blockl_k, blockl_v, sizel = self.load_block(p + i_ext, height)
            self.write_block(d1, p + i_ext, height + 1)
            i_ext += 1

        while j_ext < nr:
            d2, blockr_k, blockr_v, sizer = self.load_block(q + j_ext,
                                                            height + 1)
            self.write_block(d2, q + j_ext, height + 1)
            j_ext += 1

    def merge_dicts(self, d1: Dict[str, Dict[str, int]],
                    d2: Dict[str, Dict[str, int]]) -> Dict[
        str, Dict[str, int]]:
        merged: Dict[str, Dict[str, int]] = {}
        keys1: List[str] = list(d1.keys())
        keys2: List[str] = list(d2.keys())

        i, j = 0, 0
        while i < len(keys1) and j < len(keys2):
            if keys1[i] < keys2[j]:
                merged[keys1[i]] = d1[keys1[i]]
                i += 1
            elif keys1[i] > keys2[j]:
                merged[keys2[j]] = d2[keys2[j]]
                j += 1
            else:  # keys1[i] == keys2[j]
                merged[keys1[i]] = {}
                nested_keys1: List[str] = list(d1[keys1[i]].keys())
                nested_keys2: List[str] = list(d2[keys1[i]].keys())

                k, l = 0, 0
                while k < len(nested_keys1) and l < len(nested_keys2):
                    if nested_keys1[k] < nested_keys2[l]:
                        merged[keys1[i]][nested_keys1[k]] = d1[keys1[i]][
                            nested_keys1[k]]
                        k += 1
                    elif nested_keys1[k] > nested_keys2[l]:
                        merged[keys1[i]][nested_keys2[l]] = d2[keys1[i]][
                            nested_keys2[l]]
                        l += 1
                    else:  # nested_keys1[k] == nested_keys2[l]
                        merged[keys1[i]][nested_keys1[k]] = d2[keys1[i]][
                            nested_keys2[l]]
                        k += 1
                        l += 1

                while k < len(nested_keys1):
                    merged[keys1[i]][nested_keys1[k]] = d1[keys1[i]][
                        nested_keys1[k]]
                    k += 1

                while l < len(nested_keys2):
                    merged[keys1[i]][nested_keys2[l]] = d2[keys1[i]][
                        nested_keys2[l]]
                    l += 1

                i += 1
                j += 1

        while i < len(keys1):
            merged[keys1[i]] = d1[keys1[i]]
            i += 1

        while j < len(keys2):
            merged[keys2[j]] = d2[keys2[j]]
            j += 1

        return merged

    def split_dict(self, input_dict: Dict[str, Dict[str, int]],
                   split_size: int) -> Tuple[
        Dict[str, Dict[str, int]], Dict[str, Dict[str, int]]]:
        dict1 = {}
        dict2 = {}
        current_size = 0

        for key, value in input_dict.items():
            if current_size < split_size:
                dict1[key] = value
                current_size += len(value)
            else:
                dict2[key] = value
        return dict1, dict2

    def write_block(self, block: Dict[str, Dict[str, int]], block_num: int,
                    height: int) -> None:
        block_content = json.dumps(block, indent=4)
        file_name = f"block_{block_num}__height_{height}.json"

        index_file, created = IndexFile.objects.get_or_create(
            block_number=block_num,
            height=height
        )
        index_file.file.save(file_name, ContentFile(block_content), save=True)

    def load_block(self, block_num: int, height: int = 0) -> Tuple[
        Dict[str, Dict[str, int]], List[str], List[Dict[str, int]], int]:
        print(f"Loading block {block_num} at height {height}")
        index_file = IndexFile.objects.get(block_number=block_num,
                                           height=height)
        block_content = index_file.file.read()
        block_index = json.loads(block_content)
        docsizes = sum(len(posting) for posting in block_index.values())
        keys = list(block_index.keys())
        values = list(block_index.values())
        return block_index, keys, values, docsizes

    def compute_idf(self, num_documents: int) -> None:
        idf: Dict[str, float] = {}
        for term, doc_freq in self.df.items():
            idf[term] = np.log(num_documents / doc_freq)
        with open(tf_idf_json, 'w', encoding='utf-8') as file:
            json.dump(idf, file, indent=4)

    def compute_doc_norms(self) -> None:
        doc_norms: Dict[int, float] = defaultdict(float)
        for i in range(1, self.n_blocks + 1):
            block_path = os.path.join(blocks_dir, f"block_{i}__height_0.json")
            if not os.path.exists(block_path):
                continue
            with open(block_path, 'r', encoding='utf-8') as file:
                block_index = json.load(file)
                for term, postings in block_index.items():
                    for doc_id, tf in postings.items():
                        doc_norms[int(doc_id)] += tf ** 2

        for doc_id in doc_norms:
            doc_norms[doc_id] = np.sqrt(doc_norms[doc_id])

        with open(doc_norms_json, 'w', encoding='utf-8') as file:
            json.dump(doc_norms, file, indent=4)

    def preprocess(self, doc: str) -> Dict[str, int]:
        words: List[str] = word_tokenize(doc.lower())
        words_f: List[str] = [w for w in words if
                              w not in self.stoplist and w.isalpha()]
        return Counter([self.stemmer.stem(w) for w in words_f])

    def query(self, query_str: str, k: int) -> List[Tuple[int, float]]:
        query_counter = self.preprocess_query(query_str)
        total_docs = sum(self.block_size_list)
        query_tf_idf = self.compute_query_tf_idf(query_counter, total_docs)
        relevant_docs = self.get_relevant_docs(list(query_counter.keys()))

        with open(doc_norms_json, 'r') as f:
            doc_norms = json.load(f)

        similarities = self.compute_cosine_similarity(query_tf_idf,
                                                      relevant_docs, doc_norms)

        # Obtener los k documentos más relevantes
        return heapq.nlargest(k, similarities, key=lambda x: x[1])

    def preprocess_query(self, query: str) -> Dict[str, int]:
        words: List[str] = word_tokenize(query.lower())
        words_f: List[str] = [w for w in words if
                              w not in self.stoplist and w.isalpha()]
        return Counter([self.stemmer.stem(w) for w in words_f])

    def compute_query_tf_idf(self, query_counter: Dict[str, int],
                             total_docs: int) -> Dict[str, float]:
        tf_idf_query = {}
        with open(tf_idf_json, 'r') as f:
            idf = json.load(f)

        for term, tf in query_counter.items():
            if term in idf:
                tf_idf_query[term] = tf * idf[term]

        return tf_idf_query

    def get_relevant_docs(self, query_terms: List[str]) -> Dict[
        int, Dict[str, int]]:
        relevant_docs = defaultdict(dict)
        for term in query_terms:
            block_num, height = 1, 0
            while True:
                block_path = os.path.join(blocks_dir,
                                          f"block_{block_num}__height_{height}.json")
                if not os.path.exists(block_path):
                    break
                with open(block_path, 'r', encoding='utf-8') as file:
                    block_index = json.load(file)
                    if term in block_index:
                        for doc_id, tf in block_index[term].items():
                            relevant_docs[doc_id][term] = tf
                block_num += 1
        return relevant_docs

    def compute_cosine_similarity(self, query_tf_idf: Dict[str, float],
                                  relevant_docs: Dict[int, Dict[str, int]],
                                  doc_norms: Dict[int, float]) -> List[
        Tuple[int, float]]:
        cosine_similarities = []
        query_norm = np.sqrt(
            sum(value ** 2 for value in query_tf_idf.values()))
        if query_norm == 0:
            return []

        for doc_id, terms in relevant_docs.items():
            up = 0
            down1 = 0
            down2 = 0
            for term, tf in terms.items():
                if term in query_tf_idf:
                    up += query_tf_idf[term] * tf
                    down1 += query_tf_idf[term] ** 2
                    down2 += tf ** 2

            down = np.sqrt(down1) * np.sqrt(down2)

            if down != 0:
                cosine_similarity = up / down
                cosine_similarities.append((doc_id, cosine_similarity))

        return cosine_similarities

    def get_lyrics_from_doc_ids(doc_ids: List[int], file_name: str) -> List[
        str]:
        lyrics = []
        chunks: TextFileReader = pd.read_csv(os.path.join(data_dir, file_name),
                                             chunksize=1000,
                                             usecols=['id', 'lyrics'])
        for chunk in chunks:
            for doc_id in doc_ids:
                lyrics_chunk = chunk[chunk['id'] == doc_id]['lyrics']
                if not lyrics_chunk.empty:
                    lyrics.append(lyrics_chunk.values[0])
                    if len(lyrics) == len(doc_ids):
                        return lyrics
        return lyrics


def get_lyrics_by_id(doc_id):
    direccion = "spotify_songs.csv"
    with open(os.path.join(data_dir, direccion), newline='',
              encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        try:
            # Convertir doc_id a entero para acceder al índice correcto (considerando que el ID es la posición)
            doc_id_int = int(doc_id)
            # Saltar las primeras líneas hasta llegar al índice deseado (doc_id_int)
            for _ in range(doc_id_int):
                next(reader)
            # Leer la línea deseada
            next(reader)
            row = next(reader)
            return row[3]  # Devolver el campo 'lyrics'
        except (ValueError, IndexError):
            return None  # Manejar errores si el ID no es válido o está fuera de rango


if __name__ == "__main__":
    xd: InvertedIndex = InvertedIndex("spotify_songs.csv", "lyrics", 4000)
    results = xd.query("bed", k=10)
    # for doc_id, score in results:
    #     print(f"Document ID: {doc_id}, Score: {score}")

    lyrics = []
    for n, _ in results:
        lyrics.append(get_lyrics_by_id(n))

    for i in lyrics:
        print(i)
