<script setup lang="jsx">
import { useRoute } from "vue-router";
import { NIcon } from "naive-ui";
import { Cog, Documents, People, CloudUpload } from "@vicons/ionicons5";
import { useUserStore } from "../stores/user";

const collapsed = inject("collapsed");
const route = useRoute();
const userStore = useUserStore();

const renderIcon = (icon) => () => <NIcon component={icon}></NIcon>;

const renderLabel = (title, to) => () =>
    <router-link to={{ name: to }}>{title}</router-link>;

const menuOptions = [
    {
        label: renderLabel("上传试卷", "upload"),
        icon: renderIcon(CloudUpload),
        key: "upload",
    },
    {
        label: renderLabel("试卷管理", "manage"),
        icon: renderIcon(Documents),
        key: "manage",
    },
];
if (userStore.admin) {
    menuOptions.push({
        label: renderLabel("用户管理", "user"),
        icon: renderIcon(People),
        key: "user",
    });
    menuOptions.push({
        label: renderLabel("系统管理", "system"),
        icon: renderIcon(Cog),
        key: "system",
    });
}
</script>

<template>
    <n-layout class="min-h-full pb-12">
        <n-layout-header bordered>
            <Header></Header>
        </n-layout-header>
        <n-layout class="admin-container" has-sider>
            <n-layout-sider
                bordered
                collapse-mode="width"
                :collapsed-width="64"
                :width="180"
                :collapsed="collapsed"
                class="h-full"
            >
                <n-scrollbar class="h-full">
                    <n-menu
                        :collapsed-width="64"
                        :collapsed="collapsed"
                        :collapsed-icon-size="22"
                        :value="route.name"
                        :options="menuOptions"
                    />
                </n-scrollbar>
            </n-layout-sider>
            <n-layout-content>
                <div class="mx-8 w-auto lg:mx-auto lg:w-[60vw] my-8">
                    <router-view />
                </div>
            </n-layout-content>
        </n-layout>
        <n-layout-footer bordered position="absolute">
            <Footer></Footer>
        </n-layout-footer>
    </n-layout>
</template>

<style scoped>
.admin-container {
    height: calc(100vh - 7rem);
}
</style>
