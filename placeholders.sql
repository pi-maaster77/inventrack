-- Insertar personas
-- Insertar personas con los valores correctos
INSERT INTO personas (nombre, apellido, dni, tipo_persona, confianza)
VALUES
('Juan', 'Pérez', '12345678', 'Alumno', 5),
('Ana', 'Gómez', '23456789', 'Profesor', 10),
('Carlos', 'Martínez', '34567890', 'Pañolero', 3);


-- Insertar categorías
INSERT INTO categorias (nombre, descripcion)
VALUES
('Herramientas', 'Herramientas de uso general'),
('Recursos', 'Materiales y recursos de consumo'),
('Electrónica', 'Artículos electrónicos y gadgets');

-- Insertar unidades de medida
INSERT INTO unidad_medida (nombre)
VALUES
('Kilogramo'),
('Metro'),
('Unidad'),
('Litro');

-- Insertar ubicaciones
INSERT INTO ubicaciones (estanteria, cajon)
VALUES
('Estante 1', 'Cajón A'),
('Estante 1', 'Cajón B'),
('Estante 2', 'Cajón A'),
('Estante 3', 'Cajón C');

-- Insertar artículos (items)
INSERT INTO items (nombre, descripcion, cantidad_total, cantidad_disponible, categoria_id, ubicacion_id, tipo_item)
VALUES
('Martillo', 'Martillo de acero para trabajos de carpintería', 50, 45, 1, 1, 'Herramienta'),
('Destornillador', 'Destornillador plano y cruz', 100, 95, 1, 2, 'Herramienta'),
('Tornillos', 'Tornillos de acero de diferentes tamaños', 200, 150, 2, 1, 'Recurso'),
('Cable HDMI', 'Cable para conexión de dispositivos HDMI', 30, 25, 3, 3, 'Recurso'),
('Sierra de mano', 'Sierra de mano para cortar madera', 20, 15, 1, 4, 'Herramienta'),
('Papel higiénico', 'Papel higiénico para uso general', 500, 450, 2, 2, 'Recurso');

-- Insertar herramientas (relacionadas con items)
INSERT INTO herramientas (item_id)
VALUES
(1),  -- Martillo
(2),  -- Destornillador
(5);  -- Sierra de mano

-- Insertar recursos (relacionados con items)
INSERT INTO recursos (item_id, unidad_medida_id)
VALUES
(3, 3),  -- Tornillos, Unidad
(4, 4),  -- Cable HDMI, Litro (aunque no es muy apropiado, solo es un ejemplo)
(6, 1);  -- Papel higiénico, Kilogramo

-- Insertar préstamos
INSERT INTO prestamos (persona_id, fecha_prestamo, fecha_devolucion, vigente)
VALUES
(1, '2023-10-01', '2023-10-10', 1),  -- Juan Pérez, préstamo vigente
(2, '2023-10-05', '2023-10-12', 1),  -- Ana Gómez, préstamo vigente
(3, '2023-10-07', '2023-10-14', 1);  -- Carlos Martínez, préstamo vigente

-- Insertar detalles de préstamo de artículos
INSERT INTO detalle_prestamo_item (prestamo_id, item_id, cantidad)
VALUES
(1, 1, 2),  -- Juan Pérez pidió 2 martillos
(2, 4, 1),  -- Ana Gómez pidió 1 cable HDMI
(3, 6, 3);  -- Carlos Martínez pidió 3 paquetes de papel higiénico
