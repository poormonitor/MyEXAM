<script setup lang="jsx">
import { grades, courses } from "../const";
import { GetYearMonth } from "../func";
import { message } from "../discrete";

const axios = inject("axios");
const data = ref([]);
const cnt = ref(0);
const loading = ref(true);

const searchInfo = reactive({
    s: "",
    range: [Date.now() - 1000 * 60 * 60 * 24 * 30, Date.now()],
    grade: null,
    courses: [],
});

const pagination = reactive({
    page: 0,
    pageCount: 0,
    pageSize: 10,
});

const ModifyAction = reactive({
    show: false,
    type: null,
    id: null,
});

const fetchData = () => {
    loading.value = true;
    axios
        .post("/search/exam", {
            name: searchInfo.s,
            start: searchInfo.range[0],
            end: searchInfo.range[1],
            courses: searchInfo.courses,
            grade: searchInfo.grade,
            page: pagination.page,
        })
        .then((response) => {
            if (response.data.list) {
                data.value = response.data.list;
                cnt.value = response.data.cnt;
                pagination.pageCount = Math.ceil(
                    cnt.value / pagination.pageCount
                );
                loading.value = false;
            }
        });
};

const getOptions = (items) =>
    items.map((item, index) => ({
        label: item,
        value: index,
    }));

const DeleteExam = (eid) => {
    axios.post("/manage/delete/exam", { eid: eid }).then((response) => {
        if (response.data.result === "success") {
            message.success("删除成功");
            data.value = data.value.filter((item) => item.eid != eid);
        }
    });
};

const tableColumns = [
    {
        title: "联盟",
        key: "union",
        render: (row) => (
            <n-button
                text
                tag="a"
                type="info"
                on-click={() => {
                    ModifyAction.id = row.union.nid;
                    ModifyAction.type = "union";
                    ModifyAction.show = true;
                }}
            >
                {row.union.name}
            </n-button>
        ),
    },
    {
        title: "联考",
        key: "examgroup",
        render: (row) => (
            <n-button
                text
                tag="a"
                type="info"
                on-click={() => {
                    ModifyAction.id = row.examgroup.egid;
                    ModifyAction.type = "examgroup";
                    ModifyAction.show = true;
                }}
            >
                {GetYearMonth(row.examgroup.date) + " " + row.examgroup.name}
            </n-button>
        ),
    },
    {
        title: "日期",
        key: "date",
        render: (row) => <span>{row.date}</span>,
    },
    {
        title: "科目",
        key: "course",
        render: (row) => <span>{courses[row.course]}</span>,
    },
    {
        title: "年级",
        key: "grade",
        render: (row) => <span>{grades[row.grade]}</span>,
    },
    {
        title: "浏览量",
        key: "views",
    },
    {
        title: "版本",
        key: "version",
        render: (row) => (
            <div class="flex flex-row gap-y-2">
                {row.papers.map((item) => (
                    <n-button
                        type="info"
                        size="small"
                        secondary
                        on-click={() => {
                            ModifyAction.id = item.pid;
                            ModifyAction.type = "paper";
                            ModifyAction.show = true;
                        }}
                    >
                        {item.comment}
                    </n-button>
                ))}
            </div>
        ),
    },
    {
        title: "修改",
        key: "edit",
        render: (row) => (
            <n-button
                type="info"
                size="small"
                on-click={() => {
                    ModifyAction.id = row.eid;
                    ModifyAction.type = "exam";
                    ModifyAction.show = true;
                }}
            >
                修改
            </n-button>
        ),
    },
    {
        title: "删除",
        key: "delete",
        render: (row) => (
            <n-popconfirm on-positive-click={() => DeleteExam(row.eid)}>
                {{
                    trigger: () => (
                        <n-button type="error" size="small">
                            删除
                        </n-button>
                    ),
                    default: () => "你确认要删除吗？",
                }}
            </n-popconfirm>
        ),
    },
];

fetchData();
</script>

<template>
    <Suspense>
        <EditItem
            v-model:show="ModifyAction.show"
            :type="ModifyAction.type"
            :id="ModifyAction.id"
            v-if="ModifyAction.type"
        />
    </Suspense>
    <p class="text-3xl font-bold pb-6 pt-2">试卷管理</p>
    <div>
        <n-form class="flex flex-col gap-x-4 md:flex-row mb-2">
            <div class="w-full md:w-1/5">
                <n-form-item label="名称">
                    <n-input v-model:value="searchInfo.s" />
                </n-form-item>
            </div>
            <div class="w-full md:w-1/5">
                <n-form-item label="年级">
                    <n-select
                        v-model:value="searchInfo.grade"
                        type="daterange"
                        :options="getOptions(grades)"
                    />
                </n-form-item>
            </div>
            <div class="w-full md:w-1/5">
                <n-form-item label="科目">
                    <n-select
                        v-model:value="searchInfo.courses"
                        max-tag-count="responsive"
                        multiple
                        clearable
                        :options="getOptions(courses)"
                    />
                </n-form-item>
            </div>
            <div class="w-full md:w-2/5">
                <n-form-item label="时间">
                    <n-date-picker
                        v-model:value="searchInfo.range"
                        type="daterange"
                        clearable
                    />
                </n-form-item>
            </div>
        </n-form>
        <n-data-table
            :data="data"
            :columns="tableColumns"
            :loading="loading"
            :pagination="pagination"
            class="whitespace-nowrap md:whitespace-normal"
            @update:page="fetchData"
        />
    </div>
</template>
