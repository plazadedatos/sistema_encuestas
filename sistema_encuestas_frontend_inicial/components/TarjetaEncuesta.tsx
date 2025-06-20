import { FaPoll } from "react-icons/fa";

export default function TarjetaEncuesta({
  titulo,
  puntos,
}: {
  titulo: string;
  puntos: number;
}) {
  return (
    <article
      className="
        group
        bg-white rounded-2xl p-6 flex flex-col gap-4
        shadow-lg transition
        hover:-translate-y-2 hover:shadow-xl
        active:translate-y-0
      "
    >
      <div className="flex items-center gap-3">
        <FaPoll className="text-primary text-3xl transition group-hover:rotate-6" />
        <h4 className="text-lg font-semibold">{titulo}</h4>
      </div>

      <p className="text-sm text-slate-600">
        Gana{" "}
        <span className="text-primary font-bold">{puntos} puntos</span>{" "}
        completando esta encuesta.
      </p>

      <button
        className="
          mt-auto self-start px-4 py-2 rounded-lg font-medium
          bg-primary text-white
          hover:bg-primary-dark transition
        "
      >
        Ver detalles
      </button>
    </article>
  );
}
