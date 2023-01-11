import { ref } from "vue";
import { defineStore } from "pinia";

export const useTokenStore = defineStore(
    "token",
    () => {
        const token = ref(null);

        function createToken() {
            token.value = crypto.randomUUID();
        }

        return { token, createToken };
    },
    {
        persist: {
            storage: localStorage,
        },
    }
);
