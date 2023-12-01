<script setup lang="jsx">
import { useRoute } from "vue-router";

const route = useRoute();

const currentTab = ref("0");
if (route.query.t) currentTab.value = route.query.t;
</script>

<template>
    <div class="mt-8 flex flex-col items-center md:mt-10 pb-12">
        <n-tabs type="segment" v-model:value="currentTab">
            <n-tab-pane name="0" tab="搜索考试">
                <QueryExam />
            </n-tab-pane>
            <n-tab-pane name="1" tab="搜索文件">
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
