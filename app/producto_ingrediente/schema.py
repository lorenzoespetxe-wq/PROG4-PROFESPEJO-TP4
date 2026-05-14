from pydantic import BaseModel, Field, ConfigDict
from app.ingrediente.model import UnidadMedida  # Asegúrate de importar el Enum


# GET Ingrediente + Unidad de medida:
class IngredienteReducidoRead(BaseModel):
    nombre: str
    unidad_de_medida: UnidadMedida

    model_config = ConfigDict(from_attributes=True)


# BASE:
class ProductoIngredienteBase(BaseModel):
    producto_id: int
    ingrediente_id: int
    cantidad: float = Field(..., gt=0)


# POST:
class ProductoIngredienteCreate(ProductoIngredienteBase):
    pass


# READ:
class ProductoIngredienteRead(ProductoIngredienteBase):
    # Usamos IngredienteReducidoRead para traer el nombre
    # del ingrediente al mostrar la relación.
    ingrediente: IngredienteReducidoRead

    model_config = ConfigDict(from_attributes=True)
