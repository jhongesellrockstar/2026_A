IF DB_ID('hospital_interop') IS NULL
BEGIN
    CREATE DATABASE hospital_interop;
END
GO

USE hospital_interop;
GO

IF OBJECT_ID('establecimiento', 'U') IS NULL
BEGIN
    CREATE TABLE establecimiento (
        id_establecimiento INT IDENTITY(1,1) PRIMARY KEY,
        nombre VARCHAR(150) NOT NULL,
        tipo VARCHAR(20) CHECK (tipo IN ('Hospital', 'Clinica', 'Centro de Salud', 'Posta')),
        distrito VARCHAR(100),
        region VARCHAR(20) CHECK (region IN ('Lima', 'Callao')),
        telefono VARCHAR(20)
    );
END
GO

IF OBJECT_ID('paciente', 'U') IS NULL
BEGIN
    CREATE TABLE paciente (
        id_paciente INT IDENTITY(1,1) PRIMARY KEY,
        dni CHAR(8) NOT NULL UNIQUE,
        nombres VARCHAR(100) NOT NULL,
        apellidos VARCHAR(100) NOT NULL,
        fecha_nacimiento DATE,
        sexo CHAR(1) CHECK (sexo IN ('M', 'F')),
        direccion VARCHAR(200),
        telefono VARCHAR(20),
        seguro VARCHAR(20) CHECK (seguro IN ('SIS', 'EsSalud', 'Privado', 'Ninguno'))
    );
END
GO

IF OBJECT_ID('medico', 'U') IS NULL
BEGIN
    CREATE TABLE medico (
        id_medico INT IDENTITY(1,1) PRIMARY KEY,
        cmp VARCHAR(20) NOT NULL UNIQUE,
        nombres VARCHAR(100) NOT NULL,
        apellidos VARCHAR(100) NOT NULL,
        especialidad VARCHAR(100),
        id_establecimiento INT,
        CONSTRAINT FK_Medico_Establecimiento
            FOREIGN KEY (id_establecimiento)
            REFERENCES establecimiento(id_establecimiento)
    );
END
GO

IF OBJECT_ID('historia_clinica', 'U') IS NULL
BEGIN
    CREATE TABLE historia_clinica (
        id_historia INT IDENTITY(1,1) PRIMARY KEY,
        id_paciente INT NOT NULL UNIQUE,
        fecha_creacion DATE DEFAULT CAST(GETDATE() AS DATE),
        estado VARCHAR(20) DEFAULT 'Activo',
        CONSTRAINT FK_Historia_Paciente
            FOREIGN KEY (id_paciente)
            REFERENCES paciente(id_paciente)
    );
END
GO

IF OBJECT_ID('atencion', 'U') IS NULL
BEGIN
    CREATE TABLE atencion (
        id_atencion INT IDENTITY(1,1) PRIMARY KEY,
        id_historia INT NOT NULL,
        id_medico INT,
        id_establecimiento INT,
        fecha_hora DATETIME DEFAULT GETDATE(),
        motivo VARCHAR(MAX),
        diagnostico VARCHAR(MAX),
        tratamiento VARCHAR(MAX),
        tipo_atencion VARCHAR(20) CHECK (tipo_atencion IN ('Consulta', 'Emergencia', 'Hospitalizacion', 'Hospitalización')),
        CONSTRAINT FK_Atencion_Historia
            FOREIGN KEY (id_historia)
            REFERENCES historia_clinica(id_historia),
        CONSTRAINT FK_Atencion_Medico
            FOREIGN KEY (id_medico)
            REFERENCES medico(id_medico),
        CONSTRAINT FK_Atencion_Establecimiento
            FOREIGN KEY (id_establecimiento)
            REFERENCES establecimiento(id_establecimiento)
    );
END
GO

IF OBJECT_ID('derivacion', 'U') IS NULL
BEGIN
    CREATE TABLE derivacion (
        id_derivacion INT IDENTITY(1,1) PRIMARY KEY,
        id_atencion INT NOT NULL,
        id_establecimiento_destino INT NOT NULL,
        motivo_derivacion VARCHAR(MAX),
        estado VARCHAR(30) DEFAULT 'Pendiente',
        fecha DATETIME DEFAULT GETDATE(),
        CONSTRAINT FK_Derivacion_Atencion
            FOREIGN KEY (id_atencion)
            REFERENCES atencion(id_atencion),
        CONSTRAINT FK_Derivacion_Establecimiento
            FOREIGN KEY (id_establecimiento_destino)
            REFERENCES establecimiento(id_establecimiento)
    );
END
GO

IF OBJECT_ID('medicamento', 'U') IS NULL
BEGIN
    CREATE TABLE medicamento (
        id_medicamento INT IDENTITY(1,1) PRIMARY KEY,
        nombre VARCHAR(150) NOT NULL,
        presentacion VARCHAR(100),
        concentracion VARCHAR(50)
    );
END
GO

IF OBJECT_ID('prescripcion', 'U') IS NULL
BEGIN
    CREATE TABLE prescripcion (
        id_prescripcion INT IDENTITY(1,1) PRIMARY KEY,
        id_atencion INT NOT NULL,
        id_medicamento INT NOT NULL,
        dosis VARCHAR(100),
        frecuencia VARCHAR(100),
        duracion_dias INT,
        CONSTRAINT FK_Prescripcion_Atencion
            FOREIGN KEY (id_atencion)
            REFERENCES atencion(id_atencion),
        CONSTRAINT FK_Prescripcion_Medicamento
            FOREIGN KEY (id_medicamento)
            REFERENCES medicamento(id_medicamento)
    );
END
GO

IF NOT EXISTS (SELECT 1 FROM establecimiento WHERE nombre = 'Hospital Academico Lima Callao')
BEGIN
    INSERT INTO establecimiento (nombre, tipo, distrito, region, telefono)
    VALUES ('Hospital Academico Lima Callao', 'Hospital', 'Bellavista', 'Callao', '014000001');
END

IF NOT EXISTS (SELECT 1 FROM establecimiento WHERE nombre = 'Centro de Salud Universitario')
BEGIN
    INSERT INTO establecimiento (nombre, tipo, distrito, region, telefono)
    VALUES ('Centro de Salud Universitario', 'Centro de Salud', 'Cercado de Lima', 'Lima', '014000002');
END
GO

IF NOT EXISTS (SELECT 1 FROM medico WHERE cmp = '123456')
BEGIN
    INSERT INTO medico (cmp, nombres, apellidos, especialidad, id_establecimiento)
    SELECT '123456', 'Carlos', 'Ramirez', 'Medicina General', id_establecimiento
    FROM establecimiento
    WHERE nombre = 'Hospital Academico Lima Callao';
END

IF NOT EXISTS (SELECT 1 FROM medico WHERE cmp = 'CMP10002')
BEGIN
    INSERT INTO medico (cmp, nombres, apellidos, especialidad, id_establecimiento)
    SELECT 'CMP10002', 'Ana', 'Torres', 'Pediatria', id_establecimiento
    FROM establecimiento
    WHERE nombre = 'Centro de Salud Universitario';
END
GO

IF NOT EXISTS (SELECT 1 FROM paciente WHERE dni = '76543210')
BEGIN
    INSERT INTO paciente (dni, nombres, apellidos, fecha_nacimiento, sexo, direccion, telefono, seguro)
    VALUES ('76543210', 'Jose', 'Gomez', '1995-08-15', 'M', 'Direccion academica de prueba', '987654321', 'SIS');
END

IF NOT EXISTS (SELECT 1 FROM paciente WHERE dni = '87654321')
BEGIN
    INSERT INTO paciente (dni, nombres, apellidos, fecha_nacimiento, sexo, direccion, telefono, seguro)
    VALUES ('87654321', 'Maria', 'Lopez', '1988-05-20', 'F', 'Direccion academica de prueba', '987654322', 'EsSalud');
END
GO

IF NOT EXISTS (
    SELECT 1
    FROM historia_clinica h
    INNER JOIN paciente p ON h.id_paciente = p.id_paciente
    WHERE p.dni = '76543210'
)
BEGIN
    INSERT INTO historia_clinica (id_paciente, estado)
    SELECT id_paciente, 'Activo'
    FROM paciente
    WHERE dni = '76543210';
END

IF NOT EXISTS (
    SELECT 1
    FROM historia_clinica h
    INNER JOIN paciente p ON h.id_paciente = p.id_paciente
    WHERE p.dni = '87654321'
)
BEGIN
    INSERT INTO historia_clinica (id_paciente, estado)
    SELECT id_paciente, 'Activo'
    FROM paciente
    WHERE dni = '87654321';
END
GO

IF NOT EXISTS (SELECT 1 FROM medicamento WHERE nombre = 'Paracetamol')
BEGIN
    INSERT INTO medicamento (nombre, presentacion, concentracion)
    VALUES ('Paracetamol', 'Tabletas', '500 mg');
END

IF NOT EXISTS (SELECT 1 FROM medicamento WHERE nombre = 'Amoxicilina')
BEGIN
    INSERT INTO medicamento (nombre, presentacion, concentracion)
    VALUES ('Amoxicilina', 'Capsulas', '500 mg');
END
GO

IF NOT EXISTS (SELECT 1 FROM atencion WHERE motivo = 'Consulta academica de prueba')
BEGIN
    INSERT INTO atencion (id_historia, id_medico, id_establecimiento, motivo, diagnostico, tratamiento, tipo_atencion)
    SELECT h.id_historia, m.id_medico, m.id_establecimiento,
           'Consulta academica de prueba',
           'Paciente estable',
           'Control general y seguimiento',
           'Consulta'
    FROM historia_clinica h
    INNER JOIN paciente p ON h.id_paciente = p.id_paciente
    INNER JOIN medico m ON m.cmp = '123456'
    WHERE p.dni = '76543210';
END
GO

IF NOT EXISTS (SELECT 1 FROM derivacion WHERE motivo_derivacion = 'Evaluacion academica de referencia')
BEGIN
    INSERT INTO derivacion (id_atencion, id_establecimiento_destino, motivo_derivacion, estado)
    SELECT TOP 1 a.id_atencion, e.id_establecimiento, 'Evaluacion academica de referencia', 'Pendiente'
    FROM atencion a
    INNER JOIN establecimiento e ON e.nombre = 'Centro de Salud Universitario'
    WHERE a.motivo = 'Consulta academica de prueba';
END
GO
