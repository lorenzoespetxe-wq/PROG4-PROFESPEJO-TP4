import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";

import Navbar from "./components/Navbar";
import CategoriasPage from "./pages/CategoriasPage";
import ProductosPage from "./pages/ProductosPage";

// ─── React Query client ────────────────────────────────────────────────────────
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // Reintenta 1 vez antes de pasar al estado de error
      retry: 1,
      // Considera los datos frescos por 30 segundos
      staleTime: 30_000,
    },
  },
});

// ─── App ───────────────────────────────────────────────────────────────────────
function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="min-h-screen bg-gray-50">
          <Navbar />

          <main className="max-w-6xl mx-auto px-6 py-8">
            <Routes>
              {/* Redirige la raíz a /categorias */}
              <Route path="/" element={<Navigate to="/categorias" replace />} />

              <Route path="/categorias" element={<CategoriasPage />} />
              <Route path="/productos" element={<ProductosPage />} />

              {/* Cualquier ruta no reconocida vuelve a /categorias */}
              <Route path="*" element={<Navigate to="/categorias" replace />} />
            </Routes>
          </main>
        </div>
      </BrowserRouter>

      {/* Panel de devtools de React Query — solo visible en desarrollo */}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}

export default App;
