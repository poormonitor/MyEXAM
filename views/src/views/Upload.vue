<script setup lang="jsx">
import { Archive } from "@vicons/ionicons5";
import { courses, grades, file_types, paper_types } from "../const";
import { getYearMonth } from "../func";
import { AddCircleOutline } from "@vicons/ionicons5";
import { useDialog } from "naive-ui";
import { message } from "../discrete";

const dialog = useDialog();
const axios = inject("axios");
const showPDF = ref(false);
const confirming = ref(false);
const unionList = ref([]);
const examGroupList = ref([]);
const newUnionForm = reactive({ name: "", member: "" });
const newExamGroupForm = reactive({ name: "", date: Date.now() });
const uploadFile = reactive({
    url: null,
    key: null,
});

const uploadInfo = reactive({
    nid: null,
    egid: null,
    eid: null,
    pid: null,
    comment: "",
    files: [],
    date: Date.now(),
    grade: 2,
    course: 0,
});

const getOptions = (items) =>
    items.map((item, index) => ({
        label: item,
        value: index,
    }));

const fetchUnions = () => {
    axios.get("/list/unions").then((response) => {
        unionList.value = response.data.list.map((item) => ({
            label: item.name,
            value: item.nid,
        }));
        unionList.value.push({
            label: "",
            value: "new",
        });
    });
};

const fetchExamGroups = () => {
    axios
        .get("/list/union", {
            params: {
                nid: uploadInfo.nid,
            },
        })
        .then((response) => {
            if (response.data.union) {
                examGroupList.value = response.data.union.examgroups.map(
                    (item) => ({
                        label: getYearMonth(item.date) + " " + item.name,
                        value: item.egid,
                        date: item.date,
                    })
                );
                examGroupList.value.push({
                    label: "",
                    value: "new",
                });
            }
        });
};

const renderLabel = (option) =>
    option.value === "new" ? (
        <div class="flex items-center gap-x-2">
            <n-icon>
                <AddCircleOutline />
            </n-icon>
            创建新的
        </div>
    ) : (
        <span>{option.label}</span>
    );

const createNewUnion = async () => {
    uploadInfo.nid = await axios
        .post("/new/union", {
            name: newUnionForm.name,
            member: newUnionForm.member,
        })
        .then((response) => {
            if (response.data.result == "success") return response.data.nid;
        });
};

const createNewExamGroup = async () => {
    uploadInfo.egid = await axios
        .post("/new/examgroup", {
            name: newExamGroupForm.name,
            date: newExamGroupForm.date,
            nid: uploadInfo.nid,
        })
        .then((response) => {
            if (response.data.result == "success") return response.data.egid;
        });
};

const createNewExam = async () => {
    uploadInfo.eid = await axios
        .post("/new/exam", {
            egid: uploadInfo.egid,
            course: uploadInfo.course,
            grade: uploadInfo.grade,
            date: uploadInfo.date,
        })
        .then((response) => {
            if (response.data.eid) return response.data.eid;
        });
};

const createNewPaper = async () => {
    uploadInfo.pid = await axios.post("/new/paper").then((response) => {
        if (response.data.pid) return response.data.pid;
    });
};

const newUnionDialog = () => {
    dialog.info({
        title: "创建新联盟",
        positiveText: "确定",
        maskClosable: false,
        icon: () => (
            <n-icon size="1.5rem">
                <AddCircleOutline />
            </n-icon>
        ),
        content: () => (
            <div class="mx-6 my-10">
                <n-form>
                    <n-form-item label="联盟名称">
                        <n-input v-model:value={newUnionForm.name}></n-input>
                    </n-form-item>
                    <n-form-item label="成员">
                        <n-input
                            v-model:value={newUnionForm.member}
                            type="textarea"
                        ></n-input>
                    </n-form-item>
                </n-form>
            </div>
        ),
        onPositiveClick: () => {
            return new Promise((resolve, reject) => {
                unionList.value = unionList.value.filter(
                    (item) => item.value != "create"
                );
                unionList.value.splice(-2, 0, {
                    label: newUnionForm.name,
                    value: "create",
                });
                uploadInfo.nid = "create";
                resolve();
            });
        },
        onClose: () => {
            uploadInfo.nid = null;
        },
    });
};

const newExamGroupDialog = () => {
    if (!uploadInfo.nid || uploadInfo.nid === "new") {
        message.error("请先选择联盟");
    }
    dialog.info({
        title: "创建新测试",
        positiveText: "确定",
        maskClosable: false,
        icon: () => (
            <n-icon size="1.5rem">
                <AddCircleOutline />
            </n-icon>
        ),
        content: () => (
            <div class="mx-6 my-8">
                <n-form>
                    <n-form-item label="考试名称">
                        <n-input
                            v-model:value={newExamGroupForm.name}
                        ></n-input>
                    </n-form-item>
                    <n-form-item label="考试年月">
                        <n-date-picker
                            type="month"
                            v-model:value={newExamGroupForm.date}
                            is-date-disabled={disablePreviousDate}
                        ></n-date-picker>
                    </n-form-item>
                </n-form>
                <div v-if={newExamGroupForm.name}>
                    <p class="text-sky-800 text-sm">您即将创建</p>
                    <p class="text-lg">
                        {unionList.value.find(
                            (item) => item.value == uploadInfo.nid
                        ).label +
                            " " +
                            getYearMonth(newExamGroupForm.date) +
                            " " +
                            newExamGroupForm.name}
                    </p>
                </div>
            </div>
        ),
        onPositiveClick: () => {
            return new Promise((resolve, reject) => {
                examGroupList.value = examGroupList.value.filter(
                    (item) => item.value != "create"
                );
                examGroupList.value.splice(-2, 0, {
                    label:
                        getYearMonth(newExamGroupForm.date) +
                        " " +
                        newExamGroupForm.name,
                    value: "create",
                    date: newExamGroupForm.date,
                });
                uploadInfo.egid = "create";
                resolve();
            });
        },
        onClose: () => {
            uploadInfo.egid = null;
        },
    });
};

const setUploadURL = async (options) => {
    if (!uploadInfo.pid) await createNewPaper();
    return new Promise((resolve, reject) => {
        axios
            .post("/new/file", {
                name: options.file.name,
                pid: uploadInfo.pid,
            })
            .catch(reject)
            .then((response) => {
                if (response.data.result == "success") {
                    uploadInfo.files.push({
                        id: options.file.id,
                        fid: response.data.fid,
                        name: options.file.name,
                        type: 0,
                        key: response.data.key,
                        url: response.data.url,
                        obj: options.file,
                        status: 0,
                    });
                    uploadFile.url = response.data.url;
                    uploadFile.key = response.data.key;
                    resolve();
                }
                reject();
            });
    });
};

const setFinishUpload = (options) => {
    uploadInfo.files.find((item) => item.id == options.file.id).status = 2;
};

const setFailedUpload = (options) => {
    uploadInfo.files.find((item) => item.id == options.file.id).status = 1;
};

const handlePDFUpload = async (file, name) => {
    if (!uploadInfo.pid) await createNewPaper();
    axios
        .post("/new/file", {
            name: name,
            pid: uploadInfo.pid,
        })
        .then((response) => {
            if (response.data.result == "success") {
                uploadInfo.files.push({
                    fid: response.data.fid,
                    name: name,
                    type: 0,
                    key: response.data.key,
                    url: response.data.url,
                    obj: null,
                });
                postToS3(file, response.data.url, response.data.key);
                showPDF.value = false;
            }
        });
};

const postToS3 = (file, url, key) => {
    let formData = new FormData();
    formData.append("key", key);
    formData.append("acl", "private");
    formData.append("file", file);
    return axios({
        baseURL: "",
        url: url,
        method: "post",
        data: formData,
    });
};

const removeFile = (fid) => {
    if (uploadInfo.files.find((item) => item.fid == fid).status === 1) {
        uploadInfo.files = uploadInfo.files.filter((item) => item.fid != fid);
        return;
    }

    axios
        .post("/new/delete_file", {
            fid: fid,
        })
        .catch(reject)
        .then((response) => {
            if (response.data.result == "success") {
                uploadInfo.files = uploadInfo.files.filter(
                    (item) => item.fid != fid
                );
            }
        });
};

watch(
    () => uploadInfo.nid,
    (val) => {
        if (confirming.value) return;
        examGroupList.value = [];
        uploadInfo.egid = null;
        if (val === "new") {
            newUnionDialog();
        } else if (val === "create") {
            examGroupList.value.push({
                label: "",
                value: "new",
            });
        } else if (val) {
            fetchExamGroups();
        }
    }
);

watch(
    () => uploadInfo.egid,
    (val) => {
        if (val === "new") {
            newExamGroupDialog();
        }
    }
);

const ExamFinalName = computed(() => {
    let union = unionList.value.find((item) => item.value == uploadInfo.nid);
    let examgroup = examGroupList.value.find(
        (item) => item.value == uploadInfo.egid
    );
    let grade = grades[uploadInfo.grade];
    let course = courses[uploadInfo.course];
    if (!union || !examgroup) return null;
    return `${union.label} ${examgroup.label} ${grade} ${course}`;
});

const disablePreviousDate = (ts) => {
    return ts > Date.now();
};

const tableColumns = [
    {
        title: "文件名",
        key: "name",
        render: (row) => {
            return (
                <span class="whitespace-nowrap md:whitespace-normal">
                    {row.name}
                </span>
            );
        },
    },
    {
        title: "上传状态",
        key: "status",
        render: (row) => {
            switch (row.status) {
                case 0:
                    return (
                        <div class="flex items-center gap-x-2">
                            <n-spin size="small"></n-spin>
                            <span>上传中</span>
                        </div>
                    );
                case 1:
                    return <span class="text-red-500">错误发生</span>;
                case 2:
                default:
                    return <span class="text-green-500">上传成功</span>;
            }
        },
    },
    {
        title: "类型",
        key: "type",
        render: (row) => {
            return (
                <n-radio-group
                    size="small"
                    value={row.type}
                    on-update:value={(val) => {
                        uploadInfo.files.find(
                            (item) => item.fid == row.fid
                        ).type = val;
                    }}
                >
                    {file_types.map((item, index) => (
                        <n-radio-button
                            value={index}
                            label={item}
                        ></n-radio-button>
                    ))}
                </n-radio-group>
            );
        },
    },
    {
        title: "删除",
        key: "delete",
        render: (row) => (
            <n-button
                size="small"
                strong
                secondary
                round
                type="error"
                disabled={row.status === 0}
                on-click={() => removeFile(row.fid)}
            >
                删除
            </n-button>
        ),
    },
];

const tableData = computed(() => {
    return uploadInfo.files.map((item) => ({
        fid: item.fid,
        name: item.name,
        type: item.type,
        status: item.status,
    }));
});

const confirmUpload = async () => {
    confirming.value = true;
    if (uploadInfo.nid === "create") await createNewUnion();
    if (uploadInfo.egid === "create") await createNewExamGroup();
    await createNewExam();
    axios
        .post("/new/confirm", {
            eid: uploadInfo.eid,
            pid: uploadInfo.pid,
            comment: uploadInfo.comment,
            files: uploadInfo.files
                .filter((item) => item.status === 2)
                .map((item) => ({
                    fid: item.fid,
                    type: item.type,
                })),
        })
        .then((response) => {
            if (response.data.result == "success") {
                confirming.value = false;
                fetchUnions();
                fetchExamGroups();
                dialog.success({
                    title: "成功",
                    content: "试卷添加成功！",
                    positiveText: "好的",
                    onPositiveClick: () => {
                        uploadInfo.files = [];
                        createNewPaper();
                    },
                });
            }
        });
};

fetchUnions();
</script>

<template>
    <PicPdf
        v-model:show="showPDF"
        :hint="ExamFinalName"
        :key="ExamFinalName"
        @confirm="handlePDFUpload"
    />
    <div class="mx-8 w-auto lg:mx-auto lg:w-[60vw] mt-8">
        <p class="text-3xl font-bold mb-8">上传试卷</p>
        <n-form class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-x-8">
            <div class="col-span-1 lg:col-span-2">
                <n-form-item label="考试联盟/学校">
                    <n-select
                        v-model:value="uploadInfo.nid"
                        :options="unionList"
                        :render-label="renderLabel"
                        filterable
                    >
                    </n-select>
                </n-form-item>
            </div>
            <div class="col-span-1 lg:col-span-2">
                <n-form-item label="大考名称">
                    <n-select
                        v-model:value="uploadInfo.egid"
                        :options="examGroupList"
                        :disabled="
                            uploadInfo.nid === 'new' || uploadInfo.nid === null
                        "
                        :render-label="renderLabel"
                        filterable
                    >
                    </n-select>
                </n-form-item>
            </div>
            <div class="col-span-1">
                <n-form-item label="备注">
                    <n-auto-complete
                        class="w-full"
                        placeholder="图片版, 详解版 ..."
                        :options="getOptions(paper_types)"
                        v-model:value="uploadInfo.comment"
                    />
                </n-form-item>
            </div>
            <div class="col-span-1">
                <n-form-item label="考试时间">
                    <n-date-picker
                        class="w-full"
                        v-model:value="uploadInfo.date"
                        :is-date-disabled="disablePreviousDate"
                        type="date"
                    />
                </n-form-item>
            </div>
            <div class="col-span-1">
                <n-form-item label="年级">
                    <n-select
                        class="w-full"
                        v-model:value="uploadInfo.grade"
                        :options="getOptions(grades)"
                    />
                </n-form-item>
            </div>
            <div class="col-span-1">
                <n-form-item label="考试科目">
                    <n-select
                        v-model:value="uploadInfo.course"
                        :options="getOptions(courses)"
                    ></n-select>
                </n-form-item>
            </div>
        </n-form>
        <div
            class="flex flex-col md:flex-row gap-x-6 gap-y-2 items-start md:items-end"
            v-if="ExamFinalName"
        >
            <div>
                <p class="text-sky-800">您即将上传</p>
                <p class="text-lg">{{ ExamFinalName }}</p>
            </div>
            <n-button size="small" secondary @click="showPDF = true" type="info"
                >图片生成PDF</n-button
            >
        </div>
        <n-upload
            multiple
            directory-dnd
            class="mt-8 mb-4"
            :show-file-list="false"
            :action="uploadFile.url"
            :data="{ key: uploadFile.key, acl: 'private' }"
            :on-before-upload="setUploadURL"
            :on-finish="setFinishUpload"
            :on-error="setFailedUpload"
            v-if="ExamFinalName"
        >
            <n-upload-dragger>
                <div style="margin-bottom: 12px">
                    <n-icon size="48" :depth="3">
                        <Archive />
                    </n-icon>
                </div>
                <n-text style="font-size: 16px">
                    点击或者拖动文件到该区域来上传
                </n-text>
                <n-p depth="3" style="margin: 8px 0 0 0">
                    请不要上传敏感数据，比如你的银行卡号和密码，信用卡号有效期和安全码
                </n-p>
            </n-upload-dragger>
        </n-upload>
        <n-data-table
            :columns="tableColumns"
            :data="tableData"
            :bordered="false"
            v-if="uploadInfo.files.length"
        />
        <div
            class="mt-4 mb-8 flex justify-center"
            v-if="ExamFinalName && uploadInfo.files.length"
        >
            <n-button :on-click="confirmUpload" type="primary"
                >确认上传</n-button
            >
        </div>
    </div>
</template>
