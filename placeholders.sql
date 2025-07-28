-- algunos placeholders para el proyecto
-- estos son ejemplos de cómo podrías estructurar tus consultas SQL
-- para interactuar con una base de datos en tu proyecto

-- Agregar unas categorías
INSERT INTO categorias (nombre, descripcion)
VALUES ('Herramientas Eléctricas', 'Herramientas que funcionan con electricidad');

INSERT INTO categorias (nombre, descripcion)
VALUES ('Herramientas Manuales', 'Herramientas que se utilizan manualmente sin electricidad');

INSERT INTO categorias (nombre, descripcion)
VALUES ('Recursos de Construcción', 'Materiales y recursos utilizados en la construcción');

-- Agregar unidades de medida
INSERT INTO unidad_medida (nombre) VALUES ('unidades');
INSERT INTO unidad_medida (nombre) VALUES ('metros cuadrados');

-- Agregar unas ubicaciones
INSERT INTO ubicaciones (estanteria, cajon)
VALUES ('Estantería A', 'Cajón 1');
INSERT INTO ubicaciones (estanteria, cajon)
VALUES ('Estantería A', 'Cajón 2'); 
INSERT INTO ubicaciones (estanteria, cajon)
VALUES ('Estantería B', 'Cajón 1');
INSERT INTO ubicaciones (estanteria, cajon)
VALUES ('Estantería B', 'Cajón 2');

-- Agregar algunos items y sus particularidades

-- Herramientas
INSERT INTO items (nombre, descripcion, cantidad_total, cantidad_disponible, categoria_id, ubicacion_id, tipo_item)
VALUES (
    'Taladro',
    'Taladro eléctrico de alta potencia',
    10,
    10,
    (SELECT id FROM categorias WHERE nombre = 'Herramientas Eléctricas' LIMIT 1),
    (SELECT id FROM ubicaciones WHERE estanteria = 'Estantería A' AND cajon = 'Cajón 1' LIMIT 1),
    'Herramienta'
);
INSERT INTO herramientas (item_id) VALUES ((SELECT id FROM items WHERE nombre = 'Taladro' LIMIT 1));

INSERT INTO items (nombre, descripcion, cantidad_total, cantidad_disponible, categoria_id, ubicacion_id, tipo_item)
VALUES (
    'Destornillador',
    'Destornillador de precisión',
    20,
    20,
    (SELECT id FROM categorias WHERE nombre = 'Herramientas Manuales' LIMIT 1),
    (SELECT id FROM ubicaciones WHERE estanteria = 'Estantería A' AND cajon = 'Cajón 1' LIMIT 1),
    'Herramienta'
);
INSERT INTO herramientas (item_id) VALUES ((SELECT id FROM items WHERE nombre = 'Destornillador' LIMIT 1));

INSERT INTO items (nombre, descripcion, cantidad_total, cantidad_disponible, categoria_id, ubicacion_id, tipo_item)
VALUES (
    'Martillo',
    'Martillo de acero forjado',
    15,
    15,
    (SELECT id FROM categorias WHERE nombre = 'Herramientas Manuales' LIMIT 1),
    (SELECT id FROM ubicaciones WHERE estanteria = 'Estantería A' AND cajon = 'Cajón 2' LIMIT 1),
    'Herramienta'
);
INSERT INTO herramientas (item_id) VALUES ((SELECT id FROM items WHERE nombre = 'Martillo' LIMIT 1));

-- Recursos
INSERT INTO items (nombre, descripcion, cantidad_total, cantidad_disponible, categoria_id, ubicacion_id, tipo_item)
VALUES (
    'Tornillo Autoperforante',
    'Tornillo para madera y metal',
    1000,
    1000,
    (SELECT id FROM categorias WHERE nombre = 'Recursos de Construcción' LIMIT 1),
    (SELECT id FROM ubicaciones WHERE estanteria = 'Estantería A' AND cajon = 'Cajón 1' LIMIT 1),
    'Recurso'
);
INSERT INTO recursos (item_id, unidad_medida_id) VALUES (
    (SELECT id FROM items WHERE nombre = 'Tornillo Autoperforante' LIMIT 1),
    (SELECT id FROM unidad_medida WHERE nombre = 'unidades' LIMIT 1)
);

INSERT INTO items (nombre, descripcion, cantidad_total, cantidad_disponible, categoria_id, ubicacion_id, tipo_item)
VALUES (
    'Tablero de Madera',
    'Tablero para construcción',
    500,
    500,
    (SELECT id FROM categorias WHERE nombre = 'Recursos de Construcción' LIMIT 1),
    (SELECT id FROM ubicaciones WHERE estanteria = 'Estantería A' AND cajon = 'Cajón 2' LIMIT 1),
    'Recurso'
);
INSERT INTO recursos (item_id, unidad_medida_id) VALUES (
    (SELECT id FROM items WHERE nombre = 'Tablero de Madera' LIMIT 1),
    (SELECT id FROM unidad_medida WHERE nombre = 'metros cuadrados' LIMIT 1)
);