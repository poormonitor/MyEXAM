<script setup>
import sha256 from "crypto-js/sha256";
import { useRouter } from "vue-router";
import { useCartStore } from "../stores/cart";
import { useUserStore } from "../stores/user";

const userStore = useUserStore();
const cartStore = useCartStore();
const router = useRouter();
const loading = ref(false);
const axios = inject("axios");

const loginForm = reactive({
    email: "",
    passwd: "",
});

const submitLogin = () => {
    loading.value = true;
    axios
        .post("/user/login", {
            email: loginForm.email,
            password: sha256(loginForm.passwd).toString(),
        })
        .catch(() => {
            loading.value = false;
        })
        .then(async (response) => {
            if (response.data.access_token) {
                let token = response.data.access_token;
                let payload = JSON.parse(atob(token.split(".")[1]));
                userStore.login(
                    token,
                    payload.uid,
                    payload.nick,
                    payload.admin,
                    payload.exp * 1000
                );
                loading.value = true;
                router.push({ name: "home" });
            }
        });
};
</script>

<template>
    <div class="mx-8 w-auto md:mx-auto md:w-[60vw] lg:w-[40vw] my-20">
        <div class="border px-8 md:px-20 py-12 rounded-2xl">
            <p class="text-lg text-red-600 mb-2">欢迎使用 MyEXAM</p>
            <p class="text-4xl font-bold">登录</p>
            <n-form size="large" class="mt-10">
                <n-form-item label="邮箱">
                    <n-input
                        :input-props="{ autocomplete: 'email' }"
                        v-model:value="loginForm.email"
                    ></n-input>
                </n-form-item>
                <n-form-item label="密码">
                    <n-input
                        :input-props="{ autocomplete: 'current-password' }"
                        type="password"
                        v-model:value="loginForm.passwd"
                    ></n-input>
                </n-form-item>
                <div class="flex gap-x-4 justify-center mt-4">
                    <n-button
                        class="basis-1/2"
                        type="primary"
                        @click="submitLogin"
                        :loading="loading"
                    >
                        登录
                    </n-button>
                </div>
            </n-form>
        </div>
    </div>
</template>
