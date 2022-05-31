import gdown
import os
from pathlib import Path

def get_metadata_demo():
    metadata_url = 'https://drive.google.com/uc?export=download&id=14KGm2GaRgwlrZvtmMwWTYu7itaRVQV8f'
    output = 'metadata.tgz'

    gdown.download(metadata_url, output, quiet=False)
    p = Path("clarity_data/demo")
    if p.exists()==False:
        p.mkdir(parents=True, exist_ok=True)
    os.system('tar -xvzf metadata.tgz --directory clarity_data/')
    os.system('rm metadata.tgz')

def get_targets_demo():
    targets_url = "https://drive.google.com/uc?export=download&id=1uu2Hes1fzqNaZSCiFNhxZM3bE_fAVKsD"
    output = "targets.tgz"
    gdown.download(targets_url, output, quiet=False)
    p = Path("clarity_data/demo")
    if p.exists()==False:
        p.mkdir(parents=True, exist_ok=True)
    os.system("tar -xzf targets.tgz --directory clarity_data/demo/")
    os.system("rm targets.tgz")


def get_interferers_demo():
    interferers_url = "https://drive.google.com/uc?export=download&id=1_ssD238Qv-EETzC0hJze7JhLE7bHyqwG"
    output = "interferers.tgz"
    gdown.download(interferers_url, output, quiet=False)
    p = Path("clarity_data/demo")
    if p.exists()==False:
        p.mkdir(parents=True, exist_ok=True)
    os.system("tar -xzf interferers.tgz --directory clarity_data/demo/")
    os.system("rm interferers.tgz")


def get_rooms_demo():
    rooms_url = "https://drive.google.com/uc?export=download&id=1FBC8DI4Ru-g3Set0fDzoKmXTqHqNXV8n"
    output = "rooms.tgz"
    gdown.download(rooms_url, output, quiet=False)
    p = Path("clarity_data/demo")
    if p.exists()==False:
        p.mkdir(parents=True, exist_ok=True)
    os.system("tar -xzf rooms.tgz --directory clarity_data/demo/")
    os.system("rm rooms.tgz")


def get_scenes_demo():
    scenes_url = "https://drive.google.com/uc?export=download&id=1PB0CfGXhpkYNk8HbE5lTWowm2016x6Hl"
    output = "scenes.tgz"
    gdown.download(scenes_url, output, quiet=False)
    p = Path("clarity_data/demo")
    if p.exists()==False:
        p.mkdir(parents=True, exist_ok=True)
    os.system("tar -xzf scenes.tgz --directory clarity_data/")
    os.system("rm scenes.tgz")
