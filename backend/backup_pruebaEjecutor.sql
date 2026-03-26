-- Backup of pruebaEjecutor

CREATE TABLE `compras` (
  `id` int(11) DEFAULT NULL,
  `nombre` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


CREATE TABLE `usuarios` (
  `id` int(11) DEFAULT NULL,
  `nombre` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


CREATE TABLE `usuarios_prueba` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `edad` int(11) DEFAULT NULL,
  `fecha_registro` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

INSERT INTO `usuarios_prueba` (`id`, `nombre`, `edad`, `fecha_registro`) VALUES (1, 'Santiago', 28, '2026-03-23 15:58:40');
INSERT INTO `usuarios_prueba` (`id`, `nombre`, `edad`, `fecha_registro`) VALUES (2, 'Elena', 34, '2026-03-23 15:58:40');
INSERT INTO `usuarios_prueba` (`id`, `nombre`, `edad`, `fecha_registro`) VALUES (3, 'Carlos', 21, '2026-03-23 15:58:40');

