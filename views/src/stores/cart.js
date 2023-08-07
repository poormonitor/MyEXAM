import { ref } from "vue";
import { defineStore } from "pinia";
import { axios } from "../axios";
import { useUserStore } from "./user";

const userStore = useUserStore();

export const useCartStore = defineStore(
    "cart",
    () => {
        const cart = ref([]);

        function add(pid) {
            cart.value.push(pid);
        }

        function del(fid) {
            cart.value = cart.value.filter((item) => item !== fid);
        }

        function has(fid) {
            return cart.value.includes(fid);
        }

        function reset() {
            cart.value = [];
        }

        return { cart, add, del, has, reset };
    },
    {
        persist: {
            storage: localStorage,
        },
    }
);
