// ─── Respuesta estándar del backend ───────────────────────────────────────────
// Refleja el schema StandardResponse[T] definido en app/core/schema.py
export interface ApiResponse<T> {
  status: string;
  message: string;
  data: T | null;
}

// Helper: desenvuelve la respuesta y lanza si data es null
export function unwrapData<T>(response: ApiResponse<T>): T {
  if (response.data === null || response.data === undefined) {
    throw new Error(response.message ?? "La respuesta del servidor no contiene datos.");
  }
  return response.data;
}
