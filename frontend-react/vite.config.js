import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
    plugins: [react()],

    server: {
        port: 5173,

        proxy: {
            "/api": {
                target: "http://127.0.0.1:5000",
                changeOrigin: true,
            },

            "/health": {
                target: "http://127.0.0.1:5000",
                changeOrigin: true,
            },

            "/start_camera": {
                target: "http://127.0.0.1:5000",
                changeOrigin: true,
            },

            "/stop_camera": {
                target: "http://127.0.0.1:5000",
                changeOrigin: true,
            },

            "/video_feed": {
                target: "http://127.0.0.1:5000",
                changeOrigin: true,
            },

            "/capture_snapshot": {
                target: "http://127.0.0.1:5000",
                changeOrigin: true,
            },
        },
    },
});