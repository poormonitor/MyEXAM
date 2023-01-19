<script setup lang="jsx">
import { useRoute, useRouter } from "vue-router";
import { watch } from "vue";

const route = useRoute();
const router = useRouter();

const currentTab = ref("exam");

if (route.query.type && ["exam", "file"].includes(route.query.type))
    currentTab.value = route.query.type;

watch(currentTab, (val) => {
    router.push({ query: { type: val, ...route.query } });
});
</script>

<template>
    <div class="mt-8 flex flex-col items-center md:mt-10">
        <n-tabs type="segment" v-model:value="currentTab">
            <n-tab-pane name="exam" tab="搜索考试">
                <QueryExam />
            </n-tab-pane>
            <n-tab-pane name="file" tab="搜索文件">
                <QueryFile />
            </n-tab-pane>
        </n-tabs>
    </div>
</template>

<style lang="postcss">
.n-tabs-nav {
    @apply justify-center mb-1;
}

.n-tabs-rail {
    @apply w-64 !important;
}

.paperTable tr:hover td {
    @apply bg-blue-50;
}
</style>
