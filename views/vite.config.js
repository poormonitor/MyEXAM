import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import vueJsx from "@vitejs/plugin-vue-jsx";

import AutoImport from "unplugin-auto-import/vite";
import Components from "unplugin-vue-components/vite";
import { NaiveUiResolver } from "unplugin-vue-components/resolvers";

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        vue(),
        vueJsx(),
        AutoImport({
            imports: [
                "vue",
                {
                    "naive-ui": [
                        "useDialog",
                        "useMessage",
                        "useNotification",
                        "useLoadingBar",
                    ],
                },
            ],
        }),
        Components({
            resolvers: [NaiveUiResolver()],
        }),
    ],
    resolve: {
        alias: {
            "@": fileURLToPath(new URL("./src", import.meta.url)),
        },
    },
    build: {
        chunkSizeWarningLimit: 500,
        cssCodeSplit: false,
        rollupOptions: {
            output: {
                manualChunks: {
                    vue: ["vue", "vue-router", "pinia"],
                    icons: ["@vicons/ionicons5"],
                },
                chunkFileNames: (chunkInfo) => {
                    if (chunkInfo.moduleIds[0].includes("node_modules")) {
                        return "assets/vendor-[hash].js";
                    }
                    return "assets/index-[hash].js";
                },
            },
        },
        brotliSize: false,
    },
});
