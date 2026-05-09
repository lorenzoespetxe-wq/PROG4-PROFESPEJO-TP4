import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import CategoriaList from "../components/CategoriaList";
import CategoriaModal from "../components/CategoriaModal";

import { type Categoria, type CategoriaFormData, EMPTY_CAT_FORM } from "../types/categoria";
import {
  getCategorias,
  createCategoria,
  updateCategoria,
  deleteCategoria,
} from "../services/api";

// ─── Query key factory ────────────────────────────────────────────────────────
export const categoriaKeys = {
  all: ["categorias"] as const,
};

// ─── Page component ───────────────────────────────────────────────────────────
const CategoriasPage = () => {
  const queryClient = useQueryClient();

  // ── Estado del modal ──────────────────────────────────────────────────────
  const [modalOpen, setModalOpen] = useState(false);
  const [catEditando, setCatEditando] = useState<Categoria | null>(null);
  const [formData, setFormData] = useState<CategoriaFormData>(EMPTY_CAT_FORM);

  // ── Lectura (GET) ─────────────────────────────────────────────────────────
  const {
    data: categorias = [],
    isLoading,
    isError,
    error,
  } = useQuery({
    queryKey: categoriaKeys.all,
    queryFn: getCategorias,
  });

  // ── Mutaciones ────────────────────────────────────────────────────────────
  const invalidateCategorias = () =>
    queryClient.invalidateQueries({ queryKey: categoriaKeys.all });

  const createMutation = useMutation({
    mutationFn: createCategoria,
    onSuccess: () => {
      invalidateCategorias();
      setModalOpen(false);
    },
    onError: () => alert("Error al crear la categoría."),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: CategoriaFormData }) =>
      updateCategoria(id, data),
    onSuccess: () => {
      invalidateCategorias();
      setModalOpen(false);
    },
    onError: () => alert("Error al actualizar la categoría."),
  });

  const deleteMutation = useMutation({
    mutationFn: deleteCategoria,
    onSuccess: invalidateCategorias,
    onError: () => alert("Error al eliminar la categoría."),
  });

  // ── Handlers de modal ─────────────────────────────────────────────────────
  const openCreate = () => {
    setCatEditando(null);
    setFormData(EMPTY_CAT_FORM);
    setModalOpen(true);
  };

  const openEdit = (cat: Categoria) => {
    setCatEditando(cat);
    setFormData({ nombre: cat.nombre, descripcion: cat.descripcion });
    setModalOpen(true);
  };

  const handleSubmit = () => {
    if (catEditando) {
      updateMutation.mutate({ id: catEditando.id, data: formData });
    } else {
      createMutation.mutate(formData);
    }
  };

  const handleDelete = (id: number) => {
    if (
      confirm(
        "¿Eliminar categoría? Si tiene productos asociados puede generarse un error en el backend."
      )
    ) {
      deleteMutation.mutate(id);
    }
  };

  const isMutating = createMutation.isPending || updateMutation.isPending;

  // ── Renderizado ───────────────────────────────────────────────────────────
  return (
    <div>
      {/* Encabezado */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-800">Categorías</h2>
          <p className="text-sm text-gray-400 mt-0.5">
            {isLoading ? "Cargando..." : `${categorias.length} registradas`}
          </p>
        </div>
        <button
          onClick={openCreate}
          className="bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold px-5 py-2.5 rounded-xl shadow-sm transition-colors"
        >
          ＋ Nueva categoría
        </button>
      </div>

      {/* Contenido */}
      {isLoading ? (
        <div className="text-center py-10 text-indigo-400 animate-pulse">Cargando...</div>
      ) : isError ? (
        <div className="bg-red-50 text-red-600 p-4 rounded-xl text-sm">
          {(error as Error)?.message ?? "Error de conexión con el servidor."}
        </div>
      ) : (
        <CategoriaList categorias={categorias} onEdit={openEdit} onDelete={handleDelete} />
      )}

      {/* Modal */}
      <CategoriaModal
        isOpen={modalOpen}
        categoriaEditando={catEditando}
        formData={formData}
        isMutating={isMutating}
        onFormChange={(field, val) => setFormData({ ...formData, [field]: val })}
        onClose={() => setModalOpen(false)}
        onSubmit={handleSubmit}
      />
    </div>
  );
};

export default CategoriasPage;
