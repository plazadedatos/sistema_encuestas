"use client";
import Hero from "../../components/Hero";
import TarjetaEncuesta from "../../components/TarjetaEncuesta";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "../../context/authContext";
import { Encuesta, encuestasService } from "@/app/services/encuestas";
import { SkeletonCard } from "../../components/ui/loading";
import { toast } from "react-toastify";
export default function HomePage() {
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();
  const [encuestas, setEncuestas] = useState<Encuesta[]>([]);
  const [cargandoEncuestas, setCargandoEncuestas] = useState(true);

  // Redirección inmediata para usuarios autenticados
  useEffect(() => {
    if (!loading && isAuthenticated) {
      console.log("🔄 Usuario autenticado detectado, redirigiendo a /panel");
      router.push("/panel");
    }
  }, [isAuthenticated, loading, router]);

  // Cargar encuestas públicas
  useEffect(() => {
    const cargarEncuestas = async () => {
      try {
        setCargandoEncuestas(true);
        const encuestasPublicas = await encuestasService.obtenerEncuestasActivas({
          limit: 6,
          filtro_visibilidad: 'todos'
        });
        setEncuestas(encuestasPublicas);
      } catch (error) {
        console.error('Error al cargar encuestas:', error);
        toast.error('No se pudieron cargar las encuestas');
      } finally {
        setCargandoEncuestas(false);
      }
    };

    cargarEncuestas();
  }, []);
  return (
    <>
      <Hero />
      <section className="container mx-auto px-4 py-20">
        <section className="max-w-7xl mx-auto px-4 py-20">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-6 text-primary">
            ¿Cómo funciona?
          </h2>
          <p className="text-center text-gray-700 max-w-2xl mx-auto text-md md:text-lg mb-12 leading-relaxed">
            En <strong>Plaza de Datos</strong>, ganas puntos por solo responder encuestas desde tu celular o computadora.
            Luego podrás canjearlos por increíbles premios reales, ¡y todo en pocos minutos!
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-8 text-center text-slate-800">
            {/* Paso 1 */}
            <div className="flex flex-col items-center">
              <img src="/img/paso1.png" alt="Paso 1" className="w-20 h-20 mb-3" />
              <h3 className="text-primary font-bold text-lg mb-1">Paso 1</h3>
              <p className="text-sm">
                Regístrate y <span className="font-semibold">confirma tu email</span>
              </p>
            </div>

            {/* Paso 2 */}
            <div className="flex flex-col items-center">
              <img src="/img/paso2.png" alt="Paso 2" className="w-20 h-20 mb-3" />
              <h3 className="text-primary font-bold text-lg mb-1">Paso 2</h3>
              <p className="text-sm">
                Inicia sesión desde tu <span className="font-semibold">computadora o celular</span>
              </p>
            </div>

            {/* Paso 3 */}
            <div className="flex flex-col items-center">
              <img src="/img/paso3.png" alt="Paso 3" className="w-20 h-20 mb-3" />
              <h3 className="text-primary font-bold text-lg mb-1">Paso 3</h3>
              <p className="text-sm">
                Responde encuestas online y <span className="font-semibold">gana puntos</span>
              </p>
            </div>

            {/* Paso 4 */}
            <div className="flex flex-col items-center">
              <img src="/img/paso4.png" alt="Paso 4" className="w-20 h-20 mb-3" />
              <h3 className="text-primary font-bold text-lg mb-1">Paso 4</h3>
              <p className="text-sm">
                Cambia tus puntos por <span className="font-semibold">premios reales</span>
              </p>
            </div>
          </div>
        </section>

         <section id="encuestas" className="max-w-7xl mx-auto px-4 py-24" >
        <h2 className="text-2xl font-bold text-center mb-6">Encuestas Disponibles</h2>
       
        <p className="text-center text-gray-600 mb-10">
          Participa en nuestras encuestas y acumula puntos que podrás canjear por increíbles premios. ¡Tu opinión es valiosa!
        </p>
        
        {cargandoEncuestas ? (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {[...Array(6)].map((_, index) => (
              <SkeletonCard key={index} />
            ))}
          </div>
        ) : encuestas.length > 0 ? (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {encuestas.map((encuesta) => (
              <TarjetaEncuesta 
                key={encuesta.id_encuesta} 
                encuesta={encuesta}
                mostrarEstado={false}
                onParticipate={() => {
                  if (!isAuthenticated) {
                    toast.info("Inicia sesión para responder encuestas");
                    router.push("/login");
                  } else {
                    router.push(`/panel/encuestas/${encuesta.id_encuesta}`);
                  }
                }}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <div className="text-gray-400 text-6xl mb-4">📝</div>
            <h3 className="text-xl font-semibold text-gray-600 mb-2">
              No hay encuestas disponibles
            </h3>
            <p className="text-gray-500">
              Vuelve pronto para encontrar nuevas encuestas
            </p>
          </div>
        )}
        
        {!isAuthenticated && encuestas.length > 0 && (
          <div className="text-center mt-8">
            <p className="text-gray-600 mb-4">
              ¿Quieres participar en más encuestas y ganar puntos?
            </p>
            <button
              onClick={() => router.push("/registro")}
              className="bg-primary hover:bg-primary-dark text-white px-6 py-3 rounded-md font-medium transition-colors"
            >
              Regístrate Gratis
            </button>
          </div>
        )}
        </section>
        <section className="max-w-4xl mx-auto px-4 py-20" id="faq">
          <h2 className="text-4xl font-bold text-center text-primary mb-10">
            Preguntas frecuentes
          </h2>

          <div className="space-y-6">
            {/* FAQ 1 */}
            <details className="group border-b border-gray-200 pb-4">
              <summary className="flex items-center justify-between cursor-pointer text-lg font-semibold text-slate-800">
                <span>¿Cómo empiezo a participar?</span>
                <span className="transition-transform group-open:rotate-90 text-primary">▶</span>
              </summary>
              <p className="text-sm text-slate-600 mt-2">
                Solo necesitas registrarte llenando un pequeño formulario con tus datos básicos. Luego de confirmar tu correo electrónico, podrás comenzar a responder encuestas y ganar puntos.
              </p>
            </details>

            {/* FAQ 2 */}
            <details className="group border-b border-gray-200 pb-4">
              <summary className="flex items-center justify-between cursor-pointer text-lg font-semibold text-slate-800">
                <span>¿Qué tipo de recompensas puedo obtener?</span>
                <span className="transition-transform group-open:rotate-90 text-primary">▶</span>
              </summary>
              <p className="text-sm text-slate-600 mt-2">
                Desde tarjetas de regalo, productos, descuentos hasta sorteos exclusivos. Todo depende de la cantidad de puntos que acumules.
              </p>
            </details>

            {/* FAQ 3 */}
            <details className="group border-b border-gray-200 pb-4">
              <summary className="flex items-center justify-between cursor-pointer text-lg font-semibold text-slate-800">
                <span>¿Quiénes pueden participar?</span>
                <span className="transition-transform group-open:rotate-90 text-primary">▶</span>
              </summary>
              <p className="text-sm text-slate-600 mt-2">
                Cualquier persona mayor de 18 años con acceso a internet puede registrarse y formar parte de la comunidad de Plaza de Datos.
              </p>
            </details>

            {/* FAQ 4 */}
            <details className="group border-b border-gray-200 pb-4">
              <summary className="flex items-center justify-between cursor-pointer text-lg font-semibold text-slate-800">
                <span>¿Cuánto tiempo duran las encuestas?</span>
                <span className="transition-transform group-open:rotate-90 text-primary">▶</span>
              </summary>
              <p className="text-sm text-slate-600 mt-2">
                La mayoría toma entre 3 y 10 minutos. Siempre verás el tiempo estimado antes de comenzar.
              </p>
            </details>

            {/* FAQ 5 */}
            <details className="group border-b border-gray-200 pb-4">
              <summary className="flex items-center justify-between cursor-pointer text-lg font-semibold text-slate-800">
                <span>¿Es seguro compartir mis datos?</span>
                <span className="transition-transform group-open:rotate-90 text-primary">▶</span>
              </summary>
              <p className="text-sm text-slate-600 mt-2">
                Absolutamente. Toda tu información está protegida por políticas de privacidad y cifrado. Nunca compartimos tus datos sin tu consentimiento.
              </p>
            </details>

            {/* FAQ 6 */}
            <details className="group border-b border-gray-200 pb-4">
              <summary className="flex items-center justify-between cursor-pointer text-lg font-semibold text-slate-800">
                <span>¿Puedo dejar de participar cuando quiera?</span>
                <span className="transition-transform group-open:rotate-90 text-primary">▶</span>
              </summary>
              <p className="text-sm text-slate-600 mt-2">
                Sí, puedes darte de baja en cualquier momento desde tu perfil. Tus datos se eliminarán si lo solicitás.
              </p>
            </details>
          </div>
        </section>
<section id="nosotros" className="max-w-6xl mx-auto px-4 py-24">
  <div className="grid md:grid-cols-2 gap-10 items-center">
    
    {/* Texto */}
    <div>
      <h2 className="text-3xl md:text-4xl font-bold text-primary mb-6">Quiénes somos</h2>
      <p className="text-gray-700 leading-relaxed text-base md:text-lg">
        En <strong>Plaza de Datos</strong>, somos un equipo apasionado por la recopilación inteligente de datos para generar impacto real. 
        Nuestro objetivo es <span className="font-medium">conectar personas y organizaciones</span> a través de encuestas estratégicas, estadísticas y participación ciudadana.
        <br /><br />
        Promovemos la voz de la gente y convertimos sus respuestas en oportunidades de mejora para empresas, instituciones y comunidades.
        Creemos en el poder de la información colectiva para construir un futuro más informado.
      </p>
    </div>

    {/* Imagen */}
    <div className="flex justify-center">
      <img
        src="/img/nosotros.png"     // ← pon tu imagen aquí
        alt="Equipo de Plaza de Datos"
        className="w-full max-w-md rounded-[2rem] shadow-xl"
      />
    </div>
  </div>
</section>

      </section>
    </>
  );
}
