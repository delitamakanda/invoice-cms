import { defineConfig } from 'vite'
import BundleTacker from 'webpack-bundle-tracker'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [
      vue()
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://localhost:3000',
        changeOrigin: true,
        secure: false,
      },
    }
  },
  build: {
    outDir: path.resolve(__dirname, './dist'),
    assetsDir: 'assets',
    filenameHashing: true,
    publicPath: import.meta.VUE_APP_NODE_ENV === 'production' ? '/static/': 'http://0.0.0.0:8080',
    outputDir: './dist/',
    stats: 'errors-only'
  }
})
