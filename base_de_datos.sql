-- Habilitar claves foráneas
PRAGMA foreign_keys = ON;

-- Tabla: personas
CREATE TABLE IF NOT EXISTS personas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,           -- Identificador único de la persona
    nombre TEXT NOT NULL,                           -- Nombre de la persona
    apellido TEXT NOT NULL,                         -- Apellido de la persona
    dni TEXT UNIQUE NOT NULL,                       -- DNI (identificador único)
    tipo_persona TEXT NOT NULL CHECK (tipo_persona IN ('Alumno', 'Profesor', 'Pañolero')),  -- Tipo de persona
    confianza INTEGER DEFAULT 0                     -- Nivel de confianza, por defecto 0
);

-- Tabla: categorias
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,           -- Identificador único de la categoría
    nombre TEXT NOT NULL,                           -- Nombre de la categoría
    descripcion TEXT                                -- Descripción de la categoría
);

-- Tabla: unidad_medida
CREATE TABLE IF NOT EXISTS unidad_medida (
    id INTEGER PRIMARY KEY AUTOINCREMENT,           -- Identificador único de la unidad de medida
    nombre TEXT UNIQUE NOT NULL                     -- Nombre de la unidad de medida
);

-- Tabla: ubicaciones
CREATE TABLE IF NOT EXISTS ubicaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,           -- Identificador único de la ubicación
    estanteria TEXT NOT NULL,                       -- Nombre de la estantería
    cajon TEXT NOT NULL                              -- Nombre del cajón dentro de la estantería
);

-- Tabla: items (artículos)
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,           -- Identificador único del artículo
    nombre TEXT NOT NULL,                           -- Nombre del artículo
    descripcion TEXT,                               -- Descripción del artículo
    cantidad_total REAL NOT NULL,                   -- Cantidad total del artículo
    cantidad_disponible REAL NOT NULL,              -- Cantidad disponible para préstamo
    categoria_id INTEGER,                           -- ID de la categoría (relación con tabla categorias)
    ubicacion_id INTEGER,                           -- ID de la ubicación (relación con tabla ubicaciones)
    tipo_item TEXT NOT NULL CHECK (tipo_item IN ('Herramienta', 'Recurso')), -- Tipo de item
    FOREIGN KEY (categoria_id) REFERENCES categorias(id),  -- Relación con la tabla categorias
    FOREIGN KEY (ubicacion_id) REFERENCES ubicaciones(id) -- Relación con la tabla ubicaciones
);

-- Tabla: herramientas (detalles específicos de las herramientas)
CREATE TABLE IF NOT EXISTS herramientas (
    item_id INTEGER PRIMARY KEY,                    -- ID del artículo (clave primaria de la tabla items)
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE  -- Relación con la tabla items
    -- Puedes agregar aquí campos específicos para herramientas, si es necesario
);

-- Tabla: recursos (detalles específicos de los recursos)
CREATE TABLE IF NOT EXISTS recursos (
    item_id INTEGER PRIMARY KEY,                    -- ID del artículo (clave primaria de la tabla items)
    unidad_medida_id INTEGER NOT NULL,              -- ID de la unidad de medida (relación con la tabla unidad_medida)
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,  -- Relación con la tabla items
    FOREIGN KEY (unidad_medida_id) REFERENCES unidad_medida(id)  -- Relación con la tabla unidad_medida
    -- Puedes agregar aquí campos específicos para recursos, si es necesario
);

-- Tabla: prestamos (préstamos de artículos)
CREATE TABLE IF NOT EXISTS prestamos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,           -- Identificador único del préstamo
    persona_id INTEGER,                              -- ID de la persona que realiza el préstamo
    fecha_prestamo DATE NOT NULL DEFAULT (DATE('now')),  -- Fecha del préstamo
    fecha_devolucion DATE,                          -- Fecha de devolución
    vigente BOOLEAN DEFAULT 1,                      -- Indica si el préstamo sigue vigente
    FOREIGN KEY (persona_id) REFERENCES personas(id) -- Relación con la tabla personas
);

-- Tabla: detalle_prestamo_item (detalle de los artículos prestados en cada préstamo)
CREATE TABLE IF NOT EXISTS detalle_prestamo_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,           -- Identificador único de cada detalle de préstamo
    prestamo_id INTEGER,                             -- ID del préstamo (relación con la tabla prestamos)
    item_id INTEGER,                                 -- ID del artículo (relación con la tabla items)
    cantidad REAL NOT NULL,                          -- Cantidad del artículo prestado
    FOREIGN KEY (prestamo_id) REFERENCES prestamos(id) ON DELETE CASCADE,  -- Relación con la tabla prestamos
    FOREIGN KEY (item_id) REFERENCES items(id)      -- Relación con la tabla items
);
