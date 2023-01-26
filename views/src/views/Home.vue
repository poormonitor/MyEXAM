<script setup>
import { Search } from "@vicons/ionicons5";
import { useRouter } from "vue-router";

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
    <div class="select-none pt-16 text-center font-black md:pt-20">
        <div class="gradient-title from-cyan-500 via-sky-600 to-blue-800">
            <div class="mb-3 text-4xl md:text-6xl tracking-wider md:mb-5">
                世界领先的
            </div>
            <div class="text-5xl md:text-7xl tracking-widest">试卷分享平台</div>
        </div>
    </div>
    <div class="mt-14 flex justify-center md:mt-16">
        <div class="mx-8 flex items-center gap-x-4 md:mx-auto md:w-[40vw]">
            <span class="whitespace-nowrap md:text-lg">试卷</span>
            <n-input
                ref="inputRef"
                @keyup.enter="goQuery"
                v-model:value="searchContent"
                size="large"
                placeholder="搜索"
            >
                <template #prefix>
                    <n-icon :component="Search" />
                </template>
            </n-input>
            <n-button :size="collapsed ? 'medium' : 'large'" @click="goQuery">
                检索
            </n-button>
        </div>
    </div>
    <div class="mx-10 my-16 md:my-24">
        <Intro />
    </div>
</template>
