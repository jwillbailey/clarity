import argparse
import glob
import itertools
import json
import logging
from pathlib import Path
import re

import jiwer  # package for computing WER

logging.basicConfig(level=logging.INFO)


class MySubstituteWords(jiwer.AbstractTransform):
    """Replacement for jiwer's substitute transform that is much faster"""

    def __init__(self, substitutions):
        self.substitutions = substitutions

    def process_string(self, s):
        for word in s.split():
            if word not in self.substitutions:
                logging.info(f"OOV word: {word}")

        return " ".join(
            [
                self.substitutions[word] if (word in self.substitutions) else word
                for word in s.split()
            ]
        )

    def process_list(self, inp):
        return [self.process_string(s) for s in inp]


class MyRemovePunctuation(jiwer.AbstractTransform):
    """Replacement for jiwer's remove punctuation that allows more control."""

    def __init__(self, symbols):
        self.substitutions = f"[{symbols}]"

    def process_string(self, s):
        return re.sub(self.substitutions, "", s)

    def process_list(self, inp):
        return [self.process_string(s) for s in inp]


class PronDictionary:
    """Class to hold the pronunciation dictionary"""

    def __init__(self, filename):
        self.pron_dict = {}
        self.add_dict(filename)

    def add_dict(self, filename):
        with open(filename, "r", encoding="utf8") as f:
            lines = [line.strip() for line in f.readlines() if line[0] != "#"]
        pairs = [re.split("\t+", line) for line in lines]
        new_dict = {pair[0].strip(): pair[1] for pair in pairs if len(pair) == 2}
        self.pron_dict.update(new_dict)

    def lookup(self, word, sep=None):
        word_upper = word.upper()
        try:
            pron = self.pron_dict[word.upper()]
        except KeyError:
            logging.info(f"OOV word: {word_upper}")
            pron = word_upper
        if sep:
            pron = re.sub(" ", sep, pron)
        return pron


class Contractions:
    """Class to handle alternative spellings for contractions, e.g. don't vs do not"""

    def __init__(self, contraction_file):
        with open(contraction_file, "r") as f:
            contractions = [line.strip().split(", ") for line in f.readlines()]
        self.contract_dict = {v: k for k, v in contractions} | {k: v for k, v in contractions}
        self.contra_re = re.compile(
            "(" + "|".join(["\\b" + k + "\\b" for k in self.contract_dict.keys()]) + ")"
        )

    def make_sentence_forms(self, sentence):
        parts = re.split(self.contra_re, sentence.lower())
        # Filter out empty strings
        parts = [p for p in parts if p != ""]
        # ["I have"] -> ["I have", "I've"] etc
        parts = [[p, self.contract_dict[p]] if (p in self.contract_dict) else [p] for p in parts]
        # Make all possible sentences with contracted and uncontracted word forms
        sentence_forms = ["".join(s) for s in itertools.product(*parts)]
        return sentence_forms


class SentenceScorer:
    def __init__(self, pron_dict=None, contractions=None):
        self.transformation = jiwer.Compose(
            [
                jiwer.RemoveKaldiNonWords(),
                jiwer.Strip(),
                MyRemovePunctuation(";!*#,?.’‘"),
                jiwer.ToUpperCase(),
                jiwer.RemoveMultipleSpaces(),
                jiwer.RemoveWhiteSpace(replace_by_space=True),
                jiwer.SentencesToListOfWords(word_delimiter=" "),
            ]
        )
        self.phoneme_transformation = None
        if pron_dict is not None:
            self.transformation = jiwer.Compose(
                [self.transformation, MySubstituteWords(pron_dict.pron_dict)]
            )
            self.phoneme_transformation = jiwer.Compose(
                [self.transformation, jiwer.SentencesToListOfWords(word_delimiter=" ")]
            )

        self.contractions = contractions

    def get_word_sequence(self, sentence):
        return self.transformation(sentence)

    def get_phoneme_sequence(self, sentence):
        return self.phoneme_transformation(sentence) if self.phoneme_transformation else None

    def score(self, ref, hyp):
        if self.contractions:
            sentence_forms = self.contractions.make_sentence_forms(hyp)
        else:
            sentence_forms = [hyp]

        measures = [
            jiwer.compute_measures(
                ref,
                hyp,
                truth_transform=self.transformation,
                hypothesis_transform=self.transformation,
            )
            for hyp in sentence_forms
        ]
        hits = [m["hits"] for m in measures]
        best_index = hits.index(max(hits))
        return (
            len(self.transformation(ref)),  # n words in the reference
            measures[best_index]["hits"],  # n hits for best sentence form
            measures[best_index]["wer"],  # n hits for best sentence form
            sentence_forms[best_index],  # Best form for the hypothesis
        )

    def score_phoneme(self, ref, hyp):
        if not self.phoneme_transformation:
            raise ValueError("No phoneme transformation defined")
        ref = self.phoneme_transformation(ref)
        hyp = self.phoneme_transformation(hyp)
        phoneme_measures = jiwer.compute_measures(
            ref,
            hyp,
        )
        return len(ref), phoneme_measures["hits"]


def score_listenhome(responses, scorer):

    responses = responses.copy()
    for r in responses:
        r["n_words"], r["hits_words"], sentence_form = scorer.score(r["prompt"], r["transcript"])
        r["scored_form"] = sentence_form
        r["n_phonemes"], r["hits_phonemes"] = scorer.score_phoneme(r["prompt"], sentence_form)
    return responses


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("input_files", type=str)
    parser.add_argument("save_dir", type=str)
    args = parser.parse_args()

    contraction = Contractions("src/analysis/contractions.csv")
    pron_dict = PronDictionary("data/external/beep/beep-1.0")
    pron_dict.add_dict("src/analysis/oov_dict.txt")
    scorer = SentenceScorer(pron_dict, contraction)

    for filename in glob.glob(args.input_files):
        file = Path(filename).name
        responses = json.load(open(filename, "r", encoding="utf-8"))
        responses = score_listenhome(responses, scorer)
        json.dump(responses, open(f"{args.save_dir}/{file}", "w", encoding="utf-8"), indent=2)


#if __name__ == "__main__":
#    main()
