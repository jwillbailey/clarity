# Compute HL severity for each listener
import json

with open("../../data/published/listeners.CPC1_train.json") as f:
    listeners = json.load(f)

# Average loss from 2-8 dB
for listener in listeners.values():
    levels = listener["audiogram_levels_l"][3:] + listener["audiogram_levels_r"][3:]
    loss = sum(levels) / len(levels)
    if loss > 56:
        loss_type = "Severe"
    elif loss > 35:
        loss_type = "Moderate"
    else:
        loss_type = "Mild"
    print(f"{listener['name']} {loss} {loss_type}")
