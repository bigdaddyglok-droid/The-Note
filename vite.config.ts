import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  return {
    plugins: [react()],
    server: {
      port: Number(env.VITE_PORT ?? 5173),
      host: true,
      proxy: {
        "/api": {
          target: env.VITE_BACKEND_URL ?? "http://127.0.0.1:8000",
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, "")
        }
      }
    },
    build: {
      sourcemap: true,
      target: "es2020",
      chunkSizeWarningLimit: 700
    }
  };
});
