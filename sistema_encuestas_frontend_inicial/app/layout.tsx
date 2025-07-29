// app/layout.tsx
import './globals.css';
import { AuthProvider } from '../context/authContext';
import GoogleProviderWrapper from '@/components/GoogleProviderWrapper';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es">
      <body>
        <GoogleProviderWrapper>
          <AuthProvider>{children}</AuthProvider>
        </GoogleProviderWrapper>
      </body>
    </html>
  );
}
