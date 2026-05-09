import { type ApiResponse, unwrapData } from "../types/api";
import { type Categoria, type CategoriaFormData } from "../types/categoria";
import { type Producto, type ProductoFormData } from "../types/producto";

export const API = "http://localhost:8000";

// ─── Helpers internos ─────────────────────────────────────────────────────────

async function apiFetch<T>(url: string, init?: RequestInit): Promise<T> {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ message: res.statusText }));
    throw new Error(error?.detail ?? error?.message ?? "Error en el servidor");
  }

  const json: ApiResponse<T> = await res.json();
  return unwrapData(json);
}

// ─── Categorías ───────────────────────────────────────────────────────────────

export const getCategorias = (): Promise<Categoria[]> =>
  apiFetch<Categoria[]>(`${API}/categorias/`);

export const createCategoria = (data: CategoriaFormData): Promise<Categoria> =>
  apiFetch<Categoria>(`${API}/categorias/`, {
    method: "POST",
    body: JSON.stringify(data),
  });

export const updateCategoria = (id: number, data: CategoriaFormData): Promise<Categoria> =>
  apiFetch<Categoria>(`${API}/categorias/${id}`, {
    method: "PUT",
    body: JSON.stringify(data),
  });

export const deleteCategoria = (id: number): Promise<void> =>
  apiFetch<void>(`${API}/categorias/${id}`, { method: "DELETE" });

// ─── Productos ────────────────────────────────────────────────────────────────

export const getProductos = (): Promise<Producto[]> =>
  apiFetch<Producto[]>(`${API}/productos/`);

/** Convierte el ProductoFormData del formulario al payload que espera el backend */
function buildProductoPayload(formData: ProductoFormData) {
  return {
    ...formData,
    precio_base: Number(formData.precio_base),
    imagen_url: formData.imagen_url
      ? formData.imagen_url
          .split(",")
          .map((s) => s.trim())
          .filter((s) => s !== "")
      : [],
  };
}

export const createProducto = (data: ProductoFormData): Promise<Producto> =>
  apiFetch<Producto>(`${API}/productos/`, {
    method: "POST",
    body: JSON.stringify(buildProductoPayload(data)),
  });

export const updateProducto = (id: number, data: ProductoFormData): Promise<Producto> =>
  apiFetch<Producto>(`${API}/productos/${id}`, {
    method: "PUT",
    body: JSON.stringify(buildProductoPayload(data)),
  });

export const deleteProducto = (id: number): Promise<void> =>
  apiFetch<void>(`${API}/productos/${id}`, { method: "DELETE" });

// ─── Relaciones producto–categoría ───────────────────────────────────────────

interface ProductoCategoriaRelacion {
  categoria_id: number;
}

export const getCategoriasDeProducto = async (productoId: number): Promise<number[]> => {
  const res = await fetch(`${API}/producto-categorias/producto/${productoId}`);
  if (!res.ok) throw new Error("Error cargando relaciones del producto");
  const json: ApiResponse<ProductoCategoriaRelacion[]> = await res.json();
  const data = unwrapData(json);
  return data.map((r) => r.categoria_id);
};
