from fastapi import APIRouter, Depends
from app.auth.dependencies import require_admin
from app.schemas.token import TokenData

router = APIRouter(tags=["Admin"])

@router.get("/admin/dashboard")
async def admin_dashboard(usuario: TokenData = Depends(require_admin)):
    return {
        "mensaje": f"Bienvenido al panel de administración, {usuario.id_usuario}",
        "rol_id": usuario.rol_id
    }
