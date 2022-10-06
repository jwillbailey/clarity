import numpy as np
import json
import jiwer
from analysis import score_transcription
from matplotlib import pyplot as plt

data = json.load(open('CEC2/target_transcription.eval.json'))


contraction = score_transcription.Contractions("analysis/contractions.csv")
pron_dict = score_transcription.PronDictionary("../external/beep/beep-1.0")
pron_dict.add_dict("analysis/oov_dict.txt")

scorer = score_transcription.SentenceScorer(pron_dict, contraction)

scores = [{"scene" : d["scene"], "target" : d["target"], "score" : scorer.score(jiwer.Strip()(d["prompt"]), jiwer.Strip()(d["transcription"])), "prompt" : d["prompt"]} for d in data]
scores = [{"scene" : s["scene"], "target" : s["target"], "score" : s["score"], "ratio" : s["score"][1] / s["score"][0], "prompt" : s["prompt"]} for s in scores]

pc = [(1-s["ratio"])*100 for s in scores]
plt.hist(wer)
plt.ylabel("count")
plt.xlabel("% correct")
plt.xlim([0,100])
plt.show()

low_wer = [{"scene" : s["scene"], "target" : s["target"], "score" : s["score"], "ratio" : s["score"][1] / s["score"][0], "prompt" : s["prompt"]} for s in scores if s["wer"] < 1]
