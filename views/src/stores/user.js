import { ref } from "vue";
import { defineStore } from "pinia";

export const useUserStore = defineStore(
    "user",
    () => {
        const uid = ref(null);
        const nick = ref(null);
        const access_token = ref(null);
        const admin = ref(false);

        function login(user_uid, user_nick, user_access_token, user_admin) {
            uid.value = user_uid;
            nick.value = user_nick;
            access_token.value = user_access_token;
            admin.value = user_admin;
        }

        function logout() {
            uid.value = null;
            nick.value = null;
            admin.value = false;
            access_token.value = null;
        }

        return { uid, access_token, admin, nick, login, logout };
    },
    {
        persist: {
            storage: sessionStorage,
        },
    }
);
