# app/services/email_service.py
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import aiosmtplib
from jinja2 import Template
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        # Configuración desde variables de entorno
        self.smtp_host = os.getenv("SMTP_SERVER", "smtp.gmail.com")  # Cambiado de SMTP_HOST a SMTP_SERVER
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USERNAME", "")  # Cambiado de SMTP_USER a SMTP_USERNAME
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", self.smtp_user)
        self.from_name = os.getenv("FROM_NAME", "Sistema de Encuestas")
        self.frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        
        # Log de configuración (sin mostrar contraseñas)
        logger.info(f"📧 Email Service configurado:")
        logger.info(f"  - SMTP Server: {self.smtp_host}:{self.smtp_port}")
        logger.info(f"  - From: {self.from_email}")
        logger.info(f"  - Frontend URL: {self.frontend_url}")
        if not self.smtp_user or not self.smtp_password:
            logger.warning("⚠️ SMTP credentials not configured. Email sending will fail.")
        
    async def enviar_correo_verificacion(self, email: str, nombre: str, token: str) -> bool:
        """Envía un correo de verificación al usuario"""
        try:
            # Verificar que tengamos las credenciales necesarias
            if not self.smtp_user or not self.smtp_password:
                logger.error("❌ No se pueden enviar emails: SMTP_USERNAME y SMTP_PASSWORD no están configurados")
                logger.info("📋 Por favor configura las siguientes variables en tu archivo .env:")
                logger.info("   SMTP_SERVER=smtp.gmail.com")
                logger.info("   SMTP_PORT=587")
                logger.info("   SMTP_USERNAME=tu_email@gmail.com")
                logger.info("   SMTP_PASSWORD=tu_app_password")
                return False
                
            # Generar el enlace de verificación
            verification_link = f"{self.frontend_url}/verificar-correo?token={token}"
            
            # Plantilla HTML del correo
            html_template = """
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                    .header { background-color: #4A90E2; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }
                    .content { background-color: #f9f9f9; padding: 30px; border-radius: 0 0 5px 5px; }
                    .button { display: inline-block; padding: 12px 30px; background-color: #4A90E2; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }
                    .footer { text-align: center; margin-top: 20px; color: #666; font-size: 12px; }
                    .code { background-color: #e0e0e0; padding: 10px; font-size: 24px; font-weight: bold; text-align: center; margin: 20px 0; letter-spacing: 3px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>¡Bienvenido a Sistema de Encuestas!</h1>
                    </div>
                    <div class="content">
                        <h2>Hola {{ nombre }},</h2>
                        <p>Gracias por registrarte en nuestro sistema. Para completar tu registro y comenzar a ganar puntos, necesitas verificar tu correo electrónico.</p>
                        
                        <p><strong>Opción 1:</strong> Haz clic en el siguiente botón:</p>
                        <div style="text-align: center;">
                            <a href="{{ verification_link }}" class="button">Verificar mi correo</a>
                        </div>
                        
                        <p><strong>Opción 2:</strong> O copia y pega este enlace en tu navegador:</p>
                        <p style="word-break: break-all; background-color: #e0e0e0; padding: 10px;">{{ verification_link }}</p>
                        
                        <p><strong>Opción 3:</strong> Si prefieres, puedes usar este código:</p>
                        <div class="code">{{ token[:6] }}</div>
                        
                        <p style="color: #666; font-size: 14px;">Este enlace expirará en 24 horas. Si no solicitaste este registro, puedes ignorar este correo.</p>
                    </div>
                    <div class="footer">
                        <p>© 2024 Sistema de Encuestas. Todos los derechos reservados.</p>
                        <p>Este es un correo automático, por favor no respondas a este mensaje.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Renderizar la plantilla
            template = Template(html_template)
            html_content = template.render(
                nombre=nombre,
                verification_link=verification_link,
                token=token
            )
            
            # Crear el mensaje
            message = MIMEMultipart('alternative')
            message['Subject'] = 'Verifica tu correo - Sistema de Encuestas'
            message['From'] = f"{self.from_name} <{self.from_email}>"
            message['To'] = email
            
            # Versión de texto plano
            text_content = f"""
            Hola {nombre},
            
            Gracias por registrarte en Sistema de Encuestas.
            
            Para verificar tu correo, visita el siguiente enlace:
            {verification_link}
            
            O usa este código: {token[:6]}
            
            Este enlace expirará en 24 horas.
            
            Saludos,
            El equipo de Sistema de Encuestas
            """
            
            message.attach(MIMEText(text_content, 'plain'))
            message.attach(MIMEText(html_content, 'html'))
            
            # Enviar el correo de forma asíncrona
            await aiosmtplib.send(
                message,
                hostname=self.smtp_host,
                port=self.smtp_port,
                username=self.smtp_user,
                password=self.smtp_password,
                start_tls=True
            )
            
            logger.info(f"Correo de verificación enviado a {email}")
            return True
            
        except Exception as e:
            logger.error(f"Error al enviar correo de verificación: {str(e)}")
            return False
    
    async def enviar_correo_bienvenida_google(self, email: str, nombre: str) -> bool:
        """Envía un correo de bienvenida a usuarios que se registran con Google"""
        try:
            html_template = """
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                    .header { background-color: #4285F4; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }
                    .content { background-color: #f9f9f9; padding: 30px; border-radius: 0 0 5px 5px; }
                    .button { display: inline-block; padding: 12px 30px; background-color: #4285F4; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }
                    .footer { text-align: center; margin-top: 20px; color: #666; font-size: 12px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>¡Bienvenido a Sistema de Encuestas!</h1>
                    </div>
                    <div class="content">
                        <h2>Hola {{ nombre }},</h2>
                        <p>¡Tu cuenta ha sido creada exitosamente usando Google!</p>
                        <p>Ya puedes comenzar a participar en encuestas y ganar puntos para canjear por increíbles premios.</p>
                        
                        <div style="text-align: center;">
                            <a href="{{ frontend_url }}/panel" class="button">Ir al Panel</a>
                        </div>
                        
                        <p><strong>¿Qué puedes hacer ahora?</strong></p>
                        <ul>
                            <li>✅ Responder encuestas y ganar puntos</li>
                            <li>🎁 Canjear puntos por premios</li>
                            <li>📊 Ver tu historial de participaciones</li>
                            <li>👤 Actualizar tu perfil</li>
                        </ul>
                    </div>
                    <div class="footer">
                        <p>© 2024 Sistema de Encuestas. Todos los derechos reservados.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            template = Template(html_template)
            html_content = template.render(
                nombre=nombre,
                frontend_url=self.frontend_url
            )
            
            message = MIMEMultipart('alternative')
            message['Subject'] = '¡Bienvenido! - Sistema de Encuestas'
            message['From'] = f"{self.from_name} <{self.from_email}>"
            message['To'] = email
            
            message.attach(MIMEText(html_content, 'html'))
            
            await aiosmtplib.send(
                message,
                hostname=self.smtp_host,
                port=self.smtp_port,
                username=self.smtp_user,
                password=self.smtp_password,
                start_tls=True
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error al enviar correo de bienvenida: {str(e)}")
            return False
    
    async def enviar_correo_recuperacion(self, email: str, nombre: str, token: str) -> bool:
        """Envía un correo de recuperación de contraseña al usuario"""
        try:
            # Generar el enlace de recuperación
            reset_link = f"{self.frontend_url}/reset-password?token={token}"
            
            # Plantilla HTML del correo
            html_template = """
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                    .header { background-color: #E74C3C; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }
                    .content { background-color: #f9f9f9; padding: 30px; border-radius: 0 0 5px 5px; }
                    .button { display: inline-block; padding: 12px 30px; background-color: #E74C3C; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }
                    .footer { text-align: center; margin-top: 20px; color: #666; font-size: 12px; }
                    .warning { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 5px; color: #856404; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Recuperación de Contraseña</h1>
                    </div>
                    <div class="content">
                        <h2>Hola {{ nombre }},</h2>
                        <p>Hemos recibido una solicitud para restablecer la contraseña de tu cuenta en Sistema de Encuestas.</p>
                        
                        <p>Para continuar con el proceso, haz clic en el siguiente botón:</p>
                        <div style="text-align: center;">
                            <a href="{{ reset_link }}" class="button">Restablecer mi contraseña</a>
                        </div>
                        
                        <p>O copia y pega este enlace en tu navegador:</p>
                        <p style="word-break: break-all; background-color: #e0e0e0; padding: 10px;">{{ reset_link }}</p>
                        
                        <div class="warning">
                            <strong>⚠️ Importante:</strong>
                            <ul>
                                <li>Este enlace expirará en <strong>15 minutos</strong> por razones de seguridad</li>
                                <li>Si no solicitaste este cambio, ignora este correo</li>
                                <li>Tu contraseña actual permanecerá sin cambios hasta que completes el proceso</li>
                            </ul>
                        </div>
                        
                        <p style="color: #666; font-size: 14px;">Por tu seguridad, nunca compartas este enlace con nadie.</p>
                    </div>
                    <div class="footer">
                        <p>© 2024 Sistema de Encuestas. Todos los derechos reservados.</p>
                        <p>Este es un correo automático, por favor no respondas a este mensaje.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Renderizar la plantilla
            template = Template(html_template)
            html_content = template.render(
                nombre=nombre,
                reset_link=reset_link
            )
            
            # Crear el mensaje
            message = MIMEMultipart('alternative')
            message['Subject'] = 'Recuperación de Contraseña - Sistema de Encuestas'
            message['From'] = f"{self.from_name} <{self.from_email}>"
            message['To'] = email
            
            # Versión de texto plano
            text_content = f"""
            Hola {nombre},
            
            Hemos recibido una solicitud para restablecer la contraseña de tu cuenta.
            
            Para restablecer tu contraseña, visita el siguiente enlace:
            {reset_link}
            
            Este enlace expirará en 15 minutos por razones de seguridad.
            
            Si no solicitaste este cambio, puedes ignorar este correo.
            
            Saludos,
            El equipo de Sistema de Encuestas
            """
            
            message.attach(MIMEText(text_content, 'plain'))
            message.attach(MIMEText(html_content, 'html'))
            
            # Enviar el correo de forma asíncrona
            await aiosmtplib.send(
                message,
                hostname=self.smtp_host,
                port=self.smtp_port,
                username=self.smtp_user,
                password=self.smtp_password,
                start_tls=True
            )
            
            logger.info(f"Correo de recuperación enviado a {email}")
            return True
            
        except Exception as e:
            logger.error(f"Error al enviar correo de recuperación: {str(e)}")
            return False

# Instancia global del servicio
email_service = EmailService() 