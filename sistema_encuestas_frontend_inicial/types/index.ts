// types/index.ts

export interface User {
  id_usuario: number;
  nombre: string;
  apellido: string;
  email: string;
  documento_numero: string;
  celular_numero?: string;
  estado: boolean;
  rol_id: number;
  fecha_registro?: string;
  metodo_registro: string;
  puntos_totales: number;
  puntos_disponibles: number;
  puntos_canjeados: number;
  // Nuevos campos para verificación y OAuth
  email_verificado: boolean;
  fecha_verificacion?: string;
  google_id?: string;
  avatar_url?: string;
  proveedor_auth: 'local' | 'google';
}

export interface PuntosData {
  puntos_totales: number;
  puntos_disponibles: number;
  puntos_canjeados: number;
}

export interface Premio {
  id_premio: number;
  nombre: string;
  descripcion: string;
  costo_puntos: number;
  stock_disponible: number;
  imagen_url?: string;
  esta_disponible: boolean;
  fecha_creacion: string;
  fecha_actualizacion?: string;
}

export interface Canje {
  id_canje: number;
  id_usuario: number;
  id_premio: number;
  puntos_utilizados: number;
  fecha_solicitud: string;
  fecha_aprobacion?: string;
  estado: 'pendiente' | 'aprobado' | 'rechazado' | 'entregado';
  observaciones?: string;
  id_admin_aprobador?: number;
}

export interface Encuesta {
  id_encuesta: number;
  titulo: string;
  descripcion: string;
  imagen_url?: string;
  fecha_inicio: string;
  fecha_fin: string;
  puntos_recompensa: number;
  estado: 'borrador' | 'activa' | 'finalizada';
  id_creador: number;
  fecha_creacion: string;
  fecha_actualizacion?: string;
}

export interface Participacion {
  id_participacion: number;
  id_encuesta: number;
  id_usuario: number;
  fecha_participacion: string;
  puntos_obtenidos: number;
  estado: 'completada' | 'pendiente';
}

export interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
}

export interface ErrorResponse {
  detail: string;
  status_code: number;
}

export type EstadoCanje = 'pendiente' | 'aprobado' | 'rechazado' | 'entregado';
export type EstadoEncuesta = 'borrador' | 'activa' | 'finalizada';
export type EstadoParticipacion = 'completada' | 'pendiente'; 