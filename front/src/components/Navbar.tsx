import { NavLink } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="bg-indigo-700 shadow-lg">
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center gap-6">
        {/* Logo / Brand */}
        <div className="flex items-center gap-3 mr-4">
          <span className="text-2xl">🗂️</span>
          <span className="text-white text-xl font-bold tracking-wide">
            Gestión de Stock
          </span>
        </div>

        {/* Navigation links */}
        <NavLink
          to="/categorias"
          className={({ isActive }) =>
            `text-sm font-semibold px-4 py-2 rounded-lg transition-colors ${
              isActive
                ? "bg-white text-indigo-700"
                : "text-indigo-200 hover:text-white hover:bg-indigo-600"
            }`
          }
        >
          Categorías
        </NavLink>

        <NavLink
          to="/productos"
          className={({ isActive }) =>
            `text-sm font-semibold px-4 py-2 rounded-lg transition-colors ${
              isActive
                ? "bg-white text-indigo-700"
                : "text-indigo-200 hover:text-white hover:bg-indigo-600"
            }`
          }
        >
          Productos
        </NavLink>
      </div>
    </nav>
  );
};

export default Navbar;
