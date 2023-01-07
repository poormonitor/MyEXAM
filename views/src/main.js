import { createApp } from "vue";
import { createPinia } from "pinia";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";
import axios from "./axios";
import WebFont from "webfontloader";

import App from "./App.vue";
import router from "./router";
import "./assets/index.css";

const app = createApp(App);
const pinia = createPinia();

pinia.use(piniaPluginPersistedstate);

app.use(pinia);
app.use(axios);
app.use(router);

const meta = document.createElement("meta");
meta.name = "naive-ui-style";
document.head.appendChild(meta);

app.mount("#app");

WebFont.load({
    google: {
        families: ["Inter:500,800", "Noto Sans SC:500,800"],
    },
});
