<script setup>
import { useUserStore } from "../stores/user";
import { useRouter } from "vue-router";
import sha256 from "crypto-js/sha256";
import { message } from "../discrete";

const userStore = useUserStore();
const router = useRouter();
const axios = inject("axios");

const loginForm = reactive({
    email: "",
    passwd: "",
});

const submitLogin = () => {
    axios
        .post("/user/login", {
            email: loginForm.email,
            password: sha256(loginForm.passwd).toString(),
        })
        .then((response) => {
            if (response.data.access_token) {
                userStore.login(
                    response.data.uid,
                    response.data.nick,
                    response.data.access_token,
                    response.data.admin
                );
                router.push({ name: "home" });
            } else {
                message.error(response.data.detail);
            }
        });
};
</script>

<template>
    <div class="mx-8 w-auto md:mx-auto md:w-[60vw] lg:w-[40vw] mt-20">
        <div class="border px-8 md:px-20 py-12 rounded-2xl">
            <p class="text-lg text-indigo-600 mb-2">欢迎使用 MyEXAM</p>
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
                <div class="flex justify-center">
                    <span>
                        没有账号？去
                        <router-link
                            class="text-blue-500 hover:text-blue-700"
                            :to="{ name: 'reg' }"
                        >
                            注册
                        </router-link>
                    </span>
                </div>
                <div class="flex gap-x-4 justify-center mt-4">
                    <n-button
                        class="basis-1/2"
                        type="primary"
                        @click="submitLogin"
                    >
                        登录
                    </n-button>
                </div>
            </n-form>
        </div>
    </div>
</template>
