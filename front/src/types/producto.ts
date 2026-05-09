export interface Producto {
  id: number;
  nombre: string;
  descripcion: string;
  precio_base: number;
  imagen_url: string[];
  disponible: boolean;
}

export interface ProductoFormData {
  nombre: string;
  descripcion: string;
  precio_base: number | "";
  imagen_url: string; // string CSV en el formulario → string[] al enviar
  disponible: boolean;
  categoria_ids: number[];
}

export const EMPTY_PROD_FORM: ProductoFormData = {
  nombre: "",
  descripcion: "",
  precio_base: "",
  imagen_url: "",
  disponible: true,
  categoria_ids: [],
};
