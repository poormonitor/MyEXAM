<script setup lang="jsx">
import { GetFullTime } from "../func";
import { file_types } from "../const";
import { OpenOutline, CloudDownloadOutline } from "@vicons/ionicons5";

const props = defineProps(["pid", "data"]);
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
                type="info"
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
        title: "上传时间",
        key: "upload_time",
        render: (row) => <span>{GetFullTime(row.upload_time)}</span>,
        cellProps: cellProps,
    },
    {
        title: "下载量",
        key: "views",
        cellProps: cellProps,
    },
    {
        title: "类型",
        key: "type",
        render: (row) => <span>{file_types[row.type]}</span>,
        cellProps: cellProps,
    },
];

const data = props.data
    ? props.data
    : await axios
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
