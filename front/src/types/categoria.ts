export interface Categoria {
  id: number;
  nombre: string;
  descripcion: string;
}

export interface CategoriaFormData {
  nombre: string;
  descripcion: string;
}

export const EMPTY_CAT_FORM: CategoriaFormData = {
  nombre: "",
  descripcion: "",
};
