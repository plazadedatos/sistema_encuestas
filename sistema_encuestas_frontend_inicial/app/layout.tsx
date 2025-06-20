import "./globals.css";
import Topbar from "../components/Topbar";
import Footer from "../components/Footer";

export const metadata = {
  title: "Encuestas con Recompensas",
  description: "Sistema de Encuestas Inteligentes",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es">
      <body>
        <Topbar />
        <main className="pt-20">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
