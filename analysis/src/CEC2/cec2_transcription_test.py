
import numpy as np
import pandas as pd
import json
import jiwer

from analysis import score_transcription
from matplotlib import pyplot as plt
from scipy.stats import kruskal
from scipy.stats import wilcoxon
from statsmodels.stats.multitest import multipletests
data = json.load(open('CEC2/target_transcription.eval.json'))


contraction = score_transcription.Contractions("analysis/contractions.csv")

scorer = score_transcription.SentenceScorer(pron_dict=None, contractions = contraction)

scores = [{"scene" : d["scene"], "target" : d["target"], "score" : scorer.score(jiwer.Strip()(d["prompt"]), jiwer.Strip()(d["transcription"])), "prompt" : d["prompt"]} for d in data]
scores = [{"scene" : s["scene"], "target" : s["target"], "score" : s["score"], "ratio" : s["score"][1] / s["score"][0], "prompt" : s["prompt"], "wer" : s["score"][2]} for s in scores]

pc = [(s["ratio"])*100 for s in scores]
wer = [s["wer"] * 100 for s in scores]

pc_d = pd.DataFrame(pc).describe()
wer_d = pd.DataFrame(wer).describe()

plt.hist(pc)
plt.ylabel("count")
plt.xlabel("% correct")
plt.xlim([0,100])
plt.show()


plt.hist(wer)
plt.ylabel("count")
plt.xlabel("Word Error Rate")
#plt.xlim([0,100])
plt.show()

low_wer = [s["wer"] * 100 for s in scores if s['wer'] > 0]

speakers = np.unique(np.array([s['target'].split("_")[0] for s in scores]))
spk_scores = {}
spk_scores_desc = {}

for speaker in speakers:
    spk_scores[speaker] = {
        "pc" : [s["ratio"]*100 for s in scores if s['target'].split("_")[0]==speaker],
        "wer" : [s["wer"] * 100 for s in scores if s['target'].split("_")[0]==speaker]
        }
    spk_scores_desc[speaker] = {"pc" : pd.DataFrame([s["ratio"]*100 for s in scores if s['target'].split("_")[0]==speaker]).describe(),
                                "wer" : pd.DataFrame([s["wer"]*100 for s in scores if s['target'].split("_")[0]==speaker]).describe()}

spk_scores = pd.DataFrame.from_dict(spk_scores)
spk_scores_desc = pd.DataFrame.from_dict(spk_scores_desc)

for s in speakers:
    print(s)
    print(spk_scores_desc.transpose().pc[s])


for s in speakers:
    print(s)
    print(spk_scores_desc.transpose().wer[s])

ks_pc = kruskal(spk_scores.transpose().wer[speakers[0]],
                spk_scores.transpose().wer[speakers[1]],
                spk_scores.transpose().wer[speakers[2]],
                spk_scores.transpose().wer[speakers[3]],
                spk_scores.transpose().wer[speakers[4]],
                spk_scores.transpose().wer[speakers[5]])

pairwise_comps = np.ones([6, 6])
p1d = []

for i in range(6):
    for j in range(6):
        if not i <= j:
            p = wilcoxon(spk_scores.transpose().wer[speakers[i]], spk_scores.transpose().wer[speakers[j]])[1]
            p1d.append(p)
bf = multipletests(p1d)

k = 0
for i in range(6):
    for j in range(6):
        if not i <= j:
            pairwise_comps[i, j] = bf[1][k]
            k+=1

pairwise_comps_df = pd.DataFrame(pairwise_comps)
pairwise_comps_df.columns = speakers
pairwise_comps_df.index = speakers

plt.boxplot(spk_scores.transpose().pc)
plt.xticks(np.arange(6)+1, speakers)
plt.xlabel('Speakers')
plt.ylabel('% correct')
plt.savefig('pc_by_spk.png')
plt.clf()
plt.boxplot(spk_scores.transpose().wer)
plt.xticks(np.arange(6)+1, speakers)
plt.xlabel('Speakers')
plt.ylabel('Word error rate')
plt.savefig('wer_by_spk.png')
plt.clf()