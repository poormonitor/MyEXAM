<script setup>
import { Search } from "@vicons/ionicons5";
import { useRouter } from "vue-router";

const collapsed = inject("collapsed");
const axios = inject("axios");
const router = useRouter();
const inputRef = ref(null);
const searchContent = ref(null);

const StaColumns = [
    { name: "联盟", key: "union", unit: "个" },
    { name: "联考", key: "examgroup", unit: "场" },
    { name: "考试", key: "exam", unit: "场" },
    { name: "试卷", key: "paper", unit: "张" },
    { name: "文件", key: "file", unit: "个" },
];
const ObjectCnt = ref({
    union: 0,
    examgroup: 0,
    exam: 0,
    paper: 0,
    file: 0,
});

const FetchApiSta = () => {
    axios.get("/list/statistic").then((response) => {
        if (response.data) {
            ObjectCnt.value = response.data;
        }
    });
};

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
FetchApiSta();
</script>

<template>
    <div class="select-none pt-16 text-center font-black md:pt-20">
        <div class="gradient-title from-cyan-500 via-sky-600 to-blue-800">
            <div class="text-4xl md:text-6xl tracking-wider">
                试卷分享平台
            </div>
            <div class="text-5xl md:text-7xl !leading-[1.2]">MyExam</div>
        </div>
    </div>
    <div class="mt-8 flex justify-center md:mt-12">
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
    <div class="mx-8 w-auto lg:mx-auto lg:w-[70vw] my-20 md:my-24">
        <n-card class="mb-12">
            <template #header>
                <p>当前系统内共有</p>
            </template> 
            <div class="grid grid-cols-3 md:grid-cols-5">
                <n-statistic
                    :label="column.name"
                    tabular-nums
                    v-for="column in StaColumns"
                >
                    <n-number-animation :from="0" :to="ObjectCnt[column.key]" />
                    <template #suffix> {{ column.unit }} </template>
                </n-statistic>
            </div>
        </n-card>
        <Intro />
    </div>
</template>
