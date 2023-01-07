import { ref } from "vue";
import { defineStore } from "pinia";

export const useUserStore = defineStore(
    "user",
    () => {
        const uid = ref(null);
        const access_token = ref(null);
        const admin = ref(false);

        function login(uid, access_token, admin) {
            uid.value = uid;
            access_token.value = access_token;
            admin.value = admin;
        }

        return { uid, access_token, admin, login };
    },
    {
        persist: {
            storage: window.sessionStorage,
        },
    }
);
