-- Buscar proyectos impartidas y no archivadas (listaProyectos)
Create or replace Function BuscarProyectoImpartido(profesorid int) returns TABLE (
    id INT,
    nombre VARCHAR,
    descripcion TEXT,
    ciclo_escolar VARCHAR,
    color VARCHAR,
    codigo VARCHAR
) 
as
$$
	SELECT proyectos.id, proyectos.nombre, proyectos.descripcion, proyectos.ciclo_escolar, proyectos.color, proyectos.codigo
	FROM plataforma_proyectos as proyectos
	inner join plataforma_profesores_proyecto as profesores
	on proyectos.id = profesores.id_proyecto_id
	where profesores.id_profesor_id= profesorid
	and proyectos.achivo_proyecto = false;
$$
language sql

-- Buscar proyectos impartidas y archivadas (listaProyectos)
Create or replace Function BuscarProyectoImpartidoArchivado(profesorid int) returns TABLE (
    id INT,
    nombre VARCHAR,
    descripcion TEXT,
    ciclo_escolar VARCHAR,
    color VARCHAR,
    codigo VARCHAR
) 
as
$$
	SELECT proyectos.id, proyectos.nombre, proyectos.descripcion, proyectos.ciclo_escolar, proyectos.color, proyectos.codigo
	FROM plataforma_proyectos as proyectos
	inner join plataforma_profesores_proyecto as profesores
	on proyectos.id = profesores.id_proyecto_id
	where profesores.id_profesor_id= profesorid
	and proyectos.achivo_proyecto = true;
$$
language SQL
	
-- Buscar proyectos en curso y no archivadas (listaProyectos)
	Create or replace Function BuscarProyectos(alumnoid int) returns TABLE (
    id INT,
    nombre VARCHAR,
    descripcion TEXT,
    ciclo_escolar VARCHAR,
    color VARCHAR,
    codigo VARCHAR
) 
as
$$
SELECT proyectos.id, proyectos.nombre, proyectos.descripcion, proyectos.ciclo_escolar, proyectos.color, proyectos.codigo
	FROM plataforma_proyectos as proyectos
	inner join public.plataforma_alumnos_proyecto as alumnos
	on proyectos.id = alumnos.id_proyecto_id
	where alumnos.id_alumno_id= alumnoid
	and proyectos.achivo_proyecto = false;
$$
language SQL

-- Buscar proyectos en curso y archivadas (listaProyectos)
Create or replace Function BuscarProyectosArchivado(alumnoid int) returns TABLE (
    id INT,
    nombre VARCHAR,
    descripcion TEXT,
    ciclo_escolar VARCHAR,
    color VARCHAR,
    codigo VARCHAR
) 
as
$$
SELECT proyectos.id, proyectos.nombre, proyectos.descripcion, proyectos.ciclo_escolar, proyectos.color, proyectos.codigo
	FROM plataforma_proyectos as proyectos
	inner join public.plataforma_alumnos_proyecto as alumnos
	on proyectos.id = alumnos.id_proyecto_id
	where alumnos.id_alumno_id= alumnoid
	and proyectos.achivo_proyecto = true;
$$
language sql

-- lista de profesores por proyecto
Create or replace Function ListaProfesoresproyecto() returns TABLE (
    id INT,
    nombre VARCHAR,
    apellidos Varchar
) 
as
$$
select profesores.id_proyecto_id, datos.nombre, datos.apellidos
	from plataforma_profesores_proyecto as profesores
	inner join public.plataforma_profesor as datos
	on profesores.id_profesor_id = datos.id;
$$
language sql

-- Agregar un proyecto
drop function CrearProyectocoil(
    idUsuario INT,
    nombre_parm VARCHAR,
    materia_parm VARCHAR,
    codigo_parm VARCHAR,
    descripcion_parm TEXT,
    fecha_inicio_parm DATE,
    fecha_fin_parm DATE,
    ciclo_escolar_parm VARCHAR,
    color_parm VARCHAR
);
CREATE OR REPLACE FUNCTION CrearProyectocoil(
    idUsuario INT default NULL,
    nombre_parm VARCHAR default NULL,
    materia_parm VARCHAR default NULL,
    codigo_parm VARCHAR default NULL,
    descripcion_parm text default NULL,
    fecha_inicio_parm DATE default NULL,
    fecha_fin_parm DATE default NULL,
    ciclo_escolar_parm VARCHAR default NULL,
    color_parm VARCHAR default NULL
) RETURNS VARCHAR AS
$$
DECLARE
    proyecto INT;
begin
	
	-- Inserta en la tabla de proyectos
     INSERT INTO public.plataforma_proyectos (
        nombre, materia, codigo, descripcion, fecha_inicio, fecha_fin, ciclo_escolar, achivo_proyecto, color, id_profesor_id, enlace_zoom
    )
    VALUES (nombre_parm, materia_parm, codigo_parm, descripcion_parm, fecha_inicio_parm, fecha_fin_parm, ciclo_escolar_parm, false, color_parm, idUsuario, NULL)
	RETURNING id INTO proyecto;

    -- Inserta en la tabla de profesores_proyecto
    INSERT INTO public.plataforma_profesores_proyecto (
        fecha_ingreso, id_proyecto_id, id_profesor_id
    )
    VALUES (CURRENT_DATE, proyecto, idUsuario);

    -- Inserta en la tabla de temas
    INSERT INTO public.plataforma_fases (titulo, puntuacion, id_proyecto_id)
    VALUES ('Fase 1: Conozcamonos', '20', proyecto),
           ('Fase 2: Organicémonos', '20', proyecto),
           ('Fase 3: Manos a la obra', '20', proyecto),
           ('Fase 4: Lúcete', '20', proyecto),
           ('Fase 5: Reflexionemos', '20', proyecto);

    RETURN 'Proyecto creado exitosamente';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error en la base de datos codigo: '|| SQLSTATE;
END;
$$
LANGUAGE plpgsql;

--verficar codigo distinto
CREATE OR REPLACE FUNCTION CodigosClase() RETURNS SETOF varchar AS
$$
    SELECT codigo FROM public.plataforma_proyectos;
$$
LANGUAGE SQL;

-- Ver si el alumno esta en el proyecto
Create or replace Function ComprobarAlumnoProyecto(alumnoid int, codigo_parm varchar) returns varchar
as
$$
	select proyectos.codigo from public.plataforma_proyectos as proyectos
	inner join public.plataforma_alumnos_proyecto as alumnos
	on proyectos.id = alumnos.id_proyecto_id
	where proyectos.codigo= codigo_parm
	and alumnos.id_alumno_id = alumnoid;
$$
language sql

-- agregar Alumno a proyecto
CREATE OR REPLACE FUNCTION AgregarAlumno(
    idUsuario INT,
    idProyecto INT
) RETURNS VARCHAR AS
$$
DECLARE
    proyecto INT;
BEGIN

   -- Inserta en la tabla de alumnos_proyecto
    INSERT INTO public.plataforma_alumnos_proyecto(
        fecha_ingreso, id_proyecto_id, id_alumno_id
    )
    VALUES (CURRENT_DATE, idProyecto, idUsuario);

    RETURN 'Agregado exitosamente';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error en la base de datos codigo: '+SQLSTATE;
END;
$$
LANGUAGE plpgsql;

--obtener id por codigo
CREATE OR REPLACE FUNCTION buscarProyectoPorCodigo(codigo_param varchar) RETURNS SETOF int AS
$$
    SELECT proyectos.id FROM plataforma_proyectos as proyectos WHERE proyectos.codigo = codigo_param;
$$
LANGUAGE SQL;

-- Buscar nombre proyectos impartidas y no archivadas (listaProyectos)
Create or replace Function BuscarProyectoNombreImpartido(profesorid int) returns TABLE (
    id INT,
    nombre VARCHAR,
    color VARCHAR,
    codigo VARCHAR
) 
as
$$
	SELECT proyectos.id, proyectos.nombre, proyectos.color, proyectos.codigo
	FROM plataforma_proyectos as proyectos
	inner join plataforma_profesores_proyecto as profesores
	on proyectos.id = profesores.id_proyecto_id
	where profesores.id_profesor_id= profesorid
	and proyectos.achivo_proyecto = false;
$$
language sql

-- Buscar nombre proyectos en curso y no archivadas (listaProyectos)
	Create or replace Function BuscarNombreProyectos(alumnoid int) returns TABLE (
    id INT,
    nombre VARCHAR,
    color VARCHAR,
    codigo VARCHAR
) 
as
$$
SELECT proyectos.id, proyectos.nombre, proyectos.color, proyectos.codigo
	FROM plataforma_proyectos as proyectos
	inner join public.plataforma_alumnos_proyecto as alumnos
	on proyectos.id = alumnos.id_proyecto_id
	where alumnos.id_alumno_id= alumnoid
	and proyectos.achivo_proyecto = false;
$$
language sql

--Buscar nombre proyecto por codigo
	Create or replace Function BuscarNombreProyectosByCodigo(codigo_parm varchar) returns varchar
as
$$
select nombre from plataforma_proyectos
	where codigo = codigo_parm;
$$
language sql

-- Ver si el profesor esta en el proyecto
Create or replace Function ComprobarProfesorProyecto(profesorid int, codigo_parm varchar) returns varchar
as
$$
	select proyectos.codigo from public.plataforma_proyectos as proyectos
	inner join plataforma_profesores_proyecto as profesores
	on proyectos.id = profesores.id_proyecto_id
	where proyectos.codigo= codigo_parm
	and profesores.id_profesor_id = profesorid;
$$
language sql

-- agregar Profesor a proyecto
CREATE OR REPLACE FUNCTION AgregarProfesor(
    idProfesor INT,
    idProyecto INT
) RETURNS VARCHAR AS
$$
DECLARE
    proyecto INT;
BEGIN

    -- Inserta en la tabla de alumnos_proyecto
    INSERT INTO plataforma_profesores_proyecto(
        fecha_ingreso, id_proyecto_id, id_profesor_id
    )
    VALUES (CURRENT_DATE, idProyecto, idProfesor);

    RETURN 'Agregado exitosamente';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error en la base de datos codigo: '+SQLSTATE;
END;
$$
LANGUAGE plpgsql;

-- Buscar proyecto por codigo
drop function BuscarProyectoByCodigo(varchar);
CREATE OR REPLACE FUNCTION BuscarProyectoByCodigo(
    codigo_parm VARCHAR
) RETURNS TABLE (
    id INT8,
    nombre VARCHAR,
    materia VARCHAR,
    codigo VARCHAR,
    descripcion TEXT,
    fecha_inicio DATE,
    fecha_fin DATE,
    ciclo_escolar TEXT,
    archivo_proyecto BOOLEAN,
    color VARCHAR,
    enlace_zoom text,
    id_profesor_id int8
)
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM public.plataforma_proyectos
    WHERE plataforma_proyectos.codigo = codigo_parm;
END;
$$ LANGUAGE plpgsql;

-- listar profesores proyectos
drop function BuscarProyectoProfesores(int)
CREATE OR REPLACE FUNCTION BuscarProyectoProfesores(
    codigo_parm int
) RETURNS TABLE (
    nombre VARCHAR,
    apellidos VARCHAR,
    profesor int8
)
AS $$
BEGIN
    RETURN QUERY
    select profesor.nombre, profesor.apellidos, profesor.id 
    from public.plataforma_profesores_proyecto as proyectoProfesor
	inner join public.plataforma_profesor as profesor
	on profesor.id = proyectoProfesor.id_profesor_id 
	where proyectoprofesor.id_proyecto_id = codigo_parm;
END;
$$ LANGUAGE plpgsql;

-- listar alumnos proyectos
drop function BuscarProyectoAlumnos(int);
CREATE OR REPLACE FUNCTION BuscarProyectoAlumnos(
    codigo_parm int
) RETURNS TABLE (
    nombre VARCHAR,
    apellidos VARCHAR,
    id int8
)
AS $$
BEGIN
    RETURN QUERY
    select alumnos.nombre, alumnos.apellidos, alumnos.id 
    from public.plataforma_alumnos_proyecto as proyectoAlumno
	inner join public.plataforma_alumno as alumnos
	on alumnos.id = proyectoAlumno.id_alumno_id
	where proyectoAlumno.id_proyecto_id = codigo_parm;
END;
$$ LANGUAGE plpgsql;

-- Listar fases por proyecto
CREATE OR REPLACE FUNCTION ListasFasesByProyecto(
    codigo_parm int
) RETURNS TABLE (
    id int8,
    titulo varchar,
    puntuacion varchar,
    id_proyecto_id int8
)
AS $$
BEGIN
    RETURN QUERY
    select fases.id, fases.titulo, fases.puntuacion, fases.id_proyecto_id from public.plataforma_fases as fases
	where fases.id_proyecto_id = codigo_parm;
END;
$$ LANGUAGE plpgsql;

-- agregar Profesor a proyecto
CREATE OR REPLACE FUNCTION AgregarProfesor(
    idProfesor INT,
    idProyecto INT
) RETURNS VARCHAR AS
$$
DECLARE
    proyecto INT;
BEGIN

    -- Inserta en la tabla de alumnos_proyecto
    INSERT INTO plataforma_profesores_proyecto(
        fecha_ingreso, id_proyecto_id, id_profesor_id
    )
    VALUES (CURRENT_DATE, idProyecto, idProfesor);

    RETURN 'Agregado exitosamente';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error en la base de datos codigo: '+SQLSTATE;
END;
$$
LANGUAGE plpgsql;

--actaulizar datos proyecto
Create or replace Function EditarProyecto(
	id_parm int,
	nombre_parm varchar,
	materia_parm varchar,
	descripcion_parm varchar,
	fecha_inicio_parm date,
	fecha_fin_parm date,
	ciclo_escolar_parm varchar,
	color_parm varchar
) returns varchar
as
$$
BEGIN
	UPDATE public.plataforma_proyectos
	SET nombre=nombre_parm, materia=materia_parm, descripcion=descripcion_parm, fecha_inicio=fecha_inicio_parm, fecha_fin=fecha_fin_parm, ciclo_escolar=ciclo_escolar_parm, color=color_parm
	WHERE id= id_parm;
    RETURN 'Agregado exitosamente';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error en la base de datos codigo: '||SQLSTATE;
END;
$$
LANGUAGE plpgsql;

--Actualizar zoom proyecto
Create or replace Function ZoomProyecto(
	id_parm int,
	enlace_parm varchar
) returns varchar
as
$$
BEGIN
	UPDATE public.plataforma_proyectos
	SET  enlace_zoom=enlace_parm
	WHERE id=id_parm;
	RETURN 'Agregado exitosamente';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error en la base de datos codigo: '+SQLSTATE;
END;
$$
LANGUAGE plpgsql;

--Archivar proyecto
Create or replace Function ArchivoProyecto(
	id_parm int
) returns varchar
as
$$
BEGIN
	UPDATE public.plataforma_proyectos
	SET achivo_proyecto=true
	WHERE id=id_parm;
	RETURN 'Agregado exitosamente';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error en la base de datos codigo: '+SQLSTATE;
END;
$$
LANGUAGE plpgsql;

--Reactivar proyecto
Create or replace Function ReactivarProyecto(
	id_parm int
) returns varchar
as
$$
BEGIN
	UPDATE public.plataforma_proyectos
	SET achivo_proyecto=false
	WHERE id=id_parm;
	RETURN 'Agregado exitosamente';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error en la base de datos codigo: '||SQLSTATE;
END;
$$
LANGUAGE plpgsql;

--Agregar Anuncio Profesor
Create or replace Function AnuncioProfesor(
	comentario_parm text,
	id_profesor_parm int,
	id_proyecto_parm int
) returns varchar
as
$$
BEGIN
	INSERT INTO public.plataforma_anuncios
	(comentario, fecha, fecha_edit, id_alumno_id, id_profesor_id, id_proyecto_id)
	VALUES(comentario_parm, CURRENT_DATE, CURRENT_DATE, NULL, id_profesor_parm, id_proyecto_parm);
	RETURN 'Agregado exitosamente';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error en la base de datos codigo: '+SQLSTATE;
END;
$$
LANGUAGE plpgsql;

--Agregar Anuncio Alumno
Create or replace Function AnuncioAlumno(
	comentario_parm text,
	id_alumno_parm int,
	id_proyecto_parm int
) returns varchar
as
$$
BEGIN
	INSERT INTO public.plataforma_anuncios
	(comentario, fecha, fecha_edit, id_alumno_id, id_profesor_id, id_proyecto_id)
	VALUES(comentario_parm, CURRENT_DATE, CURRENT_DATE, id_alumno_parm, NULL, id_proyecto_parm);
	RETURN 'Agregado exitosamente';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error en la base de datos codigo: '||SQLSTATE;
END;
$$
LANGUAGE plpgsql;

-- ver anuncios
drop FUNCTION obtener_anuncios(id_proyecto INT);
CREATE OR REPLACE FUNCTION obtener_anuncios(id_proyecto INT)
RETURNS TABLE (
    id INT8,
    comentario TEXT,
    fecha date,
    fecha_edit date,
    nombre varchar,
    apellidos varchar,
    id_proyecto_id INT8
) AS $$
BEGIN
    RETURN QUERY 
    SELECT anuncio.id, anuncio.comentario, anuncio.fecha, anuncio.fecha_edit, alumno.nombre, alumno.apellidos, anuncio.id_proyecto_id
    FROM plataforma_anuncios AS anuncio
    INNER JOIN public.plataforma_alumno AS alumno ON anuncio.id_alumno_id = alumno.id 
    WHERE anuncio.id_proyecto_id = id_proyecto
    UNION ALL
    SELECT anuncio.id, anuncio.comentario, anuncio.fecha, anuncio.fecha_edit, profesor.nombre, profesor.apellidos, anuncio.id_proyecto_id
    FROM plataforma_anuncios AS anuncio
    INNER JOIN public.plataforma_profesor AS profesor ON anuncio.id_profesor_id = profesor.id 
    WHERE anuncio.id_proyecto_id = id_proyecto
    ORDER BY fecha_edit DESC;  -- Ordenar por fecha_edit descendente
END;
$$ LANGUAGE plpgsql;



select obtener_anuncios(2);




SELECT anuncio.id, anuncio.comentario, anuncio.fecha, anuncio.fecha_edit, alumno.nombre , alumno.apellidos , anuncio.id_proyecto_id
	FROM plataforma_anuncios as anuncio
	inner join public.plataforma_alumno as alumno
	on anuncio.id_alumno_id = alumno.id 
	where anuncio.id_proyecto_id = 2;

SELECT anuncio.id, anuncio.comentario, anuncio.fecha, anuncio.fecha_edit, profesor.nombre , profesor.apellidos , anuncio.id_proyecto_id
	FROM plataforma_anuncios as anuncio
	inner join public.plataforma_profesor as profesor
	on anuncio.id_profesor_id = profesor.id 
	where anuncio.id_proyecto_id = 2;

--pruebas
select ListasFasesByProyecto(3);
select * from public.plataforma_fases
where id_proyecto_id = 3;
select * from public.plataforma_proyectos;
select BuscarProyectoByCodigo('599919798');
SELECT public.buscarproyectobycodigo(:codigo_parm);
select profesor.nombre, profesor.apellidos from public.plataforma_profesores_proyecto as proyectoProfesor
inner join public.plataforma_profesor as profesor
on profesor.id = proyectoProfesor.id_profesor_id 
where proyectoprofesor.id_proyecto_id ;

delete from public.plataforma_profesores_proyecto;
delete from public.plataforma_alumnos_proyecto;
delete from public.plataforma_fases;
delete from public.plataforma_proyectos;
delete from public.plataforma_alumno;

delete from public.plataforma_profesor;
delete from public.plataforma_usuario;