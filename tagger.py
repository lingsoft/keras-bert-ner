import sys
import unicodedata

import numpy as np
import tensorflow as tf

from common import process_sentences, load_ner_model
from common import encode, write_result


class Tagger(object):
    def __init__(self, model, tokenizer, labels, config):
        self.model = model
        self.tokenizer = tokenizer
        self.labels = labels
        self.config = config
        self.session = None
        self.graph = None

    def tag(self, text, tokenized=False):
        max_seq_len = self.config['max_seq_length']
        inv_label_map = {i: l for i, l in enumerate(self.labels)}
        if tokenized:
            words = text.split()    # whitespace tokenization
        else:
            words = tokenize(text)    # approximate BasicTokenizer
        dummy = ['O'] * len(words)
        data = process_sentences([words], [dummy], self.tokenizer, max_seq_len)
        x = encode(data.combined_tokens, self.tokenizer, max_seq_len)
        if self.session is None or self.graph is None:
            # assume singlethreaded
            probs = self.model.predict(x, batch_size=8)
        else:
            with self.session.as_default():
                with self.graph.as_default():
                    probs = self.model.predict(x, batch_size=8)
        preds = np.argmax(probs, axis=-1)
        pred_labels = []
        for i, pred in enumerate(preds):
            pred_labels.append([inv_label_map[t]
                                for t in pred[1:len(data.tokens[i])+1]])
        lines = write_result(
            'output.tsv', data.words, data.lengths,
            data.tokens, data.labels, pred_labels, mode='predict'
        )
        return ''.join(lines)

    @classmethod
    def load(cls, model_dir):
        # session/graph for multithreading,
        # see https://stackoverflow.com/a/54783311
        session = tf.compat.v1.Session()
        graph = tf.compat.v1.get_default_graph()
        with graph.as_default():
            with session.as_default():
                model, tokenizer, labels, config = load_ner_model(model_dir)
                tagger = cls(model, tokenizer, labels, config)
                tagger.session = session
                tagger.graph = graph
        return tagger


punct_chars = set([
    chr(i) for i in range(sys.maxunicode)
    if (unicodedata.category(chr(i)).startswith('P') or
        ((i >= 33 and i <= 47) or (i >= 58 and i <= 64) or
         (i >= 91 and i <= 96) or (i >= 123 and i <= 126)))
])

translation_table = str.maketrans({c: ' '+c+' ' for c in punct_chars})


def tokenize(text):
    return text.translate(translation_table).split()
