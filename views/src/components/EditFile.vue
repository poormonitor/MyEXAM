<script setup lang="jsx">
import { courses, file_types, grades, office_ext } from "../const";
import { message } from "../discrete";
import { ArrowUp, Checkmark, Close } from "@vicons/ionicons5";
import { GetYearMonth } from "../func";

const axios = inject("axios");
const props = defineProps(["pid"]);
const emits = defineEmits(["close"]);
const data = ref([]);
const showPDF = ref(false);
const Modify = reactive({
    delete: [],
    modify: [],
    new: [],
});

const ModifyData = inject("ModifyData");

const ExamFinalName = computed(() => {
    let data = ModifyData.value;
    let date = GetYearMonth(data.examgroup.date);
    let grade = grades[data.grade];
    let course = courses[data.course];
    return `${data.union.name} ${date} ${data.examgroup.name} ${grade} ${course}`;
});

const CurrentPaper = computed(() =>
    ModifyData.value.papers.find((item) => item.pid == props.pid)
);

const UploadFile = reactive({
    url: null,
    key: null,
});

const ApprovePaper = () => {
    axios.post("/manage/approve/paper", { pid: props.pid }).then((response) => {
        if (response.data.result === "success") {
            ModifyData.value.papers.find(
                (item) => item.pid == props.pid
            ).status = 2;
            emits("close");
        }
    });
};

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

const ReOCRFile = (fid) => {
    axios.post("/manage/ocr/file", { fid: fid }).then((response) => {
        if (response.data.result === "success") {
            message.success("正在识别。");
        }
    });
};

const ReOCRPaper = () => {
    axios.post("/manage/ocr/paper", { pid: props.pid }).then((response) => {
        if (response.data.result === "success") {
            message.success("正在识别。");
        }
    });
};

const PreviewData = ref({
    show: false,
    src: null,
    ext: "",
    title: "文件预览",
});

const PreviewFile = (fid, ext, name) => {
    axios
        .get("/list/url", {
            params: { fid: fid, download: false },
        })
        .then((response) => {
            if (response.data.url) {
                let file_url = response.data.url;
                PreviewData.value.src = office_ext.includes(ext)
                    ? "http://view.officeapps.live.com/op/view.aspx?src=" +
                      encodeURI(file_url)
                    : file_url;
                PreviewData.value.ext = ext;
                PreviewData.value.title = name;
                PreviewData.value.show = true;
            }
        });
};

const submit = () => {
    for (let item of Modify.delete) {
        axios.post("/manage/delete/file", { fid: item });
    }
    for (let item of Modify.modify) {
        axios.post("/manage/edit/file", item);
    }
    for (let item of Modify.new) {
        axios.post("/manage/edit/file", item);
        axios.post("/manage/ocr/file", { fid: item.fid });
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
        title: "预览",
        key: "preview",
        render: (row) => {
            return (
                <n-button
                    size="small"
                    strong
                    secondary
                    round
                    on-click={() => PreviewFile(row.fid, row.ext, row.name)}
                >
                    预览
                </n-button>
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
                    on-click={() => ReOCRFile(row.fid)}
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

const handlePDFUpload = async (file, name) => {
    axios
        .post("/new/file", {
            name: name,
            pid: props.pid,
        })
        .then((response) => {
            if (response.data.result == "success") {
                data.value.push({
                    fid: response.data.fid,
                    name: name,
                    type: 0,
                    key: response.data.key,
                    url: response.data.url,
                    status: 0,
                });
                postToS3(
                    file,
                    response.data.url,
                    response.data.key,
                    response.data.fid
                );
                showPDF.value = false;
            }
        });
};

const postToS3 = (file, url, key, fid) => {
    let formData = new FormData();
    formData.append("key", key);
    formData.append("acl", "private");
    formData.append("file", file);
    axios({
        baseURL: "",
        url: url,
        method: "post",
        data: formData,
    })
        .catch((error) => {
            uploadInfo.files.find((item) => item.fid == fid).status = 1;
        })
        .then((response) => {
            uploadInfo.files.find((item) => item.fid == fid).status = 2;
        });
};

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
    <Preview
        :src="PreviewData.src"
        :ext="PreviewData.ext"
        v-model:show="PreviewData.show"
        :title="PreviewData.title"
    />
    <PicPdf
        v-model:show="showPDF"
        :hint="ExamFinalName"
        :key="ExamFinalName"
        @confirm="handlePDFUpload"
    />
    <n-data-table :columns="tableColumns" :data="data" :bordered="false" />
    <div class="flex flex-wrap justify-center gap-x-2 my-3">
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
            <n-button>上传文件</n-button>
        </n-upload>
        <n-button @click="showPDF = true" type="info"> 图片生成PDF </n-button>
        <n-button type="info" secondary @click="ReOCRPaper"> 重新OCR </n-button>
        <n-button
            type="primary"
            v-if="CurrentPaper.status === 1"
            @click="ApprovePaper"
        >
            审核通过
        </n-button>
    </div>
</template>
