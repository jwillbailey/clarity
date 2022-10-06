from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class Dataset(str, Enum):
    train = "train"
    dev = "dev"
    eval = "eval"


class InterfererType(str, Enum):
    speech = "speech"
    noise = "noise"


class ASRScore(BaseModel):
    wer: float
    mer: float
    wil: float
    wip: float
    hits: int
    substitutions: int
    deletions: int
    insertions: int


class Word(BaseModel):
    startTime: str
    endTime: str
    confidence: float
    speakerTag: int
    word: str


class ASRResult(BaseModel):
    transcript: str
    confidence: float
    words: list[Word]


class Room(BaseModel):
    name: str = Field(None, regex="^R[0-9]{5}$")
    dimensions: str = Field(None, regex="[0-9.]*x[0-9.]*x[0-9.]*$")


class Target(BaseModel):
    Positions: list[float]
    ViewVectors: list[float]
    name: str = Field(None, regex="^T[0-9]{3}_[A-Z0-9]{3}_[0-9]{5}$")
    nsamples: int = Field(None, ge=0)


class Listener(BaseModel):
    Positions: list[float]
    ViewVectors: list[float]


class Interferer(BaseModel):
    Positions: list[float]
    name: str = Field(None, regex="^(CIN_[a-z]*_[0-9]{3})|([a-z]{3}_[0-9]{5})$")
    nsamples: int = Field(None, ge=0)
    duration: float = Field(None, ge=0.0)
    type: InterfererType
    offset: int = Field(None, ge=0)


class Scene(BaseModel):
    room: Room
    hrirfilename: str
    target: Target
    listener: Listener
    interferer: Interferer
    azimuth_target_listener: float = Field(None, ge=-180, le=180)
    azimuth_interferer_listener: float = Field(None, ge=-180, le=180)
    scene: str = Field(None, regex="^S[0-9]{5}$")
    dataset: Dataset
    pre_samples: int = Field(None, ge=0)
    post_samples: int = Field(None, ge=0)
    SNR: float


class ListenAtHomeResponse(BaseModel):
    id: str = Field(alias="_id")
    md5: str
    filename: str
    length: int
    uploadDate: str
    metadata: dict
    scene_name: str
    target_name: Optional[str] = None
    transcript: Optional[str] = None
    scene: Optional[Scene] = None
    asr_score: Optional[ASRScore] = None
    asr_result: Optional[ASRResult] = None


class ResponseList(BaseModel):
    __root__: list[ListenAtHomeResponse]
