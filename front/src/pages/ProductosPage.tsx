import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import ProductoList from "../components/ProductoList";
import ProductoModal from "../components/ProductoModal";

import { type Producto, type ProductoFormData, EMPTY_PROD_FORM } from "../types/producto";
import {
  getProductos,
  createProducto,
  updateProducto,
  deleteProducto,
  getCategoriasDeProducto,
} from "../services/api";
import { categoriaKeys } from "./CategoriasPage";
import { getCategorias } from "../services/api";

// ─── Query key factory ────────────────────────────────────────────────────────
const productoKeys = {
  all: ["productos"] as const,
};

// ─── Page component ───────────────────────────────────────────────────────────
const ProductosPage = () => {
  const queryClient = useQueryClient();

  // ── Estado del modal ──────────────────────────────────────────────────────
  const [modalOpen, setModalOpen] = useState(false);
  const [prodEditando, setProdEditando] = useState<Producto | null>(null);
  const [formData, setFormData] = useState<ProductoFormData>(EMPTY_PROD_FORM);

  // ── Lectura: productos ────────────────────────────────────────────────────
  const {
    data: productos = [],
    isLoading: loadingProductos,
    isError: errorProductos,
    error: errorProdMsg,
  } = useQuery({
    queryKey: productoKeys.all,
    queryFn: getProductos,
  });

  // ── Lectura: categorías (para el selector del modal) ──────────────────────
  const { data: categorias = [] } = useQuery({
    queryKey: categoriaKeys.all,
    queryFn: getCategorias,
  });

  // ── Mutaciones ────────────────────────────────────────────────────────────
  const invalidateProductos = () =>
    queryClient.invalidateQueries({ queryKey: productoKeys.all });

  const createMutation = useMutation({
    mutationFn: createProducto,
    onSuccess: () => {
      invalidateProductos();
      setModalOpen(false);
    },
    onError: () => alert("Error al crear el producto."),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: ProductoFormData }) =>
      updateProducto(id, data),
    onSuccess: () => {
      invalidateProductos();
      setModalOpen(false);
    },
    onError: () => alert("Error al actualizar el producto."),
  });

  const deleteMutation = useMutation({
    mutationFn: deleteProducto,
    onSuccess: invalidateProductos,
    onError: () => alert("Error al eliminar el producto."),
  });

  // ── Handlers de modal ─────────────────────────────────────────────────────
  const openCreate = () => {
    setProdEditando(null);
    setFormData(EMPTY_PROD_FORM);
    setModalOpen(true);
  };

  /**
   * Al editar un producto, consultamos las categorías asignadas mediante
   * el endpoint de relaciones para pre-marcar los checkboxes correctamente.
   */
  const openEdit = async (prod: Producto) => {
    try {
      const idsAsignados = await getCategoriasDeProducto(prod.id);
      setProdEditando(prod);
      setFormData({
        nombre: prod.nombre,
        descripcion: prod.descripcion,
        precio_base: prod.precio_base,
        imagen_url: prod.imagen_url.join(", "),
        disponible: prod.disponible,
        categoria_ids: idsAsignados,
      });
      setModalOpen(true);
    } catch {
      alert("Error al cargar las categorías del producto.");
    }
  };

  const handleSubmit = () => {
    if (prodEditando) {
      updateMutation.mutate({ id: prodEditando.id, data: formData });
    } else {
      createMutation.mutate(formData);
    }
  };

  const handleDelete = (id: number) => {
    if (confirm("¿Eliminar producto?")) {
      deleteMutation.mutate(id);
    }
  };

  const toggleCategoria = (catId: number) => {
    setFormData((prev) => {
      const tiene = prev.categoria_ids.includes(catId);
      return {
        ...prev,
        categoria_ids: tiene
          ? prev.categoria_ids.filter((id) => id !== catId)
          : [...prev.categoria_ids, catId],
      };
    });
  };

  const isMutating = createMutation.isPending || updateMutation.isPending;

  // ── Renderizado ───────────────────────────────────────────────────────────
  return (
    <div>
      {/* Encabezado */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-800">Productos</h2>
          <p className="text-sm text-gray-400 mt-0.5">
            {loadingProductos ? "Cargando..." : `${productos.length} registrados`}
          </p>
        </div>
        <button
          onClick={openCreate}
          className="bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold px-5 py-2.5 rounded-xl shadow-sm transition-colors"
        >
          ＋ Nuevo producto
        </button>
      </div>

      {/* Contenido */}
      {loadingProductos ? (
        <div className="text-center py-10 text-indigo-400 animate-pulse">Cargando...</div>
      ) : errorProductos ? (
        <div className="bg-red-50 text-red-600 p-4 rounded-xl text-sm">
          {(errorProdMsg as Error)?.message ?? "Error de conexión con el servidor."}
        </div>
      ) : (
        <ProductoList productos={productos} onEdit={openEdit} onDelete={handleDelete} />
      )}

      {/* Modal */}
      <ProductoModal
        isOpen={modalOpen}
        productoEditando={prodEditando}
        formData={formData}
        categorias={categorias}
        isMutating={isMutating}
        onFormChange={(field, val) => setFormData({ ...formData, [field]: val })}
        onCategoriaToggle={toggleCategoria}
        onClose={() => setModalOpen(false)}
        onSubmit={handleSubmit}
      />
    </div>
  );
};

export default ProductosPage;
