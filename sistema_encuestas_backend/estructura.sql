--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: estadoasignacion; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.estadoasignacion AS ENUM (
    'ASIGNADA',
    'EN_PROGRESO',
    'COMPLETADA',
    'PAUSADA',
    'CANCELADA'
);


ALTER TYPE public.estadoasignacion OWNER TO postgres;

--
-- Name: estadocanje; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.estadocanje AS ENUM (
    'SOLICITADO',
    'APROBADO',
    'ENTREGADO',
    'RECHAZADO',
    'CANCELADO'
);


ALTER TYPE public.estadocanje OWNER TO postgres;

--
-- Name: estadoencuesta; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.estadoencuesta AS ENUM (
    'BORRADOR',
    'PROGRAMADA',
    'ACTIVA',
    'FINALIZADA',
    'SUSPENDIDA'
);


ALTER TYPE public.estadoencuesta OWNER TO postgres;

--
-- Name: estadoparticipacion; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.estadoparticipacion AS ENUM (
    'INICIADA',
    'EN_PROGRESO',
    'COMPLETADA',
    'ABANDONADA',
    'PENDIENTE_REVISION'
);


ALTER TYPE public.estadoparticipacion OWNER TO postgres;

--
-- Name: estadopremio; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.estadopremio AS ENUM (
    'DISPONIBLE',
    'AGOTADO',
    'SUSPENDIDO',
    'DESCONTINUADO'
);


ALTER TYPE public.estadopremio OWNER TO postgres;

--
-- Name: estadousuario; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.estadousuario AS ENUM (
    'PENDIENTE',
    'APROBADO',
    'RECHAZADO',
    'SUSPENDIDO'
);


ALTER TYPE public.estadousuario OWNER TO postgres;

--
-- Name: metodoregistro; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.metodoregistro AS ENUM (
    'MANUAL',
    'GOOGLE'
);


ALTER TYPE public.metodoregistro OWNER TO postgres;

--
-- Name: tipoparticipacion; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.tipoparticipacion AS ENUM (
    'DIRECTA',
    'ENCUESTADOR'
);


ALTER TYPE public.tipoparticipacion OWNER TO postgres;

--
-- Name: tipopremio; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.tipopremio AS ENUM (
    'FISICO',
    'DIGITAL',
    'DESCUENTO',
    'SERVICIO'
);


ALTER TYPE public.tipopremio OWNER TO postgres;

--
-- Name: tiporespuesta; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.tiporespuesta AS ENUM (
    'TEXTO_SIMPLE',
    'TEXTO_LARGO',
    'OPCION_MULTIPLE',
    'SELECCION_MULTIPLE',
    'ESCALA_NUMERICA',
    'FECHA',
    'ARCHIVO'
);


ALTER TYPE public.tiporespuesta OWNER TO postgres;

--
-- Name: tipovisibilidad; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.tipovisibilidad AS ENUM (
    'USUARIOS_GENERALES',
    'ENCUESTADORES',
    'AMBOS',
    'PERSONALIZADA'
);


ALTER TYPE public.tipovisibilidad OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: asignaciones_encuestador; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.asignaciones_encuestador (
    id_asignacion integer NOT NULL,
    id_encuestador integer NOT NULL,
    id_encuesta integer NOT NULL,
    id_admin_asignador integer NOT NULL,
    estado public.estadoasignacion,
    fecha_asignacion timestamp without time zone,
    fecha_inicio timestamp without time zone,
    fecha_finalizacion timestamp without time zone,
    meta_respuestas integer,
    respuestas_obtenidas integer,
    activa boolean,
    observaciones_asignacion text,
    observaciones_encuestador text
);


ALTER TABLE public.asignaciones_encuestador OWNER TO postgres;

--
-- Name: asignaciones_encuestador_id_asignacion_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.asignaciones_encuestador_id_asignacion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.asignaciones_encuestador_id_asignacion_seq OWNER TO postgres;

--
-- Name: asignaciones_encuestador_id_asignacion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.asignaciones_encuestador_id_asignacion_seq OWNED BY public.asignaciones_encuestador.id_asignacion;


--
-- Name: canjes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.canjes (
    id_canje integer NOT NULL,
    id_usuario integer NOT NULL,
    id_premio integer NOT NULL,
    puntos_utilizados integer NOT NULL,
    estado public.estadocanje,
    fecha_solicitud timestamp without time zone,
    fecha_aprobacion timestamp without time zone,
    fecha_entrega timestamp without time zone,
    direccion_entrega text,
    telefono_contacto text,
    observaciones_usuario text,
    observaciones_admin text,
    id_admin_aprobador integer,
    codigo_seguimiento text,
    requiere_recogida boolean
);


ALTER TABLE public.canjes OWNER TO postgres;

--
-- Name: canjes_id_canje_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.canjes_id_canje_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.canjes_id_canje_seq OWNER TO postgres;

--
-- Name: canjes_id_canje_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.canjes_id_canje_seq OWNED BY public.canjes.id_canje;


--
-- Name: encuestas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.encuestas (
    id_encuesta integer NOT NULL,
    titulo character varying(255) NOT NULL,
    descripcion text,
    fecha_inicio date,
    fecha_fin date,
    puntos_otorga integer DEFAULT 0,
    tiempo_estimado character varying(50),
    visible_para character varying(20) DEFAULT 'usuarios'::character varying,
    imagen text,
    estado boolean DEFAULT true NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    id_usuario_creador integer NOT NULL
);


ALTER TABLE public.encuestas OWNER TO postgres;

--
-- Name: encuestas_id_encuesta_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.encuestas_id_encuesta_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.encuestas_id_encuesta_seq OWNER TO postgres;

--
-- Name: encuestas_id_encuesta_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.encuestas_id_encuesta_seq OWNED BY public.encuestas.id_encuesta;


--
-- Name: opciones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.opciones (
    id_opcion integer NOT NULL,
    id_pregunta integer NOT NULL,
    texto_opcion text NOT NULL
);


ALTER TABLE public.opciones OWNER TO postgres;

--
-- Name: opciones_id_opcion_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.opciones_id_opcion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.opciones_id_opcion_seq OWNER TO postgres;

--
-- Name: opciones_id_opcion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.opciones_id_opcion_seq OWNED BY public.opciones.id_opcion;


--
-- Name: participaciones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.participaciones (
    id_participacion integer NOT NULL,
    id_usuario integer NOT NULL,
    id_encuesta integer NOT NULL,
    fecha_participacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    puntaje_obtenido integer DEFAULT 0,
    tiempo_respuesta_segundos integer DEFAULT 0
);


ALTER TABLE public.participaciones OWNER TO postgres;

--
-- Name: participaciones_id_participacion_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.participaciones_id_participacion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.participaciones_id_participacion_seq OWNER TO postgres;

--
-- Name: participaciones_id_participacion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.participaciones_id_participacion_seq OWNED BY public.participaciones.id_participacion;


--
-- Name: preguntas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.preguntas (
    id_pregunta integer NOT NULL,
    id_encuesta integer NOT NULL,
    tipo character varying(20) NOT NULL,
    texto text NOT NULL,
    orden integer
);


ALTER TABLE public.preguntas OWNER TO postgres;

--
-- Name: preguntas_id_pregunta_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.preguntas_id_pregunta_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.preguntas_id_pregunta_seq OWNER TO postgres;

--
-- Name: preguntas_id_pregunta_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.preguntas_id_pregunta_seq OWNED BY public.preguntas.id_pregunta;


--
-- Name: premios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.premios (
    id_premio integer NOT NULL,
    nombre character varying(255) NOT NULL,
    descripcion text,
    imagen_url text,
    costo_puntos integer NOT NULL,
    stock_disponible integer,
    stock_original integer,
    tipo public.tipopremio NOT NULL,
    categoria character varying(100),
    estado public.estadopremio,
    activo boolean,
    fecha_creacion timestamp without time zone,
    fecha_actualizacion timestamp without time zone,
    requiere_aprobacion boolean,
    instrucciones_canje text,
    terminos_condiciones text
);


ALTER TABLE public.premios OWNER TO postgres;

--
-- Name: premios_id_premio_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.premios_id_premio_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.premios_id_premio_seq OWNER TO postgres;

--
-- Name: premios_id_premio_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.premios_id_premio_seq OWNED BY public.premios.id_premio;


--
-- Name: respuestas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.respuestas (
    id_respuesta integer NOT NULL,
    id_pregunta integer NOT NULL,
    id_usuario integer NOT NULL,
    id_opcion integer,
    respuesta_texto text,
    fecha_respuesta timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.respuestas OWNER TO postgres;

--
-- Name: respuestas_id_respuesta_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.respuestas_id_respuesta_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.respuestas_id_respuesta_seq OWNER TO postgres;

--
-- Name: respuestas_id_respuesta_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.respuestas_id_respuesta_seq OWNED BY public.respuestas.id_respuesta;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    id_rol integer NOT NULL,
    nombre_rol character varying(50) NOT NULL
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- Name: roles_id_rol_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.roles_id_rol_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.roles_id_rol_seq OWNER TO postgres;

--
-- Name: roles_id_rol_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.roles_id_rol_seq OWNED BY public.roles.id_rol;


--
-- Name: sesiones_usuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sesiones_usuario (
    id_sesion integer NOT NULL,
    id_usuario integer NOT NULL,
    token_hash character varying(255) NOT NULL,
    ip_address character varying(45),
    user_agent text,
    fecha_inicio timestamp without time zone,
    fecha_ultimo_acceso timestamp without time zone,
    fecha_expiracion timestamp without time zone NOT NULL,
    activa boolean,
    dispositivo character varying(255),
    ubicacion character varying(255)
);


ALTER TABLE public.sesiones_usuario OWNER TO postgres;

--
-- Name: sesiones_usuario_id_sesion_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sesiones_usuario_id_sesion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sesiones_usuario_id_sesion_seq OWNER TO postgres;

--
-- Name: sesiones_usuario_id_sesion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sesiones_usuario_id_sesion_seq OWNED BY public.sesiones_usuario.id_sesion;


--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    id_usuario integer NOT NULL,
    nombre character varying(100) NOT NULL,
    apellido character varying(100) NOT NULL,
    documento_numero character varying(20) NOT NULL,
    celular_numero character varying(20),
    email character varying(150) NOT NULL,
    metodo_registro character varying(20) NOT NULL,
    password_hash text,
    estado boolean DEFAULT true NOT NULL,
    rol_id integer NOT NULL,
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT usuarios_metodo_registro_check CHECK (((metodo_registro)::text = ANY ((ARRAY['local'::character varying, 'google'::character varying])::text[])))
);


ALTER TABLE public.usuarios OWNER TO postgres;

--
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuarios_id_usuario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuarios_id_usuario_seq OWNER TO postgres;

--
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarios_id_usuario_seq OWNED BY public.usuarios.id_usuario;


--
-- Name: asignaciones_encuestador id_asignacion; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asignaciones_encuestador ALTER COLUMN id_asignacion SET DEFAULT nextval('public.asignaciones_encuestador_id_asignacion_seq'::regclass);


--
-- Name: canjes id_canje; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.canjes ALTER COLUMN id_canje SET DEFAULT nextval('public.canjes_id_canje_seq'::regclass);


--
-- Name: encuestas id_encuesta; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.encuestas ALTER COLUMN id_encuesta SET DEFAULT nextval('public.encuestas_id_encuesta_seq'::regclass);


--
-- Name: opciones id_opcion; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opciones ALTER COLUMN id_opcion SET DEFAULT nextval('public.opciones_id_opcion_seq'::regclass);


--
-- Name: participaciones id_participacion; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participaciones ALTER COLUMN id_participacion SET DEFAULT nextval('public.participaciones_id_participacion_seq'::regclass);


--
-- Name: preguntas id_pregunta; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.preguntas ALTER COLUMN id_pregunta SET DEFAULT nextval('public.preguntas_id_pregunta_seq'::regclass);


--
-- Name: premios id_premio; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.premios ALTER COLUMN id_premio SET DEFAULT nextval('public.premios_id_premio_seq'::regclass);


--
-- Name: respuestas id_respuesta; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.respuestas ALTER COLUMN id_respuesta SET DEFAULT nextval('public.respuestas_id_respuesta_seq'::regclass);


--
-- Name: roles id_rol; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles ALTER COLUMN id_rol SET DEFAULT nextval('public.roles_id_rol_seq'::regclass);


--
-- Name: sesiones_usuario id_sesion; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sesiones_usuario ALTER COLUMN id_sesion SET DEFAULT nextval('public.sesiones_usuario_id_sesion_seq'::regclass);


--
-- Name: usuarios id_usuario; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id_usuario SET DEFAULT nextval('public.usuarios_id_usuario_seq'::regclass);


--
-- Name: asignaciones_encuestador asignaciones_encuestador_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asignaciones_encuestador
    ADD CONSTRAINT asignaciones_encuestador_pkey PRIMARY KEY (id_asignacion);


--
-- Name: canjes canjes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.canjes
    ADD CONSTRAINT canjes_pkey PRIMARY KEY (id_canje);


--
-- Name: encuestas encuestas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.encuestas
    ADD CONSTRAINT encuestas_pkey PRIMARY KEY (id_encuesta);


--
-- Name: opciones opciones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opciones
    ADD CONSTRAINT opciones_pkey PRIMARY KEY (id_opcion);


--
-- Name: participaciones participaciones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participaciones
    ADD CONSTRAINT participaciones_pkey PRIMARY KEY (id_participacion);


--
-- Name: preguntas preguntas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.preguntas
    ADD CONSTRAINT preguntas_pkey PRIMARY KEY (id_pregunta);


--
-- Name: premios premios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.premios
    ADD CONSTRAINT premios_pkey PRIMARY KEY (id_premio);


--
-- Name: respuestas respuestas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.respuestas
    ADD CONSTRAINT respuestas_pkey PRIMARY KEY (id_respuesta);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id_rol);


--
-- Name: sesiones_usuario sesiones_usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sesiones_usuario
    ADD CONSTRAINT sesiones_usuario_pkey PRIMARY KEY (id_sesion);


--
-- Name: sesiones_usuario sesiones_usuario_token_hash_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sesiones_usuario
    ADD CONSTRAINT sesiones_usuario_token_hash_key UNIQUE (token_hash);


--
-- Name: usuarios usuarios_documento_numero_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_documento_numero_key UNIQUE (documento_numero);


--
-- Name: usuarios usuarios_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_email_key UNIQUE (email);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id_usuario);


--
-- Name: ix_asignaciones_encuestador_id_asignacion; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_asignaciones_encuestador_id_asignacion ON public.asignaciones_encuestador USING btree (id_asignacion);


--
-- Name: ix_canjes_id_canje; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_canjes_id_canje ON public.canjes USING btree (id_canje);


--
-- Name: ix_premios_id_premio; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_premios_id_premio ON public.premios USING btree (id_premio);


--
-- Name: ix_sesiones_usuario_id_sesion; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_sesiones_usuario_id_sesion ON public.sesiones_usuario USING btree (id_sesion);


--
-- Name: asignaciones_encuestador asignaciones_encuestador_id_admin_asignador_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asignaciones_encuestador
    ADD CONSTRAINT asignaciones_encuestador_id_admin_asignador_fkey FOREIGN KEY (id_admin_asignador) REFERENCES public.usuarios(id_usuario);


--
-- Name: asignaciones_encuestador asignaciones_encuestador_id_encuesta_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asignaciones_encuestador
    ADD CONSTRAINT asignaciones_encuestador_id_encuesta_fkey FOREIGN KEY (id_encuesta) REFERENCES public.encuestas(id_encuesta);


--
-- Name: asignaciones_encuestador asignaciones_encuestador_id_encuestador_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asignaciones_encuestador
    ADD CONSTRAINT asignaciones_encuestador_id_encuestador_fkey FOREIGN KEY (id_encuestador) REFERENCES public.usuarios(id_usuario);


--
-- Name: canjes canjes_id_admin_aprobador_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.canjes
    ADD CONSTRAINT canjes_id_admin_aprobador_fkey FOREIGN KEY (id_admin_aprobador) REFERENCES public.usuarios(id_usuario);


--
-- Name: canjes canjes_id_premio_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.canjes
    ADD CONSTRAINT canjes_id_premio_fkey FOREIGN KEY (id_premio) REFERENCES public.premios(id_premio);


--
-- Name: canjes canjes_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.canjes
    ADD CONSTRAINT canjes_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario);


--
-- Name: preguntas fk_encuesta; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.preguntas
    ADD CONSTRAINT fk_encuesta FOREIGN KEY (id_encuesta) REFERENCES public.encuestas(id_encuesta) ON DELETE CASCADE;


--
-- Name: participaciones fk_encuesta_participacion; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participaciones
    ADD CONSTRAINT fk_encuesta_participacion FOREIGN KEY (id_encuesta) REFERENCES public.encuestas(id_encuesta) ON DELETE CASCADE;


--
-- Name: respuestas fk_opcion_respuesta; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.respuestas
    ADD CONSTRAINT fk_opcion_respuesta FOREIGN KEY (id_opcion) REFERENCES public.opciones(id_opcion) ON DELETE SET NULL;


--
-- Name: opciones fk_pregunta_opcion; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opciones
    ADD CONSTRAINT fk_pregunta_opcion FOREIGN KEY (id_pregunta) REFERENCES public.preguntas(id_pregunta) ON DELETE CASCADE;


--
-- Name: respuestas fk_pregunta_respuesta; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.respuestas
    ADD CONSTRAINT fk_pregunta_respuesta FOREIGN KEY (id_pregunta) REFERENCES public.preguntas(id_pregunta) ON DELETE CASCADE;


--
-- Name: usuarios fk_rol; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT fk_rol FOREIGN KEY (rol_id) REFERENCES public.roles(id_rol);


--
-- Name: encuestas fk_usuario_creador; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.encuestas
    ADD CONSTRAINT fk_usuario_creador FOREIGN KEY (id_usuario_creador) REFERENCES public.usuarios(id_usuario) ON DELETE CASCADE;


--
-- Name: participaciones fk_usuario_participacion; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participaciones
    ADD CONSTRAINT fk_usuario_participacion FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario) ON DELETE CASCADE;


--
-- Name: respuestas fk_usuario_respuesta; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.respuestas
    ADD CONSTRAINT fk_usuario_respuesta FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario) ON DELETE CASCADE;


--
-- Name: sesiones_usuario sesiones_usuario_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sesiones_usuario
    ADD CONSTRAINT sesiones_usuario_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario);


--
-- PostgreSQL database dump complete
--

