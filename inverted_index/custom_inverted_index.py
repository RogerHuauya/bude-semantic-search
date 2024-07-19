import csv
from typing import List, Any, Dict, DefaultDict, Tuple
from pandas.io.parsers import TextFileReader
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from collections import Counter, defaultdict
import os
import json
import heapq

from django.conf import settings

nltk.download('stopwords')  # Descargar stopwords
nltk.download('punkt')  # Descargar tokenizer

src_dir = os.path.abspath(settings.BASE_DIR)
data_dir = os.path.join(src_dir)  # Directorio de los datos
blocks_dir = os.path.join(data_dir, 'blocks')  # Directorio de los bloques

tf_idf_json = os.path.join(data_dir, 'tf_idf.json')  # Archivo de los tf-idf
doc_norms_json = os.path.join(data_dir, 'doc_norms.json')  # Archivo de las normas de los documentos


class InvertedIndex:  # Clase que representa el índice invertido
    def __init__(self, file_name: str, index_col: str, block_size: int, lang: str = "english") -> None:
        self.file_name: str = file_name  # Nombre del archivo
        self.block_size: int = block_size  # Tamaño de los bloques
        self.stemmer = SnowballStemmer(lang)  # Stemmer
        self.stoplist: List[str] = stopwords.words(lang)  # Stopwords

        self.df: Dict[str, int] = defaultdict(int)  # Frecuencia de documentos
        self.n_blocks: int = 0  # Número de bloques
        self.block_size_list: List[int] = []  # Lista de tamaños de los bloques
        self.build_index(index_col, lang)  # Construir el índice invertido
        self.compute_doc_norms()  # Compute and save document norms

    def build_index(self, index_col: str, lang: str) -> None:
        read_path = os.path.join(data_dir, self.file_name)
        chunks: TextFileReader = pd.read_csv(read_path, chunksize=self.block_size, usecols=[index_col, 'language'])
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

        with open(os.path.join(data_dir, 'block_sizes.json'), 'w', encoding='utf-8') as file:
            json.dump(self.block_size_list, file, indent=4)
        self.n_blocks = i
        self.merge_split()
        self.compute_idf(num_documents)

    def merge_split(self) -> None:
        total_index: Dict[str, Dict[str, int]] = {}
        for i in range(1, self.n_blocks+1):
            block_index, _ = self.load_block(i)
            total_index.update(block_index)

        sorted_keys = sorted(total_index.keys())
        total_index_ordered = {k: total_index[k] for k in sorted_keys}
        total_keys = len(sorted_keys)
        part_size = total_keys // self.n_blocks
        remaining = total_keys % self.n_blocks

        start_index = 0
        for i in range(1, self.n_blocks+1):
            end_index = start_index + part_size + (1 if i < remaining else 0)
            part_keys = sorted_keys[start_index:end_index]
            self.write_block({k: total_index_ordered[k] for k in part_keys}, i, 1)
            start_index = end_index


    def write_block(self, block: Dict[str, Dict[str, int]], block_num: int, height: int) -> None:
        block_path = os.path.join(blocks_dir, f"block_{block_num}__height_{height}.json")
        print(f"Writing block to path: {block_path}")  # Added for debugging
        with open(block_path, 'w', encoding='utf-8') as file:
            json.dump(block, file, indent=4)
        print(f"Block {block_num} written successfully")  # Added for debugging

    def load_block(self, block_num: int, height: int = 0) -> Tuple[Dict[str, Dict[str, int]], int]:
        block_path = os.path.join(blocks_dir, f"block_{block_num}__height_{height}.json")
        print(f"Loading block from path: {block_path}")  # Added for debugging
        with open(block_path, 'r', encoding='utf-8') as file:
            block_index: Dict[str, Dict[str, int]] = json.load(file)
            docsizes: int = sum(len(posting) for posting in block_index.values())
        return block_index, docsizes

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
        words_f: List[str] = [w for w in words if w not in self.stoplist and w.isalpha()]
        return Counter([self.stemmer.stem(w) for w in words_f])

    def query(self, query_str: str, k: int) -> List[Tuple[int, float]]:
        query_counter = self.preprocess_query(query_str)
        total_docs = sum(self.block_size_list)
        query_tf_idf = self.compute_query_tf_idf(query_counter, total_docs)
        relevant_docs = self.get_relevant_docs(list(query_counter.keys()))

        with open(doc_norms_json, 'r') as f:
            doc_norms = json.load(f)

        similarities = self.compute_cosine_similarity(query_tf_idf, relevant_docs, doc_norms)

        return heapq.nlargest(k, similarities, key=lambda x: x[1])

    def preprocess_query(self, query: str) -> Dict[str, int]:
        words: List[str] = word_tokenize(query.lower())
        words_f: List[str] = [w for w in words if w not in self.stoplist and w.isalpha()]
        return Counter([self.stemmer.stem(w) for w in words_f])

    def compute_query_tf_idf(self, query_counter: Dict[str, int], total_docs: int) -> Dict[str, float]:
        tf_idf_query = {}
        with open(tf_idf_json, 'r') as f:
            idf = json.load(f)

        for term, tf in query_counter.items():
            if term in idf:
                tf_idf_query[term] = tf * idf[term]

        return tf_idf_query

    def get_relevant_docs(self, query_terms: List[str]) -> Dict[int, Dict[str, int]]:
        relevant_docs = defaultdict(dict)
        for term in query_terms:
            block_num, height = 1, 0
            while True:
                block_path = os.path.join(blocks_dir, f"block_{block_num}__height_{height}.json")
                if not os.path.exists(block_path):
                    break
                with open(block_path, 'r', encoding='utf-8') as file:
                    block_index = json.load(file)
                    if term in block_index:
                        for doc_id, tf in block_index[term].items():
                            relevant_docs[doc_id][term] = tf
                block_num += 1
        return relevant_docs

    def compute_cosine_similarity(self, query_tf_idf: Dict[str, float], relevant_docs: Dict[int, Dict[str, int]], doc_norms: Dict[int, float]) -> List[Tuple[int, float]]:
        cosine_similarities = []
        query_norm = np.sqrt(sum(value ** 2 for value in query_tf_idf.values()))
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

    def get_lyrics_from_doc_ids(self, doc_ids: List[int], file_name: str) -> List[str]:
        lyrics = []
        chunks: TextFileReader = pd.read_csv(os.path.join(data_dir, file_name), chunksize=1000, usecols=['id', 'lyrics'])
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
    with open(os.path.join(data_dir, direccion), newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        try:
            doc_id_int = int(doc_id)
            for _ in range(doc_id_int):
                next(reader)
            next(reader)
            row = next(reader)
            return row[3]
        except (ValueError, IndexError):
            return None


def get_song_by_id(doc_id):
    direccion = "spotify_songs.csv"
    with open(os.path.join(data_dir, direccion), newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        try:
            doc_id_int = int(doc_id)
            for _ in range(doc_id_int):
                next(reader)
            row = next(reader)
            return row
        except (ValueError, IndexError):
            return None


if __name__ == "__main__":
    xd: InvertedIndex = InvertedIndex("spotify_songs.csv", "lyrics", 4000)
    results = xd.query("john mayer", k=1)

    lyrics = []
    for n, _ in results:
        lyrics.append(get_lyrics_by_id(n))

    for i in lyrics:
        print(i) # Imprimir las letras de las canciones
