import api from './api';

// Tipos para las encuestas
export interface Encuesta {
  id_encuesta: number;
  titulo: string;
  descripcion?: string;
  fecha_inicio?: string;
  fecha_fin?: string;
  puntos_otorga: number;
  imagen?: string;
  tiempo_estimado?: string;
  estado: boolean;
  visible_para: string;
  preguntas?: Pregunta[];
}

export interface Pregunta {
  id_pregunta: number;
  texto: string;
  tipo: 'multiple' | 'abierta' | 'escala' | 'si_no';
  orden: number;
  opciones: Opcion[];
}

export interface Opcion {
  id_opcion: number;
  texto_opcion: string;
}

export interface CrearEncuestaData {
  titulo: string;
  descripcion?: string; // ← marcar como opcional si es válido
  fecha_inicio?: string;
  fecha_fin?: string;
  estado: boolean;
  visible_para: 'todos' | 'registrados' | 'premium';
  imagen_url?: string;
  puntos_otorga: number;
  tiempo_estimado?: string;
  preguntas: {
    texto_pregunta: string;
    tipo: 'multiple' | 'abierta' | 'escala' | 'si_no';
    orden: number;
    opciones: { texto_opcion: string }[];
  }[];
}

export interface RespuestaEncuesta {
  id_encuesta: number;
  respuestas: {
    id_pregunta: number;
    id_opcion?: number;
    texto_respuesta?: string;
  }[];
  tiempo_completado?: number;
}

export interface FiltrosEncuesta {
  skip?: number;
  limit?: number;
  orden?: string;
  direccion?: 'asc' | 'desc';
  filtro_visibilidad?: string;
}

// Servicio de encuestas
class EncuestasService {
  // Obtener encuestas activas con paginación y filtros
  async obtenerEncuestasActivas(
    filtros: FiltrosEncuesta = {}
  ): Promise<Encuesta[]> {
    try {
      const params = new URLSearchParams();

      if (filtros.skip !== undefined)
        params.append('skip', filtros.skip.toString());
      if (filtros.limit !== undefined)
        params.append('limit', filtros.limit.toString());
      if (filtros.orden) params.append('orden', filtros.orden);
      if (filtros.direccion) params.append('direccion', filtros.direccion);
      if (filtros.filtro_visibilidad)
        params.append('filtro_visibilidad', filtros.filtro_visibilidad);

      const response = await api.get(`/encuestas/activas?${params}`);
      return response.data;
    } catch (error) {
      console.error('Error al obtener encuestas activas:', error);
      throw error;
    }
  }

  // Obtener una encuesta completa por ID
  async obtenerEncuesta(id: number): Promise<Encuesta> {
    try {
      const response = await api.get(`/encuestas/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error al obtener encuesta ${id}:`, error);
      throw error;
    }
  }

  // Crear nueva encuesta (solo admin)
  async crearEncuesta(
    data: CrearEncuestaData
  ): Promise<{ mensaje: string; id_encuesta: number; titulo: string }> {
    try {
      const response = await api.post('/encuestas/', data);
      return response.data;
    } catch (error) {
      console.error('Error al crear encuesta:', error);
      throw error;
    }
  }

  // Actualizar encuesta (solo admin)
  async actualizarEncuesta(
    id: number,
    data: Partial<CrearEncuestaData>
  ): Promise<{ mensaje: string; id_encuesta: number }> {
    try {
      const response = await api.put(`/encuestas/${id}`, data);
      return response.data;
    } catch (error) {
      console.error(`Error al actualizar encuesta ${id}:`, error);
      throw error;
    }
  }

  // Eliminar encuesta (solo admin)
  async eliminarEncuesta(id: number): Promise<{ mensaje: string }> {
    try {
      const response = await api.delete(`/encuestas/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error al eliminar encuesta ${id}:`, error);
      throw error;
    }
  }

  // Enviar respuestas de encuesta
  async enviarRespuestas(
    data: RespuestaEncuesta
  ): Promise<{ mensaje: string; puntos_obtenidos?: number }> {
    try {
      const response = await api.post('/respuestas/', data);
      return response.data;
    } catch (error) {
      console.error('Error al enviar respuestas:', error);
      throw error;
    }
  }

  // Obtener estadísticas de encuestas (solo admin)
  async obtenerEstadisticas(): Promise<{
    total_encuestas: number;
    encuestas_activas: number;
    encuestas_inactivas: number;
    tasa_actividad: number;
  }> {
    try {
      const response = await api.get('/encuestas/admin/estadisticas');
      return response.data;
    } catch (error) {
      console.error('Error al obtener estadísticas:', error);
      throw error;
    }
  }

  // Verificar si el usuario ya respondió una encuesta
  async verificarParticipacion(idEncuesta: number): Promise<boolean> {
    try {
      const response = await api.get(
        `/participaciones/verificar/${idEncuesta}`
      );
      return response.data.ya_participo;
    } catch (error) {
      console.error('Error al verificar participación:', error);
      return false;
    }
  }

  // Obtener historial de participaciones del usuario
  async obtenerHistorialUsuario(): Promise<any[]> {
    try {
      const response = await api.get('/participaciones/historial');
      return response.data;
    } catch (error) {
      console.error('Error al obtener historial:', error);
      throw error;
    }
  }
}

// Instancia única del servicio
export const encuestasService = new EncuestasService();

// Hook personalizado para manejar encuestas
export const useEncuestas = () => {
  const obtenerEncuestas = async (filtros: FiltrosEncuesta = {}) => {
    return await encuestasService.obtenerEncuestasActivas(filtros);
  };

  const obtenerEncuesta = async (id: number) => {
    return await encuestasService.obtenerEncuesta(id);
  };

  const enviarRespuestas = async (data: RespuestaEncuesta) => {
    return await encuestasService.enviarRespuestas(data);
  };

  return {
    obtenerEncuestas,
    obtenerEncuesta,
    enviarRespuestas,
    verificarParticipacion:
      encuestasService.verificarParticipacion.bind(encuestasService),
    obtenerHistorial:
      encuestasService.obtenerHistorialUsuario.bind(encuestasService),
  };
};

// --- PREMIOS Y CANJES ---

export async function getPremios(token: string) {
  return api.get('/premios/', {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function canjearPremio(data: any, token: string) {
  return api.post('/premios/canje', data, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function getHistorialCanjes(token: string) {
  return api.get('/premios/canjes', {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function getMisDatos(token: string) {
  return api.get('/usuario/me', {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function actualizarMisDatos(data: any, token: string) {
  return api.put('/usuario/me', data, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function cambiarContrasena(
  data: {
    contrasena_actual: string;
    nueva_contrasena: string;
    confirmar_contrasena: string;
  },
  token: string
) {
  return api.post('/usuario/cambiar-contrasena', data, {
    headers: { Authorization: `Bearer ${token}` },
  });
}
