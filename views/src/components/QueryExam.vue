<script setup lang="jsx">
import { useRoute, useRouter } from "vue-router";
import { GetYearMonth } from "../func";
import { courses, grades } from "../const";
import { Search } from "@vicons/ionicons5";

const axios = inject("axios");
const collapsed = inject("collapsed");
const route = useRoute();
const router = useRouter();
const loading = ref(false);

const searchInfo = reactive({
    s: route.query.s ? route.query.s : "",
    range: [Date.now() - 1000 * 60 * 60 * 24 * 30, Date.now()],
    grade: null,
    courses: [],
});

const queryResult = reactive({
    list: [],
    cnt: 0,
});

const pagination = reactive({
    page: 1,
    pageCount: 0,
    pageSize: 10,
});

const getOptions = (items) =>
    items.map((item, index) => ({
        label: item,
        value: index,
    }));

const goQuery = () => {
    loading.value = true;
    if (searchInfo.s) router.push({ query: { s: searchInfo.s, t: "exam" } });
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
                queryResult.list = response.data.list;
                queryResult.cnt = response.data.count;
                pagination.pageCount = Math.ceil(
                    queryResult.cnt / pagination.pageSize
                );
                loading.value = false;
            }
        });
};

const gotoExam = (eid) => {
    router.push({ name: "exam", params: { eid: eid } });
};

const gotoPaper = (eid, pid) => {
    router.push({ name: "exam", params: { eid: eid }, hash: "#" + pid });
};

const cellProps = (row) => {
    return {
        class: "cursor-pointer",
        onClick: () => gotoExam(row.eid),
    };
};

const tableColumns = [
    {
        title: "年级",
        key: "grade",
        render: (row) => <span>{grades[row.grade]}</span>,
        cellProps: cellProps,
    },
    {
        title: "科目",
        key: "course",
        render: (row) => <span>{courses[row.course]}</span>,
        cellProps: cellProps,
    },
    {
        title: "联盟",
        key: "union",
        render: (row) => (
            <router-link
                class="text-sky-800 hover:text-sky-900 transition"
                to={{ name: "union", params: { nid: row.union.nid } }}
            >
                {row.union.name}
            </router-link>
        ),
    },
    {
        title: "考试",
        key: "exam",
        render: (row) => (
            <router-link
                class="text-sky-800 hover:text-sky-900 transition"
                to={{ name: "examgroup", params: { egid: row.examgroup.egid } }}
            >
                {GetYearMonth(row.examgroup.date) + " " + row.examgroup.name}
            </router-link>
        ),
    },
    {
        title: "日期",
        key: "date",
        render: (row) => <span>{row.date}</span>,
        cellProps: cellProps,
    },
    {
        title: "版本",
        key: "version",
        render: (row) => (
            <div>
                {row.papers.map((item) => (
                    <n-tag
                        type="info"
                        class="!cursor-pointer"
                        onClick={() => gotoPaper(row.eid, item.pid)}
                    >
                        {item.comment} ({item.fcnt})
                    </n-tag>
                ))}
            </div>
        ),
    },
    {
        title: "浏览量",
        key: "views",
        cellProps: cellProps,
    },
];

if (route.query.s) {
    goQuery();
}
</script>

<template>
    <div
        class="mx-8 flex items-center gap-x-4 md:mx-auto md:w-96 lg:w-[40vw] overflow-y-hidden"
    >
        <span class="whitespace-nowrap md:text-lg">考试</span>
        <n-input
            ref="inputRef"
            :size="collapsed ? 'medium' : 'large'"
            v-model:value="searchInfo.s"
            @keyup.enter="goQuery"
            placeholder="搜索"
        >
            <template #prefix>
                <n-icon :component="Search" />
            </template>
        </n-input>
        <n-button :size="collapsed ? 'medium' : 'large'" @click="goQuery">
            检索
        </n-button>
    </div>
    <div class="mx-auto mt-4 w-full self-start px-8 md:w-[80vw] lg:w-[60vw]">
        <n-collapse display-directive="show">
            <n-collapse-item title="筛选">
                <n-form
                    :size="collapsed ? 'small' : 'medium'"
                    class="flex flex-col gap-x-4 md:flex-row"
                >
                    <div class="w-full md:w-1/5">
                        <n-form-item label="年级">
                            <n-select
                                v-model:value="searchInfo.grade"
                                type="daterange"
                                :options="getOptions(grades)"
                            />
                        </n-form-item>
                    </div>
                    <div class="w-full md:w-2/5">
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
            </n-collapse-item>
        </n-collapse>
    </div>
    <n-divider></n-divider>
    <div class="px-8 w-full md:mx-auto md:w-[80vw]">
        <div class="mb-4">
            <n-statistic label="共计找到了" tabular-nums>
                {{ queryResult.cnt }}
                <template #suffix> 场考试 </template>
            </n-statistic>
        </div>
        <div v-if="queryResult.cnt">
            <n-data-table
                :columns="tableColumns"
                :data="queryResult.list"
                :loading="loading"
                class="whitespace-nowrap"
                @update:page="goQuery"
            />
            <n-pagination
                class="justify-end mt-3"
                v-model:page="pagination.page"
                :page-count="pagination.pageCount"
                @update:page="goQuery"
            />
        </div>
    </div>
</template>
