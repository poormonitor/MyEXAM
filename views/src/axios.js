import axios from "axios";
import { message } from "./discrete";
import { useTokenStore } from "./stores/token";
import { useUserStore } from "./stores/user";
import router from "./router/index";

export default {
    install: (app, options) => {
        const instance = axios.create({
            baseURL: import.meta.env.VITE_API_URL,
            timeout: 5000,
        });

        instance.interceptors.request.use(
            (config) => {
                const tokenStore = useTokenStore();
                const userStore = useUserStore();

                let access_token = userStore.access_token;

                if (access_token) {
                    config.headers.Authorization = "Bearer " + access_token;
                    tokenStore.token = userStore.uid;
                }

                if (!tokenStore.token) {
                    tokenStore.createToken();
                }

                config.headers["X-MyExam-Token"] = tokenStore.token;

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
        app.provide("axios", instance);
    },
};
