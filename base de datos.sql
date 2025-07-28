-- Tabla: personas
CREATE TABLE personas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    dni VARCHAR(15) UNIQUE NOT NULL,
    tipo_persona VARCHAR(20) CHECK (tipo_persona IN ('Alumno', 'Profesor', 'Pañolero')) NOT NULL,
    confianza INTEGER DEFAULT 0
);

-- Tabla: categorias
CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT
);

-- Tabla: unidad_medida (nueva tabla para normalizar recursos)
CREATE TABLE unidad_medida (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(20) UNIQUE NOT NULL
);

-- Tabla: ubicaciones (normalizada)
CREATE TABLE ubicaciones (
    id SERIAL PRIMARY KEY,
    estanteria VARCHAR(20) NOT NULL,
    cajon VARCHAR(20) NOT NULL
);

-- Tabla: items (entidad madre)
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    cantidad_total NUMERIC(10,2) NOT NULL,
    cantidad_disponible NUMERIC(10,2) NOT NULL,
    categoria_id INTEGER REFERENCES categorias(id),
    ubicacion_id INTEGER REFERENCES ubicaciones(id),
    tipo_item VARCHAR(20) CHECK (tipo_item IN ('Herramienta', 'Recurso')) NOT NULL
);

-- Tabla: herramientas (particularidades)
CREATE TABLE herramientas (
    item_id INTEGER PRIMARY KEY REFERENCES items(id) ON DELETE CASCADE
    -- Puedes agregar aquí campos específicos de herramientas si los necesitas
);

-- Tabla: recursos (particularidades)
CREATE TABLE recursos (
    item_id INTEGER PRIMARY KEY REFERENCES items(id) ON DELETE CASCADE,
    unidad_medida_id INTEGER REFERENCES unidad_medida(id) NOT NULL
    -- Puedes agregar aquí campos específicos de recursos si los necesitas
);

-- Tabla: prestamos
CREATE TABLE prestamos (
    id SERIAL PRIMARY KEY,
    persona_id INTEGER REFERENCES personas(id),
    fecha_prestamo DATE NOT NULL DEFAULT CURRENT_DATE,
    fecha_devolucion DATE,
    vigente BOOLEAN DEFAULT TRUE
);

-- Tabla: detalle_prestamo_item
CREATE TABLE detalle_prestamo_item (
    id SERIAL PRIMARY KEY,
    prestamo_id INTEGER REFERENCES prestamos(id) ON DELETE CASCADE,
    item_id INTEGER REFERENCES items(id),
    cantidad NUMERIC(10,2) NOT NULL
);

