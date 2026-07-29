USE hospital_interop;
GO

IF COL_LENGTH('paciente', 'telefono') IS NULL
BEGIN
    ALTER TABLE paciente ADD telefono VARCHAR(20) NULL;
END
GO

IF COL_LENGTH('paciente', 'direccion') IS NULL
BEGIN
    ALTER TABLE paciente ADD direccion VARCHAR(200) NULL;
END
GO

IF NOT EXISTS (SELECT 1 FROM paciente WHERE dni = '11223344')
BEGIN
    INSERT INTO paciente (dni, nombres, apellidos, fecha_nacimiento, sexo, direccion, telefono, seguro)
    VALUES ('11223344', 'Luis Alberto', 'Rojas Medina', '1990-01-01', 'M', 'Direccion academica de prueba', '987654321', 'SIS');
END
GO

IF NOT EXISTS (
    SELECT 1
    FROM historia_clinica h
    INNER JOIN paciente p ON h.id_paciente = p.id_paciente
    WHERE p.dni = '11223344'
)
BEGIN
    INSERT INTO historia_clinica (id_paciente, estado)
    SELECT id_paciente, 'Activo'
    FROM paciente
    WHERE dni = '11223344';
END
GO

IF NOT EXISTS (
    SELECT 1
    FROM derivacion d
    INNER JOIN atencion a ON d.id_atencion = a.id_atencion
    INNER JOIN historia_clinica h ON a.id_historia = h.id_historia
    INNER JOIN paciente p ON h.id_paciente = p.id_paciente
    WHERE p.dni = '11223344'
      AND d.motivo_derivacion = 'Evaluacion por cardiologia'
)
BEGIN
    DECLARE @id_atencion INT;

    INSERT INTO atencion (id_historia, id_medico, id_establecimiento, motivo, diagnostico, tratamiento, tipo_atencion)
    SELECT TOP 1 h.id_historia, m.id_medico, m.id_establecimiento,
           'Derivacion directa por DNI',
           'Paciente derivado para evaluacion especializada',
           'Pendiente de evaluacion en establecimiento destino',
           'Consulta'
    FROM historia_clinica h
    INNER JOIN paciente p ON h.id_paciente = p.id_paciente
    INNER JOIN medico m ON m.cmp = '123456'
    WHERE p.dni = '11223344';

    SET @id_atencion = SCOPE_IDENTITY();

    INSERT INTO derivacion (id_atencion, id_establecimiento_destino, motivo_derivacion, estado)
    SELECT TOP 1 @id_atencion, e.id_establecimiento, 'Evaluacion por cardiologia', 'Pendiente'
    FROM establecimiento e
    WHERE e.nombre = 'Centro de Salud Universitario';
END
GO
