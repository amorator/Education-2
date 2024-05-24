BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "web_Workers" (
	"id"	INTEGER UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
	"speciality"	TEXT NOT NULL,
	"experience"	REAL NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "web_Projects" (
	"id"	INTEGER UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
	"wid"	INTEGER NOT NULL,
	"description"	TEXT,
	"stage"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("wid") REFERENCES "web_Workers"("id") ON DELETE CASCADE
);
INSERT INTO "web_Workers" VALUES (1,'Иварнов А. Б.','Программист',1.3);
INSERT INTO "web_Workers" VALUES (2,'Петров В. Г.','Тестировщик',2.0);
INSERT INTO "web_Workers" VALUES (3,'Никитин Г. Е.','Тестировщик',1.0);
INSERT INTO "web_Workers" VALUES (4,'Артемов Ж. З.','Дизайнер',0.5);
INSERT INTO "web_Workers" VALUES (5,'Федоров Е. А.','Программист',7.0);
INSERT INTO "web_Projects" VALUES (1,'З1',1,'qwe','7');
INSERT INTO "web_Projects" VALUES (2,'З2',1,'rty','0');
INSERT INTO "web_Projects" VALUES (3,'З3',5,'uio','7');
INSERT INTO "web_Projects" VALUES (4,'З4',5,'pas','7');
INSERT INTO "web_Projects" VALUES (5,'З5',1,'dfg','3');
INSERT INTO "web_Projects" VALUES (6,'З6',2,'hjk','0');
INSERT INTO "web_Projects" VALUES (7,'З11',3,'qwe','7');
INSERT INTO "web_Projects" VALUES (8,'З22',2,'rty','0');
INSERT INTO "web_Projects" VALUES (9,'З33',5,'uio','7');
INSERT INTO "web_Projects" VALUES (10,'З44',1,'pas','7');
INSERT INTO "web_Projects" VALUES (11,'З55',3,'dfg','3');
INSERT INTO "web_Projects" VALUES (12,'З66',3,'hjk','0');
INSERT INTO "web_Projects" VALUES (13,'З10',2,'qwe','7');
INSERT INTO "web_Projects" VALUES (14,'З29',1,'rty','0');
INSERT INTO "web_Projects" VALUES (15,'З38',4,'uio','7');
INSERT INTO "web_Projects" VALUES (16,'З47',4,'pas','7');
INSERT INTO "web_Projects" VALUES (17,'З56',4,'dfg','3');
INSERT INTO "web_Projects" VALUES (18,'З65',4,'hjk','0');
COMMIT;
