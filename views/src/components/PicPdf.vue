<script setup>
import { jsPDF } from "jspdf";
import Preview from "./Preview.vue";

const props = defineProps(["show", "hint"]);
const emits = defineEmits(["update:show", "confirm"]);
const picList = ref([]);
const fileName = ref(props.hint ? props.hint.replaceAll(" ", "_") : "");
const previewImage = reactive({ url: "", name: "" });
const showPreviewPic = ref(false);
const showPreviewPDF = ref(false);
const PdfUri = ref(null);
var PdfFile = null;

const handlePreview = (file) => {
    const { url, name } = file;
    previewImage.url = url;
    previewImage.name = name;
    showPreviewPic.value = true;
};

const handleUpload = (options) => {
    createPDF();
    options.onFinish();
};

function getBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = (error) => reject(error);
    });
}

function getImageSize(data) {
    return new Promise((resolve, reject) => {
        let image = new Image();
        image.src = data;
        image.onload = () => {
            resolve([image.width, image.height]);
        };
        image.onerror = reject;
    });
}

const createPDF = async () => {
    const PDF = new jsPDF("p", "cm", "a4");
    let data, size;
    for (let i = 0; i < picList.value.length; i++) {
        if (i) PDF.addPage("a4");
        data = await getBase64(picList.value[i].file);
        size = await getImageSize(data);
        PDF.addImage(data, "JPEG", 0, 0, 21, (21 * size[1]) / size[0]);
    }
    PdfUri.value = PDF.output("bloburi");
    PdfFile = PDF.output("blob");
};

const handleConfirm = () => {
    PdfFile = null;
    fileName.value = props.hint ? props.hint.replaceAll(" ", "_") : "";
    picList.value = [];
    emits("confirm", PdfFile, fileName.value + ".pdf");
};
</script>

<template>
    <Preview v-model:show="showPreviewPDF" title="PDF预览" :src="PdfUri" />
    <n-modal
        v-model:show="showPreviewPic"
        preset="card"
        :title="previewImage.name"
    >
        <img :src="previewImage.url" style="width: 100%" />
    </n-modal>
    <n-drawer
        :show="props.show"
        :on-update:show="(val) => emits('update:show', val)"
        @preview="handlePreview"
        width="max(350px, 50%)"
    >
        <n-drawer-content class="h-full" title="使用图片生成PDF">
            <n-form class="mx-8 my-6">
                <n-form-item label="文件名称">
                    <n-input v-model:value="fileName">
                        <template #suffix> .pdf </template>
                    </n-input>
                </n-form-item>
                <n-form-item label="选择图片">
                    <n-upload
                        list-type="image-card"
                        v-model:file-list="picList"
                        accept="image/*"
                        :custom-request="handleUpload"
                        multiple
                    >
                        点击上传
                    </n-upload>
                </n-form-item>
            </n-form>
            <div class="absolute bottom-4 right-4 flex gap-x-4">
                <n-button
                    @click="
                        props.show = false;
                        emits('update:show', false);
                    "
                    >取消</n-button
                >
                <n-button
                    @click="showPreviewPDF = true"
                    :disabled="picList.length == 0"
                    >预览PDF</n-button
                >
                <n-button
                    type="primary"
                    :disabled="picList.length == 0"
                    @click="handleConfirm"
                    >确认上传</n-button
                >
            </div>
        </n-drawer-content>
    </n-drawer>
</template>
