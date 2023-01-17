<script setup lang="jsx">
import { file_types } from "../const";

const axios = inject("axios");
const props = defineProps(["pid"]);
const data = ref([]);
const Modify = reactive({
    delete: [],
    modify: [],
});

const fetchFiles = async () => {
    await axios
        .get("/list/files", { params: { pid: props.pid } })
        .then((response) => {
            if (response.data.list) {
                data.value = response.data.list;
                return true;
            }
        });
};

const RemoveFile = (fid) => {
    data.value = data.value.filter((item) => item.fid !== fid);
    Modify.delete.push(fid);
};

const ModifyFile = (fid, type, name) => {
    data.value.find((item) => item.fid === fid).name = name;
    data.value.find((item) => item.fid === fid).type = type;
    let target = Modify.modify.find((item) => item.fid == fid);
    if (target) {
        target.type = type;
        target.name = name;
    } else {
        Modify.modify.push({ fid: fid, type: type, name: name });
    }
};

const submit = async () => {
    for (let item of Modify.delete) {
        await axios.post("/manage/delete/file", { fid: item });
    }
    for (let item of Modify.modify) {
        await axios.post("/manage/edit/file", item);
    }
};
defineExpose({ submit });

const tableColumns = [
    {
        title: "文件名",
        key: "name",
        render: (row) => (
            <div class="w-64 lg:w-auto">
                <n-input
                    size="small"
                    value={row.name}
                    on-update:value={(val) =>
                        ModifyFile(row.fid, row.type, val)
                    }
                ></n-input>
            </div>
        ),
    },
    {
        title: "类型",
        key: "type",
        render: (row) => {
            return (
                <n-radio-group
                    size="small"
                    value={row.type}
                    on-update:value={(val) =>
                        ModifyFile(row.fid, val, row.name)
                    }
                >
                    {file_types.map((item, index) => (
                        <n-radio-button value={index} label={item} />
                    ))}
                </n-radio-group>
            );
        },
    },
    {
        title: "删除",
        key: "delete",
        render: (row) => (
            <n-popconfirm on-positive-click={() => RemoveFile(row.fid)}>
                {{
                    trigger: () => (
                        <n-button
                            size="small"
                            strong
                            secondary
                            round
                            type="error"
                        >
                            删除
                        </n-button>
                    ),
                    default: () => "你确认要删除吗？",
                }}
            </n-popconfirm>
        ),
    },
];

await fetchFiles();
</script>

<template>
    <n-data-table :columns="tableColumns" :data="data" :bordered="false" />
</template>
