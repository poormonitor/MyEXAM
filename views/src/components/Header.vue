<script setup lang="jsx">
import { NIcon } from "naive-ui";
import { useRoute, RouterLink } from "vue-router";
import {
    School,
    CloudUpload,
    AppsOutline,
    NavigateCircle,
} from "@vicons/ionicons5";
import { inject } from "vue";

const route = useRoute();

const collapsed = inject("collapsed");

const renderLabel = (icon, target, label) => {
    return () => (
        <div class="flex items-center gap-x-1.5">
            <NIcon size="0.9rem">{() => h(icon)}</NIcon>
            <RouterLink class="text-[0.9rem]" to={{ name: target }}>
                {label}
            </RouterLink>
        </div>
    );
};

const menuOptions = [
    {
        label: renderLabel(School, "query", "搜试卷"),
        key: "query",
    },
    {
        label: renderLabel(CloudUpload, "upload", "传试卷"),
        key: "upload",
    },
    {
        label: renderLabel(NavigateCircle, "discover", "探索"),
        key: "discover",
    },
];
</script>

<template>
    <div class="px-6 py-3 md:pt-2 md:pb-1 flex items-baseline" id="main-header">
        <div class="select-none flex items-baseline md:mr-4">
            <router-link
                :to="{ name: 'home' }"
                class="font-sans text-2xl font-bold gradient-title from-indigo-600 via-violet-500 to-purple-400"
            >
                MyExam
            </router-link>
        </div>
        <n-menu
            :value="route.name"
            v-if="!collapsed"
            mode="horizontal"
            :options="menuOptions"
        />
        <div class="flex flex-grow justify-end">
            <n-dropdown size="large" :options="menuOptions" v-if="collapsed">
                <n-button>
                    <n-icon size="1rem"><AppsOutline /></n-icon>
                </n-button>
            </n-dropdown>
        </div>
    </div>
</template>
