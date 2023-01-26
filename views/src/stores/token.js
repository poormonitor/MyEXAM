import { ref } from "vue";
import { defineStore } from "pinia";
import { v1 as uuidv1 } from "uuid";

export const useTokenStore = defineStore(
    "token",
    () => {
        const token = ref(null);

        function createToken() {
            token.value = uuidv1();
        }

        return { token, createToken };
    },
    {
        persist: {
            storage: localStorage,
        },
    }
);
