import json
import os
import shutil

with open('E:\\clarity_CEC2_data\\clarity_data\\demo\\metadata\\scenes.demo.json') as f:
    scenes = json.load(f)

for scene in scenes:
    targets_present = f"{scene['target']['name']}.wav" in os.listdir(f'E:\\clarity_CEC2_data\\clarity_data\\demo\\targets\\')
    interferers_present = [f"{interf['name']}" in os.listdir(f'E:\\clarity_CEC2_data\\clarity_data\\demo\\interferers\\{interf["type"]}') for interf in scene['interferers'] if interf['type']!= 'music']
    music_interferers_present = [f"{interf['name'].split('/')[1]}" in os.listdir(f'E:\\clarity_CEC2_data\\clarity_data\\demo\\interferers\\{interf["type"]}\\{interf["name"].split("/")[0]}') for interf in scene['interferers'] if interf['type']== 'music']
    
    if targets_present==False:
        s = f"E:\\clarity_CEC2_data\\clarity_data\\dev\\targets\\{scene['target']['name']}.wav"
        t = f"E:\\clarity_CEC2_data\\clarity_data\\demo\\targets\\{scene['target']['name']}.wav"
        shutil.copy(s, t)
    
    if False in interferers_present:
        for i in scene['interferers']:
            if i['type']!= 'music':
                s = f"E:\\clarity_CEC2_data\\clarity_data\\dev\\interferers\\{i['type']}\\{i['name']}"
                t = f"E:\\clarity_CEC2_data\\clarity_data\\demo\\interferers\\{i['type']}\\{i['name']}"
                shutil.copy(s, t)
    
    
    if False in music_interferers_present:
        for i in scene['interferers']:
            print(i['type'])
            if i['type']== 'music':
                s = f"E:\\clarity_CEC2_data\\clarity_data\\dev\\interferers\\{i['type']}\\{i['name'].split('/')[0]}\\{i['name'].split('/')[1]}"
                t = f"E:\\clarity_CEC2_data\\clarity_data\\demo\\interferers\\{i['type']}\\{i['name'].split('/')[0]}\\{i['name'].split('/')[1]}"
                print(f"{s}\n{t}")
                shutil.copy(s, t)