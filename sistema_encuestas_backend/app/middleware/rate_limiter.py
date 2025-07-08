"""
Rate Limiter Middleware
"""
import time
from collections import defaultdict, deque
from fastapi import HTTPException, Request
from typing import Dict, Deque
import asyncio

class RateLimiter:
    def __init__(self):
        # Almacena las requests por IP: {ip: deque_of_timestamps}
        self.requests: Dict[str, Deque[float]] = defaultdict(lambda: deque())
        # Configuración: máximo 60 requests por minuto por IP
        self.max_requests = 60
        self.window_seconds = 60
        # Configuración especial para login: máximo 5 intentos por minuto
        self.login_max_requests = 5
        self.login_window_seconds = 60
        self.login_requests: Dict[str, Deque[float]] = defaultdict(lambda: deque())

    def is_allowed(self, ip: str, endpoint: str = None) -> bool:
        """Verifica si la IP puede hacer otra request"""
        current_time = time.time()
        
        # Configuración específica para login
        if endpoint and "login" in endpoint:
            requests_deque = self.login_requests[ip]
            max_req = self.login_max_requests
            window = self.login_window_seconds
        else:
            requests_deque = self.requests[ip]
            max_req = self.max_requests
            window = self.window_seconds
        
        # Remover requests antiguas
        while requests_deque and current_time - requests_deque[0] > window:
            requests_deque.popleft()
        
        # Verificar si se puede hacer otra request
        if len(requests_deque) >= max_req:
            return False
        
        # Agregar la request actual
        requests_deque.append(current_time)
        return True

    def cleanup_old_entries(self):
        """Limpia entradas antiguas periódicamente"""
        current_time = time.time()
        
        # Cleanup requests normales
        for ip in list(self.requests.keys()):
            deque_obj = self.requests[ip]
            while deque_obj and current_time - deque_obj[0] > self.window_seconds:
                deque_obj.popleft()
            if not deque_obj:
                del self.requests[ip]
        
        # Cleanup requests de login
        for ip in list(self.login_requests.keys()):
            deque_obj = self.login_requests[ip]
            while deque_obj and current_time - deque_obj[0] > self.login_window_seconds:
                deque_obj.popleft()
            if not deque_obj:
                del self.login_requests[ip]

# Instancia global del rate limiter
rate_limiter = RateLimiter()

async def rate_limit_middleware(request: Request, call_next):
    """Middleware para aplicar rate limiting"""
    # Obtener IP del cliente
    client_ip = request.client.host if request.client else "unknown"
    
    # Verificar rate limiting
    endpoint = str(request.url.path)
    if not rate_limiter.is_allowed(client_ip, endpoint):
        if "login" in endpoint:
            raise HTTPException(
                status_code=429,
                detail="Demasiados intentos de login. Espera 1 minuto antes de intentar nuevamente."
            )
        else:
            raise HTTPException(
                status_code=429,
                detail="Demasiadas requests. Espera un momento antes de continuar."
            )
    
    response = await call_next(request)
    return response

# Tarea en background para limpiar entradas antiguas
async def cleanup_rate_limiter():
    """Limpia el rate limiter cada 5 minutos"""
    while True:
        await asyncio.sleep(300)  # 5 minutos
        rate_limiter.cleanup_old_entries() 