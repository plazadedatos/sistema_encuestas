import "../globals.css";
import Topbar from "../../components/Topbar";
import Footer from "../../components/Footer";

export const metadata = {
  title: "Encuestas con Recompensas",
  description: "Sistema de Encuestas Inteligentes",
};

export default function PublicLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <Topbar />
      <main className="pt-20">{children}</main>
      <Footer />
    </>
  );
}
