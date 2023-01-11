<script setup lang="jsx">
import { useUserStore } from "../stores/user";
import { useRouter, useRoute } from "vue-router";
import {
    CaretDown,
    LockClosedOutline,
    ExitOutline,
    SettingsOutline,
} from "@vicons/ionicons5";
import PasswordSetter from "./PasswordSetter.vue";

const userStore = useUserStore();
const router = useRouter();
const route = useRoute();

const showPasswd = ref(false);

const renderIcon = (icon) => <n-icon component={icon}></n-icon>;

const optionsLogged = [
    {
        label: "修改密码",
        key: "pw",
        icon: () => renderIcon(LockClosedOutline),
        target: () => {
            showPasswd.value = true;
        },
    },
    {
        label: "退出登录",
        key: "logout",
        icon: () => renderIcon(ExitOutline),
        target: () => {
            userStore.logout();
            router.push({ name: "home" });
        },
    },
];

const optionsAdmin = [
    { type: "divider", key: "d1" },
    {
        label: "后台管理",
        key: "admin",
        icon: () => renderIcon(SettingsOutline),
        target: () => {
            router.push({ name: "admin" });
        },
    },
];

const option = computed(() =>
    userStore.admin ? optionsLogged.concat(optionsAdmin) : optionsLogged
);

const user = computed(() => (userStore.uid ? userStore.nick : "登录"));

const handleSelect = (key) => {
    option.value.find((item) => item.key == key).target();
};
</script>

<template>
    <PasswordSetter v-model:show="showPasswd" />
    <n-button
        v-if="!userStore.uid"
        @click="router.push({ name: 'login' })"
        quaternary
    >
        登录
    </n-button>
    <n-dropdown trigger="hover" :options="option" @select="handleSelect" v-else>
        <div class="flex items-center gap-x-1 hover:text-green-600 transition">
            <span>{{ user }}</span>
            <n-icon size="0.7rem" :component="CaretDown"></n-icon>
        </div>
    </n-dropdown>
</template>
