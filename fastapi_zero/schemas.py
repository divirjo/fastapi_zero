from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    # configura que ao validar objetos do tipo UserPublic, as informações serão # extraídas dos atributos da classe para um dicionário  # noqa: E501
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]
