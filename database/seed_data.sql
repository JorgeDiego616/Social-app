-- =============================
-- DATOS DE PRUEBA
-- =============================

-- Usuarios
INSERT INTO users (username, role) VALUES
('cristhian', 'admin'),
('ana', 'user'),
('luis', 'user'),
('maria', 'user'),
('juan', 'user');

-- Publicaciones
INSERT INTO posts (title, body, user_id) VALUES
('Primer post', 'Bienvenido a la red social', 1),
('Post de Ana', 'Amo programar en Python', 2),
('Post de Luis', 'Hoy aprendí FastAPI', 3),
('Post de María', 'Desarrollando mi portafolio web', 4),
('Post de Juan', 'Conectando backend con frontend', 5);

-- Seguimientos
INSERT INTO follows (following_user_id, followed_user_id) VALUES
(2, 1),  -- Ana sigue a Cristhian
(3, 1),  -- Luis sigue a Cristhian
(4, 2),  -- María sigue a Ana
(5, 3);  -- Juan sigue a Luis
