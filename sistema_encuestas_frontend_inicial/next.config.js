/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  webpack: (config, { buildId, dev, isServer, defaultLoaders, webpack }) => {
    // Asegurar que los alias funcionen correctamente
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': require('path').resolve(__dirname, './'),
    };
    return config;
  },
  // Configuración para Docker
  output: 'standalone',
  // Deshabilitar telemetría
  telemetry: false,
}

module.exports = nextConfig
