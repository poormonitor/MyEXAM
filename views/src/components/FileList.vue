<script setup lang="jsx">
import { GetFullTime } from "../func";
import { file_types } from "../const";
import { OpenOutline } from "@vicons/ionicons5";

const props = defineProps(["data"]);
const emits = defineEmits(["preview"]);
const axios = inject("axios");

const downloadFile = (fid) => {
    axios
        .get("/list/url", {
            params: { fid: fid },
        })
        .then((response) => {
            if (response.data.url) {
                axios
                    .get(response.data.url, { responseType: "blob" })
                    .then((res) => {
                        const blob = new Blob([res.data], {
                            type: res.headers["content-type"],
                        });
                        const url = URL.createObjectURL(blob);

                        const a = document.createElement("a");
                        a.href = url;
                        a.download = response.data.filename;
                        a.click();

                        URL.revokeObjectURL(url);
                    });
            }
        });
};

const cellProps = (row) => {
    return {
        class: "cursor-pointer",
        onClick: () => downloadFile(row.fid),
    };
};

const columns = [
    {
        title: "预览",
        key: "preview",
        render: (row) => (
            <n-button
                type="error"
                size="small"
                secondary
                on-click={() => emits("preview", row.fid, row.ext, row.name)}
            >
                {{
                    icon: () => <n-icon component={OpenOutline}></n-icon>,
                }}
            </n-button>
        ),
    },
    {
        title: "文件名",
        key: "name",
        render: (row) => <span class="lg:whitespace-normal">{row.name}</span>,
        cellProps: cellProps,
    },
    {
        title: "类型",
        key: "type",
        render: (row) => <span>{file_types[row.type]}</span>,
        cellProps: cellProps,
    },
    {
        title: "下载量",
        key: "views",
        cellProps: cellProps,
    },
    {
        title: "上传时间",
        key: "upload_time",
        render: (row) => <span>{GetFullTime(row.upload_time)}</span>,
        cellProps: cellProps,
    },
];
</script>

<template>
    <n-data-table
        class="whitespace-nowrap"
        size="small"
        :columns="columns"
        :data="props.data"
    />
</template>
