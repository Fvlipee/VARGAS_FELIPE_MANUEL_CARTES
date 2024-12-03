-- Creación de Tablas

-- Tabla ROLES
CREATE TABLE ROLES (
    id_rol INT NOT NULL PRIMARY KEY,
    nombre_rol VARCHAR(25) NOT NULL,
    descripcion_rol VARCHAR(200)
);

-- Tabla USUARIOS
CREATE TABLE USUARIOS (
    id_usuario INT NOT NULL PRIMARY KEY,
    usuario VARCHAR(25) NOT NULL,
    contrasena VARCHAR(25) NOT NULL,
    ultimo_acceso DATE,
    id_rol INT NOT NULL,
    FOREIGN KEY (id_rol) REFERENCES ROLES(id_rol)
);

-- Tabla PACIENTE
CREATE TABLE PACIENTE (
    id_paciente INT NOT NULL PRIMARY KEY,
    nombre_paciente VARCHAR(50) NOT NULL,
    apellido_paciente VARCHAR(50) NOT NULL,
    fecha_nacimiento_pac DATE NOT NULL,
    correo_pac VARCHAR(50),
    telefono_pac INT NOT NULL,
    direccion_pac VARCHAR(50),
    fecha_registro_pac DATE,
    estado_pac VARCHAR(20)
);

-- Tabla TERAPEUTA
CREATE TABLE TERAPEUTA (
    id_terapeuta INT NOT NULL PRIMARY KEY,
    nombre_terapeuta VARCHAR(50) NOT NULL,
    apellido_terapeuta VARCHAR(50) NOT NULL,
    especialidad VARCHAR(30),
    correo_ter VARCHAR(50),
    telefono_ter INT NOT NULL,
    fecha_registro_ter DATE,
    estado_ter VARCHAR(20)
);

-- Tabla SESIONES
CREATE TABLE SESIONES (
    id_sesion INT NOT NULL PRIMARY KEY,
    fecha_sesion DATE NOT NULL,
    hora_inicio DATE NOT NULL,
    hora_fin DATE NOT NULL,
    estado_sesion VARCHAR(20),
    id_terapeuta INT NOT NULL,
    id_paciente INT NOT NULL,
    FOREIGN KEY (id_terapeuta) REFERENCES TERAPEUTA(id_terapeuta),
    FOREIGN KEY (id_paciente) REFERENCES PACIENTE(id_paciente)
);

-- Tabla ACTIVIDADES
CREATE TABLE ACTIVIDADES (
    id_actividad INT NOT NULL PRIMARY KEY,
    descripcion VARCHAR(75),
    tipo VARCHAR(25),
    estado_actividad VARCHAR(20),
    fecha_asignada DATE,
    id_sesion INT NOT NULL,
    FOREIGN KEY (id_sesion) REFERENCES SESIONES(id_sesion)
);

-- Tabla ARCHIVOS
CREATE TABLE ARCHIVOS (
    id_archivo INT NOT NULL PRIMARY KEY,
    tipo_archivo VARCHAR(25),
    fecha_subida DATE,
    id_actividad INT NOT NULL,
    id_paciente INT NOT NULL,
    FOREIGN KEY (id_actividad) REFERENCES ACTIVIDADES(id_actividad),
    FOREIGN KEY (id_paciente) REFERENCES PACIENTE(id_paciente)
);

-- Tabla EVALUACIONES
CREATE TABLE EVALUACIONES (
    id_evaluacion INT NOT NULL PRIMARY KEY,
    resultado VARCHAR(25),
    comentarios VARCHAR(200),
    fecha_evaluacion DATE,
    id_sesion INT NOT NULL,
    id_paciente INT NOT NULL,
    id_terapeuta INT NOT NULL,
    FOREIGN KEY (id_sesion) REFERENCES SESIONES(id_sesion),
    FOREIGN KEY (id_paciente) REFERENCES PACIENTE(id_paciente),
    FOREIGN KEY (id_terapeuta) REFERENCES TERAPEUTA(id_terapeuta)
);

-- Nueva Tabla FICHA_SESION
CREATE TABLE FICHA_SESION (
    id_ficha INT NOT NULL PRIMARY KEY,                
    fecha_sesion DATE NOT NULL,                       
    objetivo_sesion VARCHAR(500) NOT NULL,            
    desarrollo_sesion BLOB,                           
    id_sesion INT NOT NULL,                           
    FOREIGN KEY (id_sesion) REFERENCES SESIONES(id_sesion)  
);
