from pydantic import BaseModel, ConfigDict


class ProductoCategoriaBase(BaseModel):
    producto_id: int
    categoria_id: int


class ProductoCategoriaCreate(ProductoCategoriaBase):
    pass


class ProductoCategoriaRead(ProductoCategoriaBase):
    model_config = ConfigDict(from_attributes=True)
