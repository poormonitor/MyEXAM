<script setup>
import { pic_ext } from "../const";

const props = defineProps(["src", "title", "ext"]);

const pdf = computed(() => props.ext === "pdf");
const pic = computed(() => pic_ext.includes(props.ext));
const title = computed(() => (props.title ? props.title : "文件预览"));
</script>

<template>
    <n-modal preset="card" class="preview-modal !my-8" :title="title">
        <embed
            class="w-full h-[80vh]"
            type="application/pdf"
            :src="props.src"
            v-if="pdf"
        />
        <img :src="props.src" class="!w-full" v-else-if="pic" />
        <iframe class="w-full h-[80vh]" :src="props.src" v-else></iframe>
    </n-modal>
</template>

<style>
.preview-modal {
    width: max(300px, 60%) !important;
}
</style>
