from pydantic import BaseModel, Field
from typing import Optional, List

class PersonSchema(BaseModel):
    nome: str = Field(...)
    horarios: List[str] = Field(...)
    emocoes: List[str] = Field(...)
    setor: str = Field(...)
    imagem: str = Field(...)

    class Config:
        schema_extra = {
            'example': {
                'nome': 'Emerson Roseiro Filho',
                'horarios': ['2014-02-10T10:50:42.389Z'],
                'emocoes': ['feliz'],
                'setor': 'Brain',
                'imagem': 'AgEBAYkQDgAAAAQAxJUHAMtmAQBwbAUAtBcDACAAAACnZgEAK5+cn5+cn5+coaKfpeAPAgKhnqRgAgyhoZ6hoJ2goJ2goJufgAIf…'
            }
        }

class UpdatePersonModel(BaseModel):
    nome: Optional[str]
    horarios: Optional[List[str]]
    emocoes: Optional[List[str]]
    setor: Optional[str]
    imagem: Optional[str]

    class Config:
        schema_extra = {
            'example': {
                'nome': 'Emerson Roseiro Filho',
                'horarios': ['2014-02-10T10:50:42.389Z'],
                'emocoes': ['feliz'],
                'setor': 'Brain',
                'imagem': 'AgEBAYkQDgAAAAQAxJUHAMtmAQBwbAUAtBcDACAAAACnZgEAK5+cn5+cn5+coaKfpeAPAgKhnqRgAgyhoZ6hoJ2goJ2goJufgAIf…'
            }
        }

def ResponseModel(data, message):
    return {
        'data': data,
        'code': 200,
        'message': message
    }

def ErrorResponseModel(error, code, message):
    return {
        'error': error,
        'code': code,
        'message': message
    }