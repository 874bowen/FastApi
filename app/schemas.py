from pydantic import BaseModel


# title str, content str, category, Bool published schema for validation
class PostBase(BaseModel):
    """
        This is going to give us a schema on how
        the created data should look like -
        providing validation
    """
    title: str
    content: str
    published: bool = True  # giving it a default value


class PostCreate(PostBase):
    pass


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

    class Config:
        orm_mode = True  # tells the pydantic model to read data even when it's not a dict
