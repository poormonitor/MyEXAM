import axios from "axios";
import { message } from "./discrete";
import { useTokenStore } from "./stores/token";
import { useUserStore } from "./stores/user";

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
                let token = tokenStore.token;

                if (!token) {
                    tokenStore.createToken();
                    token = tokenStore.token;
                }

                config.headers["X-MyExam-Token"] = token;

                if (access_token) {
                    config.headers.Authorization = "Bearer " + token;
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
                if (error.response) {
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
