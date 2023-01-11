<script setup>
import { useUserStore } from "../stores/user";
import { useRouter } from "vue-router";
import sha256 from "crypto-js/sha256";
import { message } from "../discrete";

const userStore = useUserStore();
const router = useRouter();
const axios = inject("axios");
const form = ref(null);

const regForm = reactive({
    email: "",
    nick: "",
    passwd: "",
    repeat: "",
});

const submitReg = () => {
    form.value
        .validate()
        .catch((error) => {})
        .then(() => {
            axios
                .post("/user/reg", {
                    email: regForm.email,
                    nick: regForm.nick,
                    password: sha256(regForm.passwd).toString(),
                })
                .then((response) => {
                    if (response.data.result === "success") {
                        message.success("注册成功。");
                        router.push({ name: "login" });
                    } else {
                        message.error(response.data.detail);
                    }
                });
        });
};

const rules = {
    email: [
        {
            required: true,
            validator: (rule, value) =>
                /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/.test(value),
            message: "请检查邮箱格式是否正确",
            trigger: ["input", "blur"],
        },
    ],
    nick: [
        {
            required: true,
            message: "请输入昵称",
            trigger: ["input", "blur"],
        },
    ],
    passwd: [
        {
            required: true,
            validator: (rule, value) => {
                return /^(?=.*\d)(?=.*[a-zA-Z]).{6,20}$/.test(value);
            },
            message: "密码应该同时包括字母、数字，且长6-20字符",
            trigger: ["input", "blur"],
        },
    ],
    repeat: [
        {
            required: true,
            validator: (rule, value) => value === regForm.passwd,
            message: "两次输入的密码不一致",
            trigger: ["input", "blur"],
        },
    ],
};
</script>

<template>
    <div class="mx-8 w-auto md:mx-auto md:w-[60vw] lg:w-[40vw] mt-12">
        <div class="border px-8 md:px-20 py-12 rounded-2xl">
            <p class="text-lg text-indigo-600 mb-2">欢迎使用 MyEXAM</p>
            <p class="text-4xl font-bold">注册</p>
            <n-form
                ref="form"
                size="large"
                class="mt-10"
                :model="regForm"
                :rules="rules"
            >
                <n-form-item label="邮箱" path="email">
                    <n-input
                        :input-props="{ autocomplete: 'email' }"
                        v-model:value="regForm.email"
                    ></n-input>
                </n-form-item>
                <n-form-item label="昵称" path="nick">
                    <n-input
                        :input-props="{ autocomplete: 'nick' }"
                        v-model:value="regForm.nick"
                    ></n-input>
                </n-form-item>
                <n-form-item label="密码" path="passwd">
                    <n-input
                        :input-props="{ autocomplete: 'new-password' }"
                        type="password"
                        v-model:value="regForm.passwd"
                    ></n-input>
                </n-form-item>
                <n-form-item label="重复密码" path="repeat">
                    <n-input
                        :input-props="{ autocomplete: 'new-password' }"
                        type="password"
                        v-model:value="regForm.repeat"
                    ></n-input>
                </n-form-item>
                <div class="flex justify-center">
                    <span>
                        已有账号？去
                        <router-link
                            class="text-blue-500 hover:text-blue-700"
                            :to="{ name: 'login' }"
                        >
                            登录
                        </router-link>
                    </span>
                </div>
                <div class="flex gap-x-4 justify-center mt-4">
                    <n-button
                        class="basis-1/2"
                        type="primary"
                        @click="submitReg"
                        >注册</n-button
                    >
                </div>
            </n-form>
        </div>
    </div>
</template>
