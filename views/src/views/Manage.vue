<script setup lang="jsx">
import { grades, courses } from "../const";
import { GetYearMonth } from "../func";
import { message } from "../discrete";
import { provide } from "vue";

const axios = inject("axios");
const data = ref([]);
const cnt = ref(0);
const loading = ref(true);

const searchInfo = reactive({
    s: "",
    range: [Date.now() - 1000 * 60 * 60 * 24 * 365, Date.now()],
    grade: null,
    courses: [],
});

const pagination = reactive({
    page: 1,
    pageCount: 0,
    pageSize: 10,
});

const ModifyAction = reactive({
    current: null,
    show: false,
    type: null,
    id: null,
});

provide("ModifyData", toRef(ModifyAction, "current"));

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
                cnt.value = response.data.count;
                pagination.pageCount = Math.ceil(
                    cnt.value / pagination.pageSize
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

const tableColumns = [
    {
        title: "联盟",
        key: "union",
        render: (row) => (
            <n-button
                text
                type="info"
                on-click={() => {
                    ModifyAction.current = row;
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
                type="info"
                on-click={() => {
                    ModifyAction.current = row;
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
        className: "whitespace-nowrap",
        render: (row) => <span>{row.date}</span>,
    },
    {
        title: "科目",
        key: "course",
        className: "whitespace-nowrap",
        render: (row) => <span>{courses[row.course]}</span>,
    },
    {
        title: "年级",
        key: "grade",
        className: "whitespace-nowrap",
        render: (row) => <span>{grades[row.grade]}</span>,
    },
    {
        title: "浏览量",
        key: "views",
        className: "whitespace-nowrap",
    },
    {
        title: "版本",
        key: "version",
        render: (row) => (
            <div class="flex flex-col gap-y-1">
                {row.papers.map((item) => (
                    <n-button
                        type="info"
                        size="small"
                        secondary
                        on-click={() => {
                            ModifyAction.current = row;
                            ModifyAction.id = item.pid;
                            ModifyAction.type = "paper";
                            ModifyAction.show = true;
                        }}
                    >
                        {item.owner} {item.comment} ({item.fcnt})
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
                    ModifyAction.current = row;
                    ModifyAction.id = row.eid;
                    ModifyAction.type = "exam";
                    ModifyAction.show = true;
                }}
            >
                修改
            </n-button>
        ),
    },
];

fetchData();

watch(searchInfo, fetchData);
</script>

<template>
    <EditItem
        v-model:show="ModifyAction.show"
        :type="ModifyAction.type"
        :id="ModifyAction.id"
        @update:modify="fetchData"
        v-if="ModifyAction.type"
    />
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
            class="whitespace-nowrap"
        />
        <n-pagination
            class="justify-end mt-3"
            v-model:page="pagination.page"
            :page-count="pagination.pageCount"
            @update:page="fetchData"
        />
    </div>
</template>
