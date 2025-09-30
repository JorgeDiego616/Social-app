# 📘 Diseño de la Base de Datos - Social Network API

Este documento describe la estructura de la base de datos utilizada en el proyecto **Social Network API**.

---

## 🔹 Tablas principales

### 1. `users`
Almacena los datos básicos de cada usuario.

| Campo      | Tipo         | Restricciones                 |
|------------|-------------|-------------------------------|
| id         | INTEGER     | PK, AUTOINCREMENT             |
| username   | VARCHAR(50) | NOT NULL, UNIQUE              |
| role       | VARCHAR(20) | DEFAULT 'user'                |
| created_at | DATETIME    | DEFAULT CURRENT_TIMESTAMP     |

---

### 2. `posts`
Contiene las publicaciones creadas por los usuarios.

| Campo      | Tipo         | Restricciones                                     |
|------------|-------------|---------------------------------------------------|
| id         | INTEGER     | PK, AUTOINCREMENT                                 |
| title      | VARCHAR(100)| NOT NULL                                          |
| body       | TEXT        | NOT NULL                                          |
| user_id    | INTEGER     | FK → users(id), NOT NULL                          |
| status     | VARCHAR(20) | DEFAULT 'published'                               |
| created_at | DATETIME    | DEFAULT CURRENT_TIMESTAMP                         |

---

### 3. `follows`
Representa la relación de "seguir" entre usuarios.

| Campo              | Tipo     | Restricciones                                    |
|--------------------|----------|--------------------------------------------------|
| following_user_id  | INTEGER  | FK → users(id), parte de PK                      |
| followed_user_id   | INTEGER  | FK → users(id), parte de PK                      |
| created_at         | DATETIME | DEFAULT CURRENT_TIMESTAMP                        |

> 🔑 **Clave primaria compuesta:** `(following_user_id, followed_user_id)`

---

## 🔗 Relaciones

- **1 usuario → N posts**
- **1 usuario → N seguidores**
- **1 usuario → N seguidos**

Diagrama (simplificado):

