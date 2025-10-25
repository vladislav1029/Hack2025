import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: prtocess.env.PORT ? parseInt(prtocess.env.PORT, 10) : 5184,
  }
})
