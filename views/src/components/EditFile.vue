<script setup lang="jsx">
import { file_types } from "../const";
import { message } from "../discrete";
import { ArrowUp, Checkmark, Close } from "@vicons/ionicons5";

const axios = inject("axios");
const props = defineProps(["pid"]);
const data = ref([]);
const Modify = reactive({
    delete: [],
    modify: [],
    new: [],
});

const UploadFile = reactive({
    url: null,
    key: null,
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
    Modify.modify = Modify.modify.filter((item) => item.fid != fid);
    Modify.new = Modify.new.filter((item) => item.fid != fid);
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

const ReOCR = (fid) => {
    axios.post("/manage/ocr/file", { fid: fid }).then((response) => {
        if (response.data.result === "success") {
            message.success("正在识别。");
        }
    });
};

const submit = async () => {
    for (let item of Modify.delete) {
        await axios.post("/manage/delete/file", { fid: item });
    }
    for (let item of Modify.modify) {
        await axios.post("/manage/edit/file", item);
    }
    for (let item of Modify.new) {
        await axios.post("/manage/edit/file", item);
        await axios.post("/manage/ocr/file", { fid: item.fid });
    }
};
defineExpose({ submit });

const renderStatus = (row) => {
    if (!row.status || row.status === 2)
        return <n-icon color="green" component={Checkmark}></n-icon>;
    else if (row.status === 0)
        return <n-icon color="blue" component={ArrowUp}></n-icon>;
    else return <n-icon color="red" component={Close}></n-icon>;
};

const tableColumns = [
    {
        title: "文件名",
        key: "name",
        render: (row) => (
            <div class="flex items-center gap-x-2">
                {renderStatus(row)}
                <div class="w-64 lg:w-auto">
                    <n-input
                        size="small"
                        value={row.name}
                        on-update:value={(val) =>
                            ModifyFile(row.fid, row.type, val)
                        }
                    ></n-input>
                </div>
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
        title: "OCR",
        key: "ocr",
        render: (row) => {
            return (
                <n-button
                    size="small"
                    strong
                    secondary
                    round
                    type="info"
                    on-click={() => ReOCR(row.fid)}
                >
                    重新识别
                </n-button>
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

const setUploadURL = async (options) => {
    return new Promise((resolve, reject) => {
        axios
            .post("/new/file", {
                name: options.file.name,
                pid: props.pid,
            })
            .catch(reject)
            .then((response) => {
                if (response.data.result == "success") {
                    data.value.push({
                        id: options.file.id,
                        fid: response.data.fid,
                        name: options.file.name,
                        type: 0,
                        key: response.data.key,
                        url: response.data.url,
                        obj: options.file,
                        status: 0,
                    });
                    UploadFile.url = response.data.url;
                    UploadFile.key = response.data.key;
                    resolve();
                }
                reject();
            });
    });
};

const setFinishUpload = (options) => {
    let object = data.value.find((item) => item.id == options.file.id);
    object.status = 2;
    Modify.new.push({
        fid: object.fid,
        name: object.name,
        type: object.type,
    });
};

const setFailedUpload = (options) => {
    data.value.find((item) => item.id == options.file.id).status = 1;
};

await fetchFiles();
</script>

<template>
    <n-data-table :columns="tableColumns" :data="data" :bordered="false" />
    <div class="flex justify-center my-3">
        <n-upload
            multiple
            directory-dnd
            :show-file-list="false"
            :action="UploadFile.url"
            :data="{ key: UploadFile.key, acl: 'private' }"
            :on-before-upload="setUploadURL"
            :on-finish="setFinishUpload"
            :on-error="setFailedUpload"
            class="!w-fit"
        >
            <n-button type="primary">上传文件</n-button>
        </n-upload>
    </div>
</template>
