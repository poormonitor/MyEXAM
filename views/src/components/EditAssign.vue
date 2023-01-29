<script setup lang="jsx">
import { ArrowUp, Checkmark, Close } from "@vicons/ionicons5";
import { blobToHash } from "../func";

const axios = inject("axios");
const props = defineProps(["egid"]);
const emits = defineEmits(["close"]);
const data = ref([]);
const Modify = reactive({
    delete: [],
    modify: [],
});

const fetchAssigns = async () => {
    await axios
        .get("/list/assigns", { params: { egid: props.egid } })
        .then((response) => {
            if (response.data.list) {
                data.value = response.data.list;
                return true;
            }
        });
};

const RemoveAssign = (aid) => {
    data.value = data.value.filter((item) => item.aid !== aid);
    Modify.delete.push(aid);
    Modify.modify = Modify.modify.filter((item) => item.aid != aid);
};

const ModifyAssign = (aid, comment) => {
    let object = data.value.find((item) => item.aid === aid);
    object.comment = comment;

    let target = Modify.modify.find((item) => item.aid == aid);
    if (target) {
        target.comment = comment;
    } else {
        Modify.modify.push({ aid: aid, comment: comment });
    }
};

const PreviewData = ref({
    show: false,
    src: null,
    ext: "",
    title: "文件预览",
});

const PreviewAssign = (aid, ext, name) => {
    axios
        .get("/list/assign_url", {
            params: { aid: aid },
        })
        .then((response) => {
            if (response.data.url) {
                PreviewData.value.src = response.data.url;
                PreviewData.value.ext = ext;
                PreviewData.value.title = name;
                PreviewData.value.show = true;
            }
        });
};

const submit = () => {
    for (let item of Modify.delete) {
        axios.post("/manage/delete/assign", { aid: item });
    }
    for (let item of Modify.modify) {
        axios.post("/manage/edit/assign", { egid: props.egid, ...item });
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
        title: "备注",
        key: "comment",
        render: (row) => (
            <div class="flex items-center gap-x-2">
                {renderStatus(row)}
                <n-input
                    size="small"
                    value={row.comment}
                    on-update:value={(val) => ModifyAssign(row.aid, val)}
                ></n-input>
            </div>
        ),
    },
    {
        title: "预览",
        key: "preview",
        render: (row) => {
            return (
                <n-button
                    size="small"
                    strong
                    secondary
                    round
                    on-click={() =>
                        PreviewAssign(row.aid, row.ext, row.comment)
                    }
                >
                    预览
                </n-button>
            );
        },
    },
    {
        title: "删除",
        key: "delete",
        render: (row) => (
            <n-popconfirm on-positive-click={() => RemoveAssign(row.aid)}>
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

const UploadToS3 = (options, url, key, suc, err) => {
    let formData = new FormData();
    formData.append("key", key);
    formData.append("acl", "private");
    formData.append("file", options.file.file);
    axios({
        baseURL: "",
        url: url,
        method: "post",
        data: formData,
    })
        .catch(() => err(options))
        .then(() => suc(options));
};

const CustomUpload = async (options) => {
    let name = options.file.name.split(".");
    data.value.push({
        id: options.file.id,
        comment: name[0],
        type: 0,
        status: 0,
    });
    axios
        .post("/new/assign", {
            ext: name.pop(),
            md5: await blobToHash(options.file.file),
        })
        .catch(() => SetFailedUpload(options))
        .then((response) => {
            let object = data.value.find((item) => item.id == options.file.id);
            object.aid = response.data.aid;
            if (response.data.result == "success") {
                UploadToS3(
                    options,
                    response.data.url,
                    response.data.key,
                    SetFinishUpload,
                    SetFailedUpload
                );
            } else if (response.data.result == "exists") {
                SetFinishUpload(options);
            }
        });
};

const SetFinishUpload = (options) => {
    let object = data.value.find((item) => item.id == options.file.id);
    object.status = 2;
    Modify.modify.push({
        aid: object.aid,
        comment: object.comment,
    });
    options.onFinish();
};

const SetFailedUpload = (options) => {
    data.value.find((item) => item.id == options.file.id).status = 1;
    options.onError();
};

await fetchAssigns();
</script>

<template>
    <Preview
        :src="PreviewData.src"
        :ext="PreviewData.ext"
        v-model:show="PreviewData.show"
        :title="PreviewData.title"
    />
    <n-data-table
        class="assign-table"
        :columns="tableColumns"
        :data="data"
        :bordered="false"
    />
    <div class="flex flex-wrap justify-center gap-x-2 gap-y-1 mt-2 mb-3">
        <n-upload
            multiple
            directory-dnd
            :show-file-list="false"
            :custom-request="CustomUpload"
            class="!w-fit"
        >
            <n-button size="small">上传赋分表</n-button>
        </n-upload>
    </div>
</template>

<style>
.assign-table .n-data-table-empty {
    --n-empty-padding: 24px 0;
}
</style>
