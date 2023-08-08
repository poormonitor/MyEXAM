<script setup>
import { message } from "../discrete";
import sha256 from "crypto-js/sha256";

const axios = inject("axios");
const props = defineProps(["show", "uid"]);
const emits = defineEmits(["update:show", "finish"]);
const form = ref(null);
const visible = computed({
    get() {
        return props.show;
    },
    set(value) {
        emits("update:show", value);
    },
});

const newUser = reactive({
    nick: "",
    email: "",
    password: "",
});

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
    password: [
        {
            required: true,
            validator: (rule, value) => {
                return /^(?=.*\d)(?=.*[a-zA-Z]).{6,20}$/.test(value);
            },
            message: "密码应该同时包括字母、数字，且长6-20字符",
            trigger: ["input", "blur"],
        },
    ],
};

const submitRequest = () => {
    form.value
        .validate()
        .catch((error) => {})
        .then(() => {
            axios
                .post("/users/new", {
                    email: newUser.email,
                    nick: newUser.nick,
                    password: sha256(newUser.password).toString(),
                })
                .then((response) => {
                    if (response.data.result == "success") {
                        visible.value = false;
                        message.success("用户添加成功。");
                        emits("finish");
                    }
                });
        });
};
</script>

<template>
    <n-modal
        v-model:show="visible"
        title="添加用户"
        preset="dialog"
        positive-text="确认"
        negative-text="取消"
        class="w-4/5 md:3/5 lg:w-2/5"
        @positive-click="submitRequest"
    >
        <n-form :rules="rules" :model="newUser" ref="form" autocomplete="off">
            <div class="mx-8 mb-6 mt-10">
                <n-form-item label="邮箱" path="email">
                    <n-input placeholder="邮箱" v-model:value="newUser.email">
                    </n-input>
                </n-form-item>
                <n-form-item label="昵称" path="nick">
                    <n-input placeholder="昵称" v-model:value="newUser.nick">
                    </n-input>
                </n-form-item>
                <n-form-item label="密码" path="password">
                    <n-input
                        placeholder="密码"
                        v-model:value="newUser.password"
                        type="password"
                        :input-props="{ autocomplete: 'new-password' }"
                    >
                    </n-input>
                </n-form-item>
            </div>
        </n-form>
    </n-modal>
</template>
