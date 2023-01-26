import ax from "axios";
import { message } from "./discrete";
import { useTokenStore } from "./stores/token";
import { useUserStore } from "./stores/user";
import router from "./router/index";

const instance = ax.create({
    baseURL: import.meta.env.VITE_API_URL,
    timeout: 5000,
});

instance.interceptors.request.use(
    (config) => {
        const tokenStore = useTokenStore();
        const userStore = useUserStore();

        if (!tokenStore.token) {
            tokenStore.createToken();
            config.headers["X-MyExam-Token"] = tokenStore.token;
        }

        let access_token = userStore.access_token;

        if (access_token) {
            if (userStore.expires <= new Date().getTime()) {
                userStore.logout();
            } else {
                config.headers.Authorization = "Bearer " + access_token;
            }
        }

        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

instance.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        if (error.response?.status === 401) {
            const userStore = useUserStore();
            userStore.logout();
            message.error("登录失效，请重新登录。");
            router.push({ name: "login" });
        } else if (typeof error.response?.data?.detail === "string") {
            message.error(error.response.data.detail);
        } else {
            message.error(error.message);
        }
        return Promise.reject(error);
    }
);

export const AxiosPlugin = {
    install: (app) => {
        app.provide("axios", instance);
    },
};

export const axios = instance;
