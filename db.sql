BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "categorias" (
	"id"	INTEGER,
	"nombre"	TEXT NOT NULL,
	"descripcion"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "detalle_prestamo_item" (
	"id"	INTEGER,
	"prestamo_id"	INTEGER,
	"item_id"	INTEGER,
	"cantidad"	REAL NOT NULL,
	"condicion"	INTEGER CHECK("condicion" IN (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, NULL)),
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("item_id") REFERENCES "items"("id"),
	FOREIGN KEY("prestamo_id") REFERENCES "prestamos"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "herramientas" (
	"item_id"	INTEGER,
	PRIMARY KEY("item_id"),
	FOREIGN KEY("item_id") REFERENCES "items"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "items" (
	"id"	INTEGER,
	"nombre"	TEXT NOT NULL,
	"descripcion"	TEXT,
	"cantidad_total"	REAL NOT NULL,
	"cantidad_disponible"	REAL NOT NULL,
	"ubicacion_id"	INTEGER,
	"tipo_item"	TEXT NOT NULL CHECK("tipo_item" IN ('Herramienta', 'Recurso')),
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("ubicacion_id") REFERENCES "ubicaciones"("id")
);
CREATE TABLE IF NOT EXISTS "items_categorias" (
	"item_id"	INTEGER,
	"categoria_id"	INTEGER,
	PRIMARY KEY("item_id","categoria_id"),
	FOREIGN KEY("categoria_id") REFERENCES "categorias"("id"),
	FOREIGN KEY("item_id") REFERENCES "items"("id")
);
CREATE TABLE IF NOT EXISTS "personas" (
	"dni"	INTEGER,
	"nombre"	TEXT NOT NULL,
	"apellido"	TEXT NOT NULL,
	"tipo_persona"	TEXT NOT NULL CHECK("tipo_persona" IN ('Alumno', 'Profesor', 'Pañolero')),
	"passwd"	TEXT NOT NULL,
	"confianza"	INTEGER DEFAULT 0,
	PRIMARY KEY("dni")
);
CREATE TABLE IF NOT EXISTS "prestamos" (
	"id"	INTEGER,
	"persona_id"	INTEGER,
	"fecha_prestamo"	DATE NOT NULL DEFAULT (DATE('now')),
	"fecha_devolucion"	DATE,
	"vigente"	BOOLEAN DEFAULT 1,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("persona_id") REFERENCES "personas"("dni")
);
CREATE TABLE IF NOT EXISTS "recursos" (
	"item_id"	INTEGER,
	"unidad_medida_id"	INTEGER NOT NULL,
	PRIMARY KEY("item_id"),
	FOREIGN KEY("item_id") REFERENCES "items"("id") ON DELETE CASCADE,
	FOREIGN KEY("unidad_medida_id") REFERENCES "unidad_medida"("id")
);
CREATE TABLE IF NOT EXISTS "sessions" (
	"id"	INTEGER,
	"user_id"	INTEGER NOT NULL UNIQUE,
	"session_token"	TEXT NOT NULL,
	"created_at"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	"expires_at"	DATETIME,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "personas"("dni") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "ubicaciones" (
	"id"	INTEGER,
	"estanteria"	TEXT NOT NULL,
	"cajon"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "unidad_medida" (
	"id"	INTEGER,
	"nombre"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "categorias" VALUES (1,'Herramientas manuales','Herramientas para trabajo manual');
INSERT INTO "categorias" VALUES (2,'Equipos electrónicos','Dispositivos electrónicos');
INSERT INTO "categorias" VALUES (3,'Material de laboratorio','Material usado en laboratorio');
INSERT INTO "detalle_prestamo_item" VALUES (4,4,1,2.0,0);
INSERT INTO "herramientas" VALUES (1);
INSERT INTO "herramientas" VALUES (2);
INSERT INTO "items" VALUES (1,'Martillo','Martillo de acero',10.0,8.0,1,'Herramienta');
INSERT INTO "items" VALUES (2,'Multímetro','Multímetro digital',5.0,3.0,2,'Herramienta');
INSERT INTO "items" VALUES (3,'Aceite lubricante','Aceite para maquinaria',20.0,15.0,3,'Recurso');
INSERT INTO "items_categorias" VALUES (1,1);
INSERT INTO "items_categorias" VALUES (2,2);
INSERT INTO "items_categorias" VALUES (3,3);
INSERT INTO "personas" VALUES (32123132,'asdawd','asdadawd','Alumno','$2b$12$EnKtM4NfJYutG1C2PoFQl.6/teKp8sYxfN9yBQtb3W/1geq5O3ayC',0);
INSERT INTO "personas" VALUES (45342312,'hola','puto','Alumno','$2b$12$IgxXflfm5gRLPJRrezuQPeHYOByyGfGQmblcZWvLXee2jdqmFAZuS',0);
INSERT INTO "personas" VALUES (123123123,'123123','12312313','Alumno','$2b$12$48dfBHFcFaRq.GH2nYYFU.mWCC2nxWt7vYHKB3t/8KIQ0GqXi1Ea.',0);
INSERT INTO "prestamos" VALUES (4,32123132,'2025-09-17 01:22:02.724883','2025-09-17 01:22:02.724883',1);
INSERT INTO "recursos" VALUES (3,1);
INSERT INTO "sessions" VALUES (38,123123123,'OOeUGxD39p6fEl615sLH3ne9FiJKiNjt92pdjItBUuM','2025-08-18 18:49:33.528288','2025-09-17 18:49:33.528288');
INSERT INTO "sessions" VALUES (39,45342312,'ER_-WBwAT7yjl84XELS7P3R2snbu0freHHanGF60bd4','2025-08-18 18:50:44.574339','2025-09-17 18:50:44.574339');
INSERT INTO "sessions" VALUES (40,32123132,'cX8uWw62u7AlJFHdwt8uOaUjmPnclQZaJWZFOrTwmp4','2025-08-19 17:21:24.628842','2025-09-18 17:21:24.628842');
INSERT INTO "ubicaciones" VALUES (1,'Estantería A','Cajón 1');
INSERT INTO "ubicaciones" VALUES (2,'Estantería B','Cajón 2');
INSERT INTO "ubicaciones" VALUES (3,'Estantería C','Cajón 3');
INSERT INTO "unidad_medida" VALUES (1,'Litros');
INSERT INTO "unidad_medida" VALUES (2,'Kilogramos');
INSERT INTO "unidad_medida" VALUES (3,'Unidades');
COMMIT;
