-- Buscar proyectos impartidas y no archivadas (listaProyectos)
Create or replace Function BuscarProyectoImpartido(profesorid int) returns TABLE (
    id INT,
    nombre VARCHAR,
    descripcion TEXT,
    ciclo_escolar VARCHAR,
    color VARCHAR,
    codigo VARCHAR,
    nombre_completo varchar[]
) 
as
$$
	SELECT proyectos.id, proyectos.nombre, proyectos.descripcion, proyectos.ciclo_escolar, proyectos.color, proyectos.codigo, ARRAY_AGG(CONCAT(datosp.nombre, ' ', datosp.apellidos)) AS nombre_completo
	FROM plataforma_proyectos as proyectos
	inner join plataforma_profesores_proyecto as profesor
	on proyectos.id = profesor.id_proyecto_id
	inner join public.plataforma_profesores_proyecto as profesores
	on profesores.id_proyecto_id = proyectos.id 
	inner join public.plataforma_profesor as datosp
	ON profesores.id_profesor_id = datosp.id
	where profesor.id_profesor_id= profesorid
	and proyectos.achivo_proyecto = false
	GROUP BY proyectos.id, proyectos.nombre, proyectos.materia, proyectos.codigo, proyectos.descripcion, proyectos.color, proyectos.achivo_proyecto;
$$
language sql

-- Buscar proyectos impartidas y archivadas (listaProyectos)
drop function BuscarProyectoImpartidoArchivado(profesorid int);
Create or replace Function BuscarProyectoImpartidoArchivado(profesorid int) returns TABLE (
    id INT,
    nombre VARCHAR,
    descripcion TEXT,
    ciclo_escolar VARCHAR,
    color VARCHAR,
    codigo VARCHAR,
    nombre_completo varchar[]
) 
as
$$
	SELECT proyectos.id, proyectos.nombre, proyectos.descripcion, proyectos.ciclo_escolar, proyectos.color, proyectos.codigo, ARRAY_AGG(CONCAT(datosp.nombre, ' ', datosp.apellidos)) AS nombre_completo
	FROM plataforma_proyectos as proyectos
	inner join plataforma_profesores_proyecto as profesor
	on proyectos.id = profesor.id_proyecto_id
	inner join public.plataforma_profesores_proyecto as profesores
	on profesores.id_proyecto_id = proyectos.id 
	inner join public.plataforma_profesor as datosp
	ON profesores.id_profesor_id = datosp.id
	where profesor.id_profesor_id= profesorid
	and proyectos.achivo_proyecto = true
	GROUP BY proyectos.id, proyectos.nombre, proyectos.materia, proyectos.codigo, proyectos.descripcion, proyectos.color, proyectos.achivo_proyecto;
$$
language sql
	
-- Buscar proyectos en curso y no archivadas (listaProyectos)
drop function BuscarProyectos(alumnoid int);
	Create or replace Function BuscarProyectos(alumnoid int) returns TABLE (
    id INT,
    nombre VARCHAR,
    descripcion TEXT,
    ciclo_escolar VARCHAR,
    color VARCHAR,
    codigo VARCHAR,
    nombre_completo varchar[]
) 
as
$$
SELECT proyectos.id, proyectos.nombre, proyectos.descripcion, proyectos.ciclo_escolar, proyectos.color, proyectos.codigo, ARRAY_AGG(CONCAT(datosp.nombre, ' ', datosp.apellidos)) AS nombre_completo
	FROM plataforma_proyectos as proyectos
	inner join public.plataforma_alumnos_proyecto as alumnos
	on proyectos.id = alumnos.id_proyecto_id
	inner join public.plataforma_profesores_proyecto as profesores
	on profesores.id_proyecto_id = proyectos.id 
	inner join public.plataforma_profesor as datosp
	ON profesores.id_profesor_id = datosp.id
	where alumnos.id_alumno_id= alumnoid
	and proyectos.achivo_proyecto = false
	GROUP BY proyectos.id, proyectos.nombre, proyectos.materia, proyectos.codigo, proyectos.descripcion, proyectos.color, proyectos.achivo_proyecto;

$$
language SQL

-- Buscar proyectos en curso y archivadas (listaProyectos)
drop function BuscarProyectosArchivado(alumnoid int);
Create or replace Function BuscarProyectosArchivado(alumnoid int) returns TABLE (
    id INT,
    nombre VARCHAR,
    descripcion TEXT,
    ciclo_escolar VARCHAR,
    color VARCHAR,
    codigo VARCHAR,
    nombre_completo varchar[]
) 
as
$$
SELECT proyectos.id, proyectos.nombre, proyectos.descripcion, proyectos.ciclo_escolar, proyectos.color, proyectos.codigo, ARRAY_AGG(CONCAT(datosp.nombre, ' ', datosp.apellidos)) AS nombre_completo
	FROM plataforma_proyectos as proyectos
	inner join public.plataforma_alumnos_proyecto as alumnos
	on proyectos.id = alumnos.id_proyecto_id
	inner join public.plataforma_profesores_proyecto as profesores
	on profesores.id_proyecto_id = proyectos.id 
	inner join public.plataforma_profesor as datosp
	ON profesores.id_profesor_id = datosp.id
	where alumnos.id_alumno_id= alumnoid
	and proyectos.achivo_proyecto = true
	GROUP BY proyectos.id, proyectos.nombre, proyectos.materia, proyectos.codigo, proyectos.descripcion, proyectos.color, proyectos.achivo_proyecto;

$$
language SQL

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
    VALUES (nombre_parm, materia_parm, codigo_parm, descripcion_parm, fecha_inicio_parm, fecha_fin_parm, ciclo_escolar_parm, false, color_parm, idUsuario, '')
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
        RETURN 'No se han insertado los datos';
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
        RETURN 'Error no se han guardado los datos';
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
        RETURN 'Error no se han insertado los datos';
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
    profesor int8,
    trayectoria_academica text,
    trayectoria_profesional text,
    decripcion text,
    gustos_personales text
)
AS $$
BEGIN
    RETURN QUERY
    select profesor.nombre, profesor.apellidos, profesor.id, profesor.trayectoria_academica, profesor.trayectoria_profesional, profesor.descripcion, profesor.gustos_personales
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
        RETURN 'Error no se registraron los datos';
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
        RETURN 'Error no se han guardado los cambios';
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
        RETURN 'Error el url no se ha guardado';
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
        RETURN 'Error no se ha podido archivar';
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
        RETURN 'Error el proyecto no se pudo activar';
END;
$$
LANGUAGE plpgsql;



-- ver anuncios
drop FUNCTION obtener_anuncios(id_proyecto INT);
CREATE OR REPLACE FUNCTION obtener_anuncios(id_proyecto INT)
RETURNS TABLE (
    id INT8,
    comentario TEXT,
    fecha timestamptz,
    fecha_edit timestamptz,
    nombre varchar,
    apellidos varchar,
    id_alumno_id INT8,
    id_profesor_id INT8
) AS $$
BEGIN
    RETURN QUERY 
    SELECT anuncio.id, anuncio.comentario, anuncio.fecha, anuncio.fecha_edit, alumno.nombre, alumno.apellidos, anuncio.id_alumno_id, anuncio.id_profesor_id 
    FROM plataforma_anuncios AS anuncio
    INNER JOIN public.plataforma_alumno AS alumno ON anuncio.id_alumno_id = alumno.id 
    WHERE anuncio.id_proyecto_id = id_proyecto
    UNION ALL
    SELECT anuncio.id, anuncio.comentario, anuncio.fecha, anuncio.fecha_edit, profesor.nombre, profesor.apellidos, anuncio.id_alumno_id, anuncio.id_profesor_id 
    FROM plataforma_anuncios AS anuncio
    INNER JOIN public.plataforma_profesor AS profesor ON anuncio.id_profesor_id = profesor.id 
    WHERE anuncio.id_proyecto_id = id_proyecto
    ORDER BY fecha DESC;  -- Ordenar por fecha_edit descendente
END;
$$ LANGUAGE plpgsql;

--comentar Anuncio Profesor
Create or replace Function ComentarAnuncioProfesor(
	comentario_parm text,
	id_profesor_parm int,
	id_anuncio_parm int
) returns varchar
as
$$
BEGIN
	INSERT INTO public.plataforma_anuncios_comentarios
	(comentario, fecha, fecha_edit, id_alumno_id, id_profesor_id, id_anuncio_id)
	VALUES(comentario_parm, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, id_profesor_parm, id_anuncio_parm);
	RETURN 'Agregado exitosamente';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error no se comento el anuncio';
END;
$$
LANGUAGE plpgsql;

--Comentario Anuncio Alumno
Create or replace Function ComentarAnuncioAlumno(
	comentario_parm text,
	id_alumno_parm int,
	id_anuncio_parm int
) returns varchar
as
$$
BEGIN
	INSERT INTO public.plataforma_anuncios_comentarios
	(comentario, fecha, fecha_edit, id_alumno_id, id_profesor_id, id_anuncio_id)
	VALUES(comentario_parm, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, id_alumno_parm, NULL, id_anuncio_parm);
	RETURN 'Agregado exitosamente';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error no se comento el anuncio';
END;
$$
LANGUAGE plpgsql;

-- ver comentarios de un anuncio
drop function obtener_comentarios(id_anuncio_parm BIGINT);
CREATE OR REPLACE FUNCTION obtener_comentarios(id_anuncio_parm BIGINT)
RETURNS TABLE (
    id INT8,
    comentario TEXT,
    fecha timestamptz,
    fecha_edit timestamptz,
    nombre varchar,
    apellidos varchar,
    id_anuncio_id int8,
    id_alumno_id INT8,
    id_profesor_id INT8
) AS $$
BEGIN
    RETURN QUERY 
    SELECT comentario.id, comentario.comentario, comentario.fecha, comentario.fecha_edit, comentarioalumno.nombre, comentarioalumno.apellidos, comentario.id_anuncio_id, comentario.id_alumno_id , comentario.id_profesor_id 
    FROM public.plataforma_anuncios_comentarios AS comentario
    INNER JOIN public.plataforma_alumno AS comentarioalumno ON comentario.id_alumno_id = comentarioalumno.id 
    WHERE comentario.id_anuncio_id = id_anuncio_parm
    UNION ALL
    SELECT comentario.id, comentario.comentario, comentario.fecha, comentario.fecha_edit, comentarioprofesor.nombre, comentarioprofesor.apellidos, comentario.id_anuncio_id, comentario.id_alumno_id , comentario.id_profesor_id 
    FROM public.plataforma_anuncios_comentarios AS comentario
    INNER JOIN public.plataforma_profesor AS comentarioprofesor ON comentario.id_profesor_id = comentarioprofesor.id 
    WHERE comentario.id_anuncio_id = id_anuncio_parm
    ORDER BY fecha asc ;   -- Ordenar por fecha_edit descendente
END;
$$ LANGUAGE plpgsql;

--eliminar comentario
Create or replace Function EliminarComentario(
	id_parm int
) returns varchar
as
$$
BEGIN
	DELETE FROM public.plataforma_anuncios_comentarios
	WHERE id= id_parm;
	RETURN 'Eliminar exitosamente';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error no se elimino el comentario';
END;
$$
LANGUAGE plpgsql;

--Funciones para materiales BY Mateo y el Dani
--Insertar material
drop function insertarMaterial(text,int,int,varchar);
Create or replace Function insertarMaterial(
	tema_parm varchar,
	descripcion_parm text,
	fechar_parm date,
 	id_fase_parm int,
 	id_profesor_parm int 	
) returns varchar
as
$$
BEGIN
	INSERT INTO public.plataforma_materiales
	(descripcion, fecha, id_fase, id_profesor, tema)
	VALUES(descripcion_parm, fechar_parm, id_fase_parm, id_profesor_parm, tema_parm);
	RETURN 'Agregado exitosamente';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error no se agrego el material';
END;
$$
LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS BuscarAlumnoComentariobyID(int);

--Buscar profesor por id de comentario
CREATE OR REPLACE FUNCTION BuscarProfesorComentariobyID(
    id_parm int
) RETURNS int AS
$$
DECLARE
    resultado int;
BEGIN
    SELECT id_profesor_id INTO resultado FROM public.plataforma_anuncios_comentarios
    WHERE id = id_parm;
    RETURN resultado;
END;
$$ LANGUAGE plpgsql;

--Buscar alumno por id de comentario
CREATE OR REPLACE FUNCTION BuscarAlumnoComentariobyID(
    id_parm int
) RETURNS int AS
$$
DECLARE
    resultado int;
BEGIN
    SELECT id_alumno_id INTO resultado FROM public.plataforma_anuncios_comentarios
    WHERE id = id_parm;
    RETURN resultado;
END;
$$ LANGUAGE plpgsql;

--eliminar un comentario por id
Create or replace Function EliminarComentario(
	id_parm int
) returns varchar
as
$$
BEGIN
	DELETE FROM public.plataforma_anuncios_comentarios
	WHERE id= id_parm;
	RETURN 'Eliminar exitosamente';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error no se elimino el comentario';
END;
$$
LANGUAGE plpgsql;

--editar comentario
Create or replace Function EditarComentario(
	id_parm int,
	comentario_parm text 
) returns varchar
as
$$
BEGIN
	UPDATE public.plataforma_anuncios_comentarios
	SET comentario=comentario_parm, fecha_edit=CURRENT_TIMESTAMP
	WHERE id=id_parm;
	RETURN 'Editado exitosamente';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error no se edito el comentario';
END;
$$
LANGUAGE plpgsql;

--ver contenido de material
CREATE OR REPLACE FUNCTION obtener_material_por_id(material_id INT)
RETURNS TABLE (
    id INT8,
    nombre VARCHAR,
    apellidos VARCHAR,
    tema VARCHAR,
    descripcion TEXT,
    fecha DATE
) AS $$
BEGIN
    RETURN QUERY
    SELECT materiales.id, profesor.nombre, profesor.apellidos, materiales.tema, materiales.descripcion, materiales.fecha
    FROM public.plataforma_materiales AS materiales
    INNER JOIN public.plataforma_profesor AS profesor
    ON materiales.id_profesor = profesor.id
    WHERE materiales.id = material_id;
END;
$$ LANGUAGE plpgsql;

-- agregar enlaces a los comentarios
CREATE OR REPLACE FUNCTION enlacesAnuncio(
    titulo_parm TEXT,
    path_parm TEXT,
    id_anuncios_parm INT
) RETURNS VARCHAR
AS
$$
BEGIN
    INSERT INTO public.plataforma_anuncios_enlaces
    (titulo, "path", fecha, id_anuncio_id)
    VALUES (titulo_parm, path_parm, CURRENT_DATE, id_anuncios_parm);
    RETURN 'Agregado exitosamente';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error: no se agrego los enlaces';
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
DECLARE
    resultado int;
BEGIN
	INSERT INTO public.plataforma_anuncios
	(comentario, fecha, fecha_edit, id_alumno_id, id_profesor_id, id_proyecto_id)
	VALUES(comentario_parm, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, id_profesor_parm, id_proyecto_parm)
	RETURNING id INTO resultado;
	RETURN resultado;
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error no se publico el anuncio';
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
DECLARE
    resultado int;
BEGIN
	INSERT INTO public.plataforma_anuncios
	(comentario, fecha, fecha_edit, id_alumno_id, id_profesor_id, id_proyecto_id)
	VALUES(comentario_parm, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, id_alumno_parm, NULL, id_proyecto_parm)
	RETURNING id INTO resultado;
	RETURN resultado;
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error no se publico el anuncio';
END;
$$
LANGUAGE plpgsql;

--enlaces anuncio

Create or replace Function verEnlacesAnuncios(
	id_anuncio_parm int
) returns table(
	id INT8,
    titulo TEXT,
    path TEXT,
    fecha date,
    anuncio_id int8,
    dominio text
)
as
$$
BEGIN
	RETURN QUERY
	select enlaces.id, enlaces.titulo, enlaces.path, enlaces.fecha, enlaces.id_anuncio_id, substring(enlaces.path from 'https?://([^/]+)') as dominio, substring(columna, 33, 11) AS id_video 
	from public.plataforma_anuncios_enlaces as enlaces
	where enlaces.id_anuncio_id = id_anuncio_parm;
END;
$$
LANGUAGE plpgsql;

--listar materiales
Create or replace Function listaMateriales(
	id_fase_parm int
) returns table(
	id INT8,
    tema varchar,
    fecha date
)
as
$$
BEGIN
	RETURN QUERY
	select materiales.id, materiales.tema, materiales.fecha
	from public.plataforma_materiales as materiales
	where materiales.id_fase = id_fase_parm;
END;
$$
LANGUAGE plpgsql;

-- INSERTAR ENLACES
CREATE OR REPLACE function EnlacesMaterial(
    titulo_param TEXT,
    path_param TEXT,
    id_anuncio_param INT8
) RETURNS VARCHAR 
AS 
$$
BEGIN
    INSERT INTO public.plataforma_materiales_enlaces (titulo, path, fecha, id_anuncio_id)
    VALUES (titulo_param, path_param, CURRENT_DATE, id_anuncio_param);
    RETURN 'Agregado exitosamente';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error: no se agregaron los enlaces';
END;
$$
LANGUAGE plpgsql;

--Guardar un archivo (no esta en uso)
Create or replace Function GuardarArchivo(
	path_parm varchar,
	id_anuncio_parm int	
) returns varchar
as
$$
BEGIN
	INSERT INTO public.plataforma_anuncios_archivos
	("path", fecha, id_anuncio_id)
	VALUES(path_parm, CURRENT_DATE, id_anuncio_parm );
	RETURN 'Agregado exitosamente';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error no se agrego el archivo';
END;
$$
LANGUAGE plpgsql;

--ver los rachivos de los anuncios
CREATE OR REPLACE FUNCTION verArchivosAnuncio(anuncio_id INT)
RETURNS TABLE (
    id INT8,
    titulo text,
    path varchar,
    fecha date,
    id_anuncio int8,
   	extencion text
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
    archivo.id, 
    substring(archivo."path" from '/([^/]+)$') AS titulo, 
    archivo."path", 
    archivo.fecha, 
    archivo.id_anuncio_id,
    LOWER(substring(archivo."path" from '\.([^\.]+)$')) AS extension
	FROM 
    public.plataforma_anuncios_archivos AS archivo
	where archivo.id_anuncio_id = anuncio_id;
END;
$$ LANGUAGE plpgsql;

--eliminar un anuncio por id
Create or replace Function EliminarAnuncio(
	id_parm int
) returns varchar
as
$$
BEGIN
--eliminar comentarios
	DELETE FROM public.plataforma_anuncios_comentarios as comentarios
	WHERE comentarios.id_anuncio_id = id_parm;
-- eliminar enlaces
	DELETE FROM public.plataforma_anuncios_enlaces as enlaces
	WHERE enlaces.id_anuncio_id = id_parm;
--eliminar archivos
	DELETE FROM public.plataforma_anuncios_archivos as archivos
	WHERE archivos.id_anuncio_id = id_parm;
--eliminar anuncio
	delete from public.plataforma_anuncios as anuncio
	where anuncio.id = id_parm;
	RETURN 'Eliminado exitosamente';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error no se elimino el post';
END;
$$
LANGUAGE plpgsql;

-- ver los enlaces de los materiales
Create or replace Function enlacesMateriales(
	id_material_parm int
) returns table(
	id INT8,
    titulo text,
    path_ text,
    fecha date,
    id_anuncio int8
)
as
$$
BEGIN
	RETURN QUERY
	select * from public.plataforma_materiales_enlaces as enlaces
	where enlaces.id_anuncio_id  = id_material_parm;
END;
$$
LANGUAGE plpgsql;

--obtener lista de actividades por fase
CREATE OR REPLACE FUNCTION obtener_actividades_por_fase(fase_id INTEGER)
RETURNS TABLE(
    id INT8,
    titulo VARCHAR,
    descripcion TEXT,
    fecha DATE,
    id_fase INT8,
    id_profesor INT4
) AS $$
BEGIN
    RETURN QUERY
    SELECT act.id, act.titulo, act.descripcion, act.fecha, act.id_fase, act.id_profesor
    FROM public.plataforma_actividades as act
    WHERE act.id_fase = fase_id;
END;
$$ LANGUAGE plpgsql;


--eliminar un alumno del proyecto por id
Create or replace Function EliminarAlumnoDelProyecto(
	id_parm int,
	id_proyecto_parm int
) returns varchar
as
$$
BEGIN
	DELETE FROM public.plataforma_alumnos_proyecto as alumno
	WHERE alumno.id_alumno_id = id_parm and alumno.id_proyecto_id = id_proyecto_parm;
	RETURN 'Eliminado exitosamente';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error no se puedo expulsar al alumno';
END;
$$
LANGUAGE plpgsql;


--eliminar un profesor del proyecto por id
Create or replace Function EliminarProfesorDelProyecto(
	id_parm int,
	id_proyecto_parm int
) returns varchar
as
$$
BEGIN
	DELETE FROM public.plataforma_profesores_proyecto as profesor
	WHERE profesor.id_profesor_id = id_parm and profesor.id_proyecto_id = id_proyecto_parm;
	RETURN 'Eliminado exitosamente';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error no se puedo expulsar al alumno';
END;
$$
LANGUAGE plpgsql;


-- validar correos

Create or replace Function obteneroCorreoUsuario(
	correo_parm varchar
) returns table(
	correo varchar,
    usuario varchar
)
as
$$
BEGIN
	RETURN QUERY
	select usuario.correo_institucional, usuario.nombre_usuario 
	from plataforma_usuario as usuario
	where usuario.correo_institucional = correo_parm;
END;
$$
LANGUAGE plpgsql;

--Nombtrar nuevo admin proyecto
Create or replace Function superAdminDelProyecto(
	id_profesor_parm int,
	id_proyecto_parm int
) returns varchar
as
$$
BEGIN
UPDATE public.plataforma_proyectos
SET id_profesor_id=id_profesor_parm
WHERE id=id_proyecto_parm;
	RETURN 'Actulizado exitosamente';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error no se puedo cambiar el administrador del proyecto';
END;
$$
LANGUAGE plpgsql;



--editar anuncio
Create or replace Function EditarAnuncio(
	id_parm int,
	comentario_parm text 
) returns varchar
as
$$
BEGIN
	UPDATE public.plataforma_anuncios
	SET comentario=comentario_parm, fecha_edit= CURRENT_TIMESTAMP
	WHERE id=id_parm;
RETURN 'Editado exitosamente';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error no se edito el post';
END;
$$
LANGUAGE plpgsql;


--buscar el id Alumno por Post Id
Create or replace function buscarAlumnoPostbyId(
	id_anuncio_parm int
) returns table(
	id INT8
)
as
$$
BEGIN
	RETURN QUERY
	select post.id_alumno_id from public.plataforma_anuncios as post
	where post.id = id_anuncio_parm;
END;
$$
LANGUAGE plpgsql;

--buscar el id Profesor por Post Id
Create or replace function buscarProfesorPostbyId(
	id_anuncio_parm int
) returns table(
	id INT8
)
as
$$
BEGIN
	RETURN QUERY
	select post.id_profesor_id from public.plataforma_anuncios as post
	where post.id = id_anuncio_parm;
END;
$$
LANGUAGE plpgsql;








--editar comentario
Create or replace Function EditarComentario(
	id_parm int,
	comentario_parm text 
) returns varchar
as
$$
BEGIN
	UPDATE public.plataforma_anuncios_comentarios
	SET comentario=comentario_parm, fecha_edit=CURRENT_TIMESTAMP
	WHERE id=id_parm;
	RETURN 'Editado exitosamente';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error no se edito el comentario';
END;
$$
LANGUAGE plpgsql;

select BuscarProyectoByCodigo('-533001937');


drop function obtener_actividades_por_fase(int);
select obtener_actividades_por_fase(1);



select obtener_material_por_id (30);

select insertarMaterial ('BASE DE DATOS 2','hola,esta es una prueba', '2024-07-17', 1,1);

select obtener_anuncios(2);
select obtener_comentarios(4);




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

select * from public.plataforma_anuncios_archivos;



SELECT id, 
       substring(path from 'https?://([^/]+)') as dominio, 
       fecha
FROM public.plataforma_anuncios_enlaces;


drop function verEnlacesAnuncios(int);



drop function verEnlacesAnuncios(int);
select verEnlacesAnuncios(119);


select comentariospublicados.id, comentariospublicados.comentario, comentariospublicados.fecha, comentariospublicados.fecha_edit, profesor.nombre, profesor.apellidos, comentariospublicados.id_alumno_id, profesor.id
	from public.plataforma_materiales_comentarios as comentariosPublicados
	inner join public.plataforma_profesor as profesor on comentariospublicados.id_profesor_id = profesor.id
	
	union all
	select comentariospublicados.id, comentariospublicados.comentario, comentariospublicados.fecha, comentariospublicados.fecha_edit, alumno.nombre, alumno.apellidos, alumno.id, comentariospublicados.id_profesor_id 
	from public.plataforma_materiales_comentarios as comentariosPublicados
	inner join public.plataforma_alumno as alumno on comentariospublicados.id_alumno_id = alumno.id
	
	ORDER BY fecha_edit asc ; 




delete from public.plataforma_anuncios_enlaces;
delete from public.plataforma_materiales_enlaces;
delete from public.plataforma_materiales_comentarios;
delete from public.plataforma_materiales;
delete from public.plataforma_anuncios_archivos;
delete from public.plataforma_anuncios_comentarios;
delete from public.plataforma_anuncios;



delete from public.plataforma_alumnos_proyecto;
delete from public.plataforma_profesores_proyecto;
delete from public.plataforma_fases;
delete from public.plataforma_proyectos;


delete from public.plataforma_alumno;

delete from public.plataforma_profesor;
delete from public.plataforma_usuario;



--enlaces actividad

Create or replace Function verEnlacesActividades(
	id_actividad_parm int
) returns table(
	id INT8,
    titulo TEXT,
    path TEXT,
    fecha date,
    anuncio_id int8,
    dominio text
)
as
$$
BEGIN
	RETURN QUERY
	select enlaces.id, enlaces.titulo, enlaces.path, enlaces.fecha, enlaces.id_anuncio_id, substring(enlaces.path from 'https?://([^/]+)') as dominio 
	from public.plataforma_actividades_enlaces as enlaces
	where enlaces.id_anuncio_id = id_actividad_parm;
END;
$$
LANGUAGE plpgsql;














--Comentarios priv

--comentar Material priv Profesor
Create or replace Function ComentarMaterialPrivProfesor(
	comentario_parm text,
	id_profesor_parm int,
	id_Material_parm int,
	id_alumno_parm int
) returns varchar
as
$$
BEGIN
	INSERT INTO public.plataforma_materiales_comentarios_priv
	( comentario, fecha, fecha_edit, id_alumno_id, id_material_id, id_profesor_id)
	VALUES(comentario_parm, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, id_alumno_parm, id_Material_parm, id_profesor_parm);
	RETURN 'Agregado exitosamente';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error no se comento el material';
END;
$$
LANGUAGE plpgsql;

--Comentario Anuncio Alumno
Create or replace Function ComentarMaterialPrivAlumno(
	comentario_parm text,
	id_alumno_parm int,
	id_material_parm int
) returns varchar
as
$$
BEGIN
	INSERT INTO public.plataforma_materiales_comentarios_priv
	( comentario, fecha, fecha_edit, id_alumno_id, id_material_id, id_profesor_id)
	VALUES(comentario_parm, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, id_alumno_parm, id_Material_parm, NULL);
	RETURN 'Agregado exitosamente';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error no se comento el anuncio';
END;
$$
LANGUAGE plpgsql;

-- ver comentarios de un material
CREATE OR REPLACE FUNCTION obtener_comentarios_material_profesor(id_material_parm BIGINT)
RETURNS TABLE (
    id INT8,
    comentario TEXT,
    fecha timestamptz,
    fecha_edit timestamptz,
    nombre varchar,
    apellidos varchar,
    id_material_id int8,
    id_alumno_id INT8,
    id_profesor_id INT8
) AS $$
BEGIN
    RETURN QUERY 
    SELECT comentario.id, comentario.comentario, comentario.fecha, comentario.fecha_edit, comentarioalumno.nombre, comentarioalumno.apellidos, comentario.id_material_id, comentario.id_alumno_id , comentario.id_profesor_id 
    FROM plataforma_materiales_comentarios_priv AS comentario
    INNER JOIN public.plataforma_alumno AS comentarioalumno ON comentario.id_alumno_id = comentarioalumno.id
    WHERE comentario.id_material_id = id_material_parm and comentario.id_profesor_id is NULL
    UNION ALL
    SELECT comentario.id, comentario.comentario, comentario.fecha, comentario.fecha_edit, comentarioprofesor.nombre, comentarioprofesor.apellidos, comentario.id_material_id, comentario.id_alumno_id , comentario.id_profesor_id 
    FROM plataforma_materiales_comentarios_priv AS comentario
    INNER JOIN public.plataforma_profesor AS comentarioprofesor ON comentario.id_profesor_id = comentarioprofesor.id 
    WHERE comentario.id_material_id = id_material_parm
    ORDER BY fecha asc ;   -- Ordenar por fecha_edit ascendente
END;
$$ LANGUAGE plpgsql;

-- ver comentarios de un material alumno
CREATE OR REPLACE FUNCTION obtener_comentarios_material_alumno(id_material_parm BIGINT, id_alumno_parm int)
RETURNS TABLE (
    id INT8,
    comentario TEXT,
    fecha timestamptz,
    fecha_edit timestamptz,
    nombre varchar,
    apellidos varchar,
    id_material_id int8,
    id_alumno_id INT8,
    id_profesor_id INT8
) AS $$
BEGIN
    RETURN QUERY 
    SELECT comentario.id, comentario.comentario, comentario.fecha, comentario.fecha_edit, comentarioalumno.nombre, comentarioalumno.apellidos, comentario.id_material_id, comentario.id_alumno_id , comentario.id_profesor_id 
    FROM plataforma_materiales_comentarios_priv AS comentario
    INNER JOIN public.plataforma_alumno AS comentarioalumno ON comentario.id_alumno_id = comentarioalumno.id
    WHERE comentario.id_material_id = id_material_parm and comentario.id_alumno_id = id_alumno_parm  and comentario.id_profesor_id is null
    UNION ALL
    SELECT comentario.id, comentario.comentario, comentario.fecha, comentario.fecha_edit, comentarioprofesor.nombre, comentarioprofesor.apellidos, comentario.id_material_id, comentario.id_alumno_id , comentario.id_profesor_id 
    FROM plataforma_materiales_comentarios_priv AS comentario
    INNER JOIN public.plataforma_profesor AS comentarioprofesor ON comentario.id_profesor_id = comentarioprofesor.id 
    WHERE comentario.id_material_id = id_material_parm and comentario.id_alumno_id = id_alumno_parm 
    ORDER BY fecha asc ;   -- Ordenar por fecha_edit ascendente
END;
$$ LANGUAGE plpgsql;




--FUNCION PUBLICAR UN COMENTARIO EN ACTIVIDADES
--comentar Anuncio Profesor
Create or replace Function Actividad_Comentario(
	comentario_parm text,
	id_profesor_parm int,
	id_anuncio_parm int
) returns varchar
as
$$
BEGIN
	INSERT INTO public.plataforma_actividades_comentarios
	(comentario, fecha, fecha_edit, id_alumno_id, id_profesor_id, id_actividad_id)
	VALUES(comentario_parm, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, id_profesor_parm, id_anuncio_parm);
	RETURN 'Agregado exitosamente';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error no se comento el anuncio';
END;
$$
LANGUAGE plpgsql;


SELECT Actividad_Comentario('Este es un comentario de actividad',4,48);

----------------------------------------------------------------------
--Comentario Materiales Alumno
Create or replace Function Actividad_Comentario_Alumno(
	comentario_parm text,
	id_alumno_parm int,
	id_anuncio_parm int
) returns varchar
as
$$
BEGIN
	INSERT INTO public.plataforma_actividades_comentarios
	(comentario, fecha, fecha_edit, id_alumno_id, id_profesor_id, id_material_id)
	VALUES(comentario_parm, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, id_alumno_parm, NULL, id_anuncio_parm);
	RETURN 'Agregado exitosamente';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error no se comento el anuncio'|| SQLERRM;
END;
$$
LANGUAGE plpgsql;

SELECT Actividad_Comentario_Alumno('Este es un comentario de actividad de alumno',2,49);
------------------------------------------------------------------------------------------------------


CREATE OR REPLACE FUNCTION obtener_comentarios_actividades(id_anuncio_parm BIGINT)
RETURNS TABLE (
    id INT8,
    comentario TEXT,
    fecha timestamptz,
    fecha_edit timestamptz,
    nombre varchar,
    apellidos varchar,
    id_alumno_id INT8,
    id_profesor_id INT8
) AS $$
BEGIN
    RETURN QUERY 
    select comentariospublicados.id, comentariospublicados.comentario, comentariospublicados.fecha, comentariospublicados.fecha_edit, profesor.nombre, profesor.apellidos,comentariospublicados.id_alumno_id, profesor.id
	from public.plataforma_actividades_comentarios as comentariosPublicados
	inner join public.plataforma_profesor as profesor on comentariospublicados.id_profesor_id = profesor.id
	where comentariospublicados.id_material_id = id_anuncio_parm
	union all
	select comentariospublicados.id, comentariospublicados.comentario, comentariospublicados.fecha, comentariospublicados.fecha_edit, alumno.nombre, alumno.apellidos, alumno.id, comentariospublicados.id_profesor_id
	from public.plataforma_actividades_comentarios as comentariosPublicados
	inner join public.plataforma_alumno as alumno on comentariospublicados.id_alumno_id = alumno.id
	where comentariospublicados.id_material_id = id_anuncio_parm
	ORDER BY fecha_edit desc ;
END;
$$ LANGUAGE plpgsql;


















CREATE OR REPLACE FUNCTION obtener_comentarios_actividades(id_anuncio_parm BIGINT)
RETURNS TABLE (
    id INT8,
    comentario TEXT,
    fecha timestamptz,
    fecha_edit timestamptz,
    nombre varchar,
    apellidos varchar,
    id_alumno_id INT8,
    id_profesor_id INT8
) AS $$
BEGIN
    RETURN QUERY 
    select comentariospublicados.id, comentariospublicados.comentario, comentariospublicados.fecha, comentariospublicados.fecha_edit, profesor.nombre, profesor.apellidos,comentariospublicados.id_alumno_id, profesor.id
	from public.plataforma_actividades_comentarios as comentariosPublicados
	inner join public.plataforma_profesor as profesor on comentariospublicados.id_profesor_id = profesor.id
	where comentariospublicados.id_actividad_id = id_anuncio_parm
	union all
	select comentariospublicados.id, comentariospublicados.comentario, comentariospublicados.fecha, comentariospublicados.fecha_edit, alumno.nombre, alumno.apellidos, alumno.id, comentariospublicados.id_profesor_id
	from public.plataforma_actividades_comentarios as comentariosPublicados
	inner join public.plataforma_alumno as alumno on comentariospublicados.id_alumno_id = alumno.id
	where comentariospublicados.id_actividad_id = id_anuncio_parm
	ORDER BY fecha_edit desc ;
END;
$$ LANGUAGE plpgsql;

-------------------------------------------------------------------------------------------------
-- Calificacar tarea
------------------------------------------------------------------------------------------------
-- Entregar actividad
Create or replace Function entregarActividad(
	id_alumno_parm int,
	id_actividad_parm int
) returns varchar
as
$$
BEGIN
UPDATE public.plataforma_asignar_actividad
	SET entregada=true
	WHERE id_alumno_id= id_alumno_parm and id_actividad_id= id_actividad_parm;
	RETURN 'Entregada con exito';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error no se entrego';
END;
$$
LANGUAGE plpgsql;

-- Anular entrega
Create or replace Function anularEntrega(
	id_alumno_parm int,
	id_actividad_parm int
) returns varchar
as
$$
BEGIN
UPDATE public.plataforma_asignar_actividad
	SET entregada=false
	WHERE id_alumno_id= id_alumno_parm and id_actividad_id= id_actividad_parm;
	RETURN 'Anulada con exito';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error no se anulo';
END;
$$
LANGUAGE plpgsql;

--asignar actividad
Create or replace Function asignarActividad(
	id_alumno_parm int,
	id_actividad_parm int
) returns varchar
as
$$
BEGIN
	INSERT INTO public.plataforma_asignar_actividad
	(calificacion, entregada, id_actividad_id, id_alumno_id)
	VALUES(null, false, id_actividad_parm, id_alumno_parm);
	RETURN 'Asignada con exito';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error no se asigno';
END;
$$
LANGUAGE plpgsql;







--actividades de un alumno espesifico

CREATE OR REPLACE FUNCTION public.obtener_actividades_por_alumno(fase_id integer, id_alumno_parm int)
 RETURNS TABLE(id bigint, titulo character varying, descripcion text, fecha date, id_fase bigint, id_profesor integer)
 LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN QUERY
    select act.id, act.titulo, act.descripcion, act.fecha, act.id_fase, act.id_profesor from public.plataforma_asignar_actividad as asig
	inner join public.plataforma_actividades as act
	on asig.id_actividad_id = act.id 
	where act.id_fase =fase_id and asig.id_alumno_id = id_alumno_parm;
END;
$function$
;

--nombres actividades

select act.id, act.titulo, act.descripcion, act.fecha , act.id_fase, act.id_profesor from public.plataforma_asignar_actividad as asig
inner join public.plataforma_actividades as act
on asig.id_actividad_id = act.id 
where act.id_fase =26 and asig.id_alumno_id = 6;




select a.nombre, a.apellidos from plataforma_alumno as a
where a.id = 2;


CREATE OR REPLACE FUNCTION public.obtener_actividades_by_alumno(id_alumno_parm int)
 RETURNS TABLE(
 id bigint, 
 calificacion boolean, 
 entregada boolean, 
 id_actividad bigint, 
 id_alumno int8,
 titulo varchar,
 id_fase int8
 )
 LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN QUERY
	select paa.id, paa.calificacion, paa.entregada, paa.id_actividad_id, paa.id_alumno_id, pa.titulo, pa.id_fase from public.plataforma_asignar_actividad as paa
	inner join plataforma_actividades as pa 
	on paa.id_actividad_id = pa.id 
	where paa.id_alumno_id = id_alumno_parm;
END;
$function$
;
 drop function obtener_actividades_by_alumno(int);
select obtener_actividades_by_alumno(2);





select obtener_entregas_by_alumno (6)
CREATE OR REPLACE FUNCTION public.obtener_entregas_by_alumno(id_alumno_parm int)
 RETURNS TABLE(
 id bigint, 
 path varchar, 
 fecha date, 
 id_actividad bigint, 
 id_alumno int8
 )
 LANGUAGE plpgsql
AS $function$
BEGIN
	RETURN QUERY
	select * from public.plataforma_entregas_actividades as pea
	where pea.id_alumno_id = id_alumno_parm;
END;
$function$
;

Create or replace Function calificarActividad(
	id_parm int
) returns varchar
as
$$
BEGIN
	UPDATE public.plataforma_asignar_actividad
	SET calificacion=true
	WHERE id=id_parm;
	RETURN 'Calificada con exito';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error no se califico';
END;
$$
LANGUAGE plpgsql;


Create or replace Function descalificarActividad(
	id_parm int
) returns varchar
as
$$
BEGIN
	UPDATE public.plataforma_asignar_actividad
	SET calificacion=false
	WHERE id=id_parm;
	RETURN 'Anulada con exito';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error no se anulo la calificacion';
END;
$$
LANGUAGE plpgsql;


select descalificarActividad(1)