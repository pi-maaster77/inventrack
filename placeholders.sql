--!SQLITE3

INSERT INTO personas (dni, nombre, apellido, tipo_persona, passwd, confianza) VALUES
(12345678, 'Juan', 'Pérez', 'Alumno', 'pass123', 5),
(87654321, 'Ana', 'Gómez', 'Profesor', 'secret', 8),
(11223344, 'Luis', 'Martínez', 'Pañolero', 'clave', 3);


INSERT INTO ubicaciones (estanteria, cajon) VALUES
('Estantería A', 'Cajón 1'),
('Estantería B', 'Cajón 2'),
('Estantería C', 'Cajón 3');

INSERT INTO unidad_medida (nombre) VALUES
('Litros'),
('Kilogramos'),
('Unidades');



INSERT INTO categorias (nombre, descripcion) VALUES
('Herramientas manuales', 'Herramientas para trabajo manual'),
('Equipos electrónicos', 'Dispositivos electrónicos'),
('Material de laboratorio', 'Material usado en laboratorio');



INSERT INTO items (nombre, descripcion, cantidad_total, cantidad_disponible, ubicacion_id, tipo_item) VALUES
('Martillo', 'Martillo de acero', 10, 8, 1, 'Herramienta'),
('Multímetro', 'Multímetro digital', 5, 3, 2, 'Herramienta'),
('Aceite lubricante', 'Aceite para maquinaria', 20, 15, 3, 'Recurso');


INSERT INTO items_categorias (item_id, categoria_id) VALUES
(1, 1),
(2, 2),
(3, 3);

INSERT INTO herramientas (item_id) VALUES
(1),
(2);


INSERT INTO recursos (item_id, unidad_medida_id) VALUES
(3, 1);


INSERT INTO prestamos (persona_id, fecha_prestamo, fecha_devolucion, vigente) VALUES
(12345678, '2025-08-01', NULL, 1),
(87654321, '2025-07-15', '2025-07-20', 0),
(11223344, '2025-08-10', NULL, 1);

INSERT INTO detalle_prestamo_item (prestamo_id, item_id, cantidad, condicion) VALUES
(1, 1, 2, 8),
(1, 3, 1, 10),
(3, 2, 1, 7);
