import sys

from flask import Flask, request

from common import argument_parser
from tagger import Tagger


DEFAULT_MODEL_DIR = 'ner-model'
app = Flask(__name__)
tagger = Tagger.load(DEFAULT_MODEL_DIR)


@app.route('/', methods=["GET", "POST"])
def tag():
    text = request.values['text']
    tokenized = request.values.get('tokenized') in ('1', 'True', 'true')
    return tagger.tag(text, tokenized)


def main(argv):
    argparser = argument_parser('serve')
    args = argparser.parse_args(argv[1:])
    app.run(host="0.0.0.0", port=args.port)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
