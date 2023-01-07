<script setup>
import { Search } from "@vicons/ionicons5";
import { onMounted, ref, inject } from "vue";
import { useRouter } from "vue-router";
import Intro from "../components/Intro.vue";

const collapsed = inject("collapsed");
const router = useRouter();
const inputRef = ref(null);
const searchContent = ref(null);

onMounted(() => {
    inputRef.value.focus();
});

const goQuery = () => {
    router.push({
        name: "query",
        query: {
            s: searchContent.value,
        },
    });
};
</script>

<template>
    <div class="select-none pt-8 text-center font-black md:pt-14">
        <div class="gradient-title from-cyan-500 via-sky-600 to-blue-800">
            <div class="mb-2 text-4xl tracking-wider md:mb-4 md:text-6xl">
                世界领先的
            </div>
            <div class="text-5xl tracking-widest md:text-7xl">试卷分享平台</div>
        </div>
    </div>
    <div class="mt-8 flex justify-center md:mt-12">
        <div class="mx-8 flex items-center gap-x-4 md:mx-auto md:w-[40vw]">
            <span class="whitespace-nowrap md:text-lg">试卷</span>
            <n-input
                ref="inputRef"
                @keyup.enter="goQuery"
                v-model:value="searchContent"
                :size="collapsed ? 'medium' : 'large'"
                placeholder="搜索"
            >
                <template #prefix>
                    <n-icon :component="Search" />
                </template>
            </n-input>
            <n-button :size="collapsed ? 'medium' : 'large'" @click="goQuery"
                >检索</n-button
            >
        </div>
    </div>
    <div class="mx-8 mt-10 md:mt-16">
        <Intro />
    </div>
</template>
