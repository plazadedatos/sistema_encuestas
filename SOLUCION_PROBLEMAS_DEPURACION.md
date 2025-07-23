# 🔧 Soluciones a Problemas de Depuración - Sistema de Encuestas

## 📋 Problemas Identificados y Soluciones

### 🧩 **Problema 1: El registro de usuario no funciona**

#### 🔍 **Diagnóstico:**
- El frontend muestra "Iniciando proceso de registro..." pero el backend no recibe la petición
- No hay logs HTTP en la consola del backend
- El request no está llegando al servidor

#### ✅ **Soluciones Implementadas:**

1. **Mejorado el logging en el frontend:**
   ```typescript
   // En app/registro/page.tsx
   console.log("🌐 URL de la API:", `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/auth/registro`);
   console.log("📦 Request data:", config.data);
   console.log("🔧 Request headers:", config.headers);
   ```

2. **Mejorado el logging en el servicio de API:**
   ```typescript
   // En app/services/api.ts
   console.log(`📦 Request data:`, config.data);
   console.log(`🔧 Request headers:`, config.headers);
   ```

3. **Scripts de prueba creados:**
   - `test_registro_simple.py` - Para probar el endpoint de registro
   - `verificar_backend.py` - Para verificar que el backend esté funcionando

#### 🔧 **Pasos para depurar:**

1. **Verificar que el backend esté corriendo:**
   ```bash
   python verificar_backend.py
   ```

2. **Probar el endpoint de registro directamente:**
   ```bash
   python test_registro_simple.py
   ```

3. **Verificar en el navegador:**
   - Abrir DevTools (F12)
   - Ir a la pestaña Network
   - Intentar registrar un usuario
   - Verificar si aparece la petición HTTP

4. **Verificar variables de entorno:**
   - Asegurar que `NEXT_PUBLIC_API_URL` esté configurado correctamente
   - Por defecto usa `http://localhost:8000`

---

### 🧩 **Problema 2: No se pueden enviar respuestas de encuestas**

#### 🔍 **Diagnóstico:**
- Error 400 Bad Request al enviar respuestas
- El request llega al backend pero es rechazado
- Problema de validación de datos

#### ✅ **Soluciones Implementadas:**

1. **Corregido el payload del frontend:**
   ```typescript
   // En app/panel/encuestas/[id]/page.tsx
   const requestData = {
     id_encuesta: Number(id),
     respuestas: payload,
     tiempo_total: 0 // Agregado campo requerido
   };
   ```

2. **Mejorado el logging de errores:**
   ```typescript
   console.error("❌ Error al enviar respuestas:", err);
   console.error("❌ Detalles del error:", {
     message: err.message,
     status: err.response?.status,
     data: err.response?.data,
   });
   ```

3. **Agregado logging en el backend:**
   ```python
   # En app/routers/respuestas_router.py
   print(f"📝 Recibiendo respuestas para encuesta {data.id_encuesta}")
   print(f"👤 Usuario: {current_user.email}")
   print(f"📊 Datos recibidos: {data}")
   ```

#### 🔧 **Estructura de datos esperada:**

**Frontend debe enviar:**
```json
{
  "id_encuesta": 1,
  "tiempo_total": 120,
  "respuestas": [
    {
      "id_pregunta": 1,
      "id_opcion": 1,
      "respuesta_texto": null
    },
    {
      "id_pregunta": 2,
      "id_opcion": null,
      "respuesta_texto": "Texto de respuesta"
    }
  ]
}
```

**Backend espera (RespuestasEnvio):**
```python
class RespuestasEnvio(BaseModel):
    id_encuesta: int
    tiempo_total: Optional[int] = None
    respuestas: List[RespuestaSchema]

class RespuestaSchema(BaseModel):
    id_pregunta: int    
    id_opcion: Optional[int] = None
    respuesta_texto: Optional[str] = None
    tiempo_respuesta_segundos: Optional[int] = None
```

---

## 🧹 **Limpieza de Archivos Realizada**

### 📁 **Archivos Eliminados del Backend:**
- `actualizar_usuario_frontend.py`
- `generar_nuevo_token.py`
- `Verifica tu correo - Sistema de Encuestas.eml`
- `verificar_email_manual.py`
- `configurar_email.py`
- `test_google_oauth.py`
- `configurar_google_oauth.py`
- `verificar_google_oauth.py`
- `test_login.py`
- `fix_database.py`
- `verificar_implementacion.py`
- `verificar_premios.py`
- `verificar_migracion.py`
- `crear_admin.py`
- `test_api.py`
- `debug_login.py`
- `create_admin_fixed.py`
- `check_constraints.py`
- `create_admin_actual.py`
- `check_db.py`
- `recrear_db.py`
- `verificar_db.py`
- `simple_start.py`
- `start_server.py`
- `app.log`

### 📁 **Archivos Eliminados del Directorio Raíz:**
- `test_registro_completo.py`
- `test_server.py`
- `verificar_docker_frontend.py`
- `limpiar_usuarios_prueba.py`
- `app.log`

### 📁 **Archivos de Prueba Creados:**
- `test_registro_simple.py` - Prueba endpoint de registro
- `test_respuestas_simple.py` - Prueba endpoint de respuestas
- `verificar_backend.py` - Verifica funcionamiento del backend

---

## 🚀 **Próximos Pasos**

1. **Ejecutar el backend:**
   ```bash
   cd sistema_encuestas_backend
   python run.py
   ```

2. **Ejecutar el frontend:**
   ```bash
   cd sistema_encuestas_frontend_inicial
   npm run dev
   ```

3. **Probar el registro:**
   ```bash
   python test_registro_simple.py
   ```

4. **Probar las respuestas:**
   ```bash
   python test_respuestas_simple.py
   ```

5. **Verificar en el navegador:**
   - Ir a `http://localhost:3000/registro`
   - Intentar registrar un usuario
   - Verificar logs en la consola del navegador

---

## 🔍 **Comandos de Depuración Útiles**

### **Verificar logs del backend:**
```bash
cd sistema_encuestas_backend
python run.py
```

### **Verificar logs del frontend:**
- Abrir DevTools (F12)
- Ir a la pestaña Console
- Intentar las operaciones y revisar los logs

### **Probar endpoints directamente:**
```bash
# Probar registro
curl -X POST http://localhost:8000/api/auth/registro \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Test","apellido":"Usuario","documento_numero":"12345678","email":"test@ejemplo.com","password":"123456"}'

# Probar ping
curl http://localhost:8000/api/ping
```

---

## 📝 **Notas Importantes**

1. **CORS:** El backend está configurado para aceptar peticiones desde `http://localhost:3000`
2. **Variables de entorno:** El frontend usa `NEXT_PUBLIC_API_URL` o por defecto `http://localhost:8000`
3. **Logging:** Se agregó logging detallado para facilitar la depuración
4. **Validación:** Los esquemas Pydantic validan los datos antes de procesarlos

---

## 🆘 **Si los problemas persisten:**

1. **Verificar que ambos servicios estén corriendo**
2. **Revisar los logs en la consola del navegador**
3. **Revisar los logs del backend**
4. **Usar los scripts de prueba para verificar endpoints**
5. **Verificar la configuración de CORS**
6. **Verificar las variables de entorno** 