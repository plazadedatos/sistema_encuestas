# 🔧 Optimización: API Centralizada

## 📋 Objetivo

Centralizar todas las llamadas a la API en el archivo `app/services/api.ts` para:
- **Facilitar cambios de configuración** (URL, puerto, etc.)
- **Mantener consistencia** en el manejo de errores
- **Reducir duplicación de código**
- **Mejorar mantenibilidad**

---

## 🏗️ **Arquitectura de la API Centralizada**

### **Archivo Principal: `app/services/api.ts`**
```typescript
// Configuración centralizada
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Instancia de Axios configurada
const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
});

// Interceptores para:
// - Agregar tokens automáticamente
// - Logging de requests/responses
// - Manejo global de errores
// - Redirección automática en errores 401
```

### **Características:**
- ✅ **Base URL configurable** desde variables de entorno
- ✅ **Interceptores automáticos** para autenticación
- ✅ **Logging detallado** para debugging
- ✅ **Manejo global de errores** con toasts
- ✅ **Redirección automática** en sesiones expiradas

---

## 🔄 **Archivos Optimizados**

### **1. `app/test-cors/page.tsx`**
**Antes:**
```typescript
const response = await fetch('http://localhost:8000/api/ping');
const data = await response.json();
```

**Después:**
```typescript
const response = await api.get('/ping');
const data = response.data;
```

### **2. `app/verificar-correo/page.tsx`**
**Antes:**
```typescript
const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/verificar-correo?token=${token}`, {
  method: 'GET',
});
const data = await response.json();
```

**Después:**
```typescript
const response = await api.get(`/auth/verificar-correo?token=${token}`);
const data = response.data;
```

### **3. `components/GoogleLoginButton.tsx`**
**Antes:**
```typescript
const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/google`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ id_token: credentialResponse.credential }),
});
const data = await response.json();
```

**Después:**
```typescript
const response = await api.post('/auth/google', { 
  id_token: credentialResponse.credential 
});
const data = response.data;
```

### **4. `app/administracion/encuestas/page.tsx`**
**Antes:**
```typescript
import axios from "axios";
const uploadRes = await axios.post("/api/imagenes", formData);
```

**Después:**
```typescript
// axios eliminado de imports
const uploadRes = await api.post("/imagenes", formData);
```

---

## 🎯 **Beneficios Implementados**

### **1. Configuración Centralizada**
- **Un solo lugar** para cambiar la URL de la API
- **Variables de entorno** para diferentes entornos
- **Configuración automática** de base URL

### **2. Manejo de Errores Consistente**
- **Interceptores globales** para errores HTTP
- **Toasts automáticos** para errores comunes
- **Redirección automática** en sesiones expiradas
- **Logging detallado** para debugging

### **3. Autenticación Automática**
- **Tokens automáticos** en headers
- **Limpieza automática** de datos de sesión
- **Renovación automática** de tokens (si se implementa)

### **4. Logging Automático**
- **Requests** con URL, método y datos
- **Responses** con status y datos
- **Errores** con detalles completos
- **Debugging** más fácil

---

## 🚀 **Uso de la API Centralizada**

### **Importar la API:**
```typescript
import api from '@/app/services/api';
```

### **Métodos Disponibles:**
```typescript
// GET requests
const response = await api.get('/endpoint');

// POST requests
const response = await api.post('/endpoint', data);

// PUT requests
const response = await api.put('/endpoint', data);

// PATCH requests
const response = await api.patch('/endpoint', data);

// DELETE requests
const response = await api.delete('/endpoint');

// Con parámetros de query
const response = await api.get('/endpoint?param=value');

// Con headers personalizados
const response = await api.post('/endpoint', data, {
  headers: { 'Custom-Header': 'value' }
});
```

### **Manejo de Respuestas:**
```typescript
try {
  const response = await api.get('/endpoint');
  const data = response.data;
  // Procesar datos
} catch (error) {
  // Error ya manejado por interceptores
  // Toast automático mostrado
  console.error('Error específico:', error);
}
```

---

## 🔧 **Configuración de Entornos**

### **Variables de Entorno:**
```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000

# .env.production
NEXT_PUBLIC_API_URL=https://api.tudominio.com
```

### **Fallback Automático:**
Si `NEXT_PUBLIC_API_URL` no está definida, usa `http://localhost:8000`

---

## 🧪 **Pruebas**

### **Script de Prueba:**
```bash
python test_api_centralizada.py
```

### **Verificación Manual:**
1. **Abrir DevTools** en el navegador
2. **Ir a pestaña Console**
3. **Hacer cualquier acción** que use la API
4. **Verificar logs** automáticos:
   ```
   🌐 API base URL: http://localhost:8000/api
   ➡️  GET http://localhost:8000/api/endpoint
   📦 Request data: {...}
   🔧 Request headers: {...}
   ```

---

## 📊 **Métricas de Mejora**

### **Antes de la Optimización:**
- ❌ URLs hardcodeadas en múltiples archivos
- ❌ Manejo de errores inconsistente
- ❌ Logging manual en cada request
- ❌ Configuración duplicada
- ❌ Difícil mantenimiento

### **Después de la Optimización:**
- ✅ **1 solo archivo** de configuración
- ✅ **Manejo de errores global** y consistente
- ✅ **Logging automático** en todos los requests
- ✅ **Configuración centralizada**
- ✅ **Fácil mantenimiento** y debugging

---

## 🆘 **Solución de Problemas**

### **Problema: "No se puede conectar al servidor"**
**Solución:**
1. Verificar que el backend esté corriendo
2. Verificar `NEXT_PUBLIC_API_URL` en variables de entorno
3. Revisar logs en consola del navegador

### **Problema: "Error 401 - Sesión expirada"**
**Solución:**
- El interceptor maneja esto automáticamente
- Redirige a login y limpia datos de sesión
- Toast automático informa al usuario

### **Problema: "Error 403 - Sin permisos"**
**Solución:**
- Toast automático informa al usuario
- Verificar que el usuario tenga los permisos necesarios

---

## 💡 **Próximos Pasos Sugeridos**

### **1. Agregar Más Interceptores:**
- **Rate limiting** automático
- **Retry automático** en errores de red
- **Cache automático** para requests GET

### **2. Mejorar Logging:**
- **Logs estructurados** para análisis
- **Métricas de performance** de requests
- **Alertas automáticas** para errores críticos

### **3. Agregar Funcionalidades:**
- **Refresh tokens** automático
- **Offline mode** con cache
- **Request queuing** para operaciones críticas

---

## 🎉 **Resultado Final**

✅ **API completamente centralizada**
✅ **Manejo de errores consistente**
✅ **Logging automático para debugging**
✅ **Configuración flexible por entornos**
✅ **Código más limpio y mantenible**
✅ **Mejor experiencia de desarrollo** 