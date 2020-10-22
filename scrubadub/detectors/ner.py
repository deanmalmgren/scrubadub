import spacy

from typing import Dict, Generator, List, Optional, Set, Sequence, Union

from .base import Detector
from ..filth import NERFilth, Filth
from ..utils import CanonicalStringSet


class SpacyDetector(Detector):
    """Use spacy's named entity recognition to clean named entities.
     List specific entities to include passing ``named_entities``, e.g.
     (PERSON)
    """
    filth_cls = NERFilth
    name = 'spacy_ner'

    disallowed_nouns = CanonicalStringSet(["skype"])

    def __init__(self, named_entities: Optional[Union[List[str], Set[str]]] = {'PERSON'},
                 model: str = "en_core_web_trf", **kwargs):
        # Spacy NER are all upper cased
        self.named_entities = {entity.upper() for entity in named_entities}
        if model not in spacy.info()['pipelines']:
            raise OSError(f"Can't find model '{model}'. If it is a valid Spacy model, "
                          f"download it (e.g. with the CLI command "
                          f"`python -m spacy download {model}`).")
        self.nlp = spacy.load(model)
        # Only enable necessary pipes
        self.nlp.select_pipes(enable=["transformer", "tagger", "parser", "ner"])
        super(SpacyDetector, self).__init__(**kwargs)

    def iter_filth_documents(self, documents: Union[Sequence[str], Dict[str, str]]) -> Generator[Filth, None, None]:
        if isinstance(documents, list):
            for doc in self.nlp.pipe(documents):
                for ent in doc.ents:
                    if ent.label_ in self.named_entities:
                        yield self.filth_cls(beg=ent.start_char,
                                             end=ent.end_char,
                                             text=ent.text,
                                             detector_name=self.name)

    def iter_filth(self, text: str, document_name: Optional[str] = None) -> Generator[Filth, None, None]:
        pass


