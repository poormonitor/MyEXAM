<script setup lang="jsx">
import { GetFullTime } from "../func";
import { file_types } from "../const";

const props = defineProps(["pid"]);
const emits = defineEmits(["preview"]);
const axios = inject("axios");

const downloadFile = (fid) => {
    axios
        .get("/list/url", {
            params: { fid: fid },
        })
        .then((response) => {
            if (response.data.url) {
                window.open(response.data.url);
            }
        });
};

const columns = [
    {
        title: "链接",
        key: "download",
        render: (row) => (
            <n-button
                type="primary"
                size="small"
                secondary
                on-click={() => downloadFile(row.fid)}
            >
                下载
            </n-button>
        ),
    },
    {
        title: "预览",
        key: "preview",
        render: (row) => (
            <n-button
                type="info"
                size="small"
                secondary
                on-click={() => emits("preview", row.fid, row.ext, row.name)}
            >
                预览
            </n-button>
        ),
    },
    { title: "文件名", key: "name" },
    {
        title: "上传时间",
        key: "upload_time",
        render: (row) => <span>{GetFullTime(row.upload_time)}</span>,
    },
    {
        title: "下载量",
        key: "views",
    },
    {
        title: "类型",
        key: "type",
        render: (row) => <span>{file_types[row.type]}</span>,
    },
];

const data = await axios
    .get("/list/files", { params: { pid: props.pid } })
    .then((response) => {
        if (response.data.list) return response.data.list;
    });
</script>

<template>
    <n-data-table
        class="whitespace-nowrap"
        size="small"
        :columns="columns"
        :data="data"
    />
</template>
