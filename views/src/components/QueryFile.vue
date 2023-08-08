<script setup lang="jsx">
import { useRoute, useRouter } from "vue-router";
import { GetYearMonth } from "../func";
import { courses, file_types, grades } from "../const";
import { Search, Ribbon } from "@vicons/ionicons5";

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
    if (!searchInfo.s) return;
    loading.value = true;
    router.push({ query: { s: searchInfo.s, t: 1, p: pagination.page } });
    axios
        .post("/search/file", {
            s: searchInfo.s,
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

const gotoPaper = (eid, pid) => {
    router.push({ name: "exam", params: { eid: eid }, hash: "#" + pid });
};

const cellProps = (row) => {
    return {
        class: "cursor-pointer",
        onClick: () => gotoPaper(row.exam.eid, row.paper.pid),
    };
};

const tableColumns = [
    {
        type: "expand",
        expandable: () => true,
        renderExpand: (row) => {
            let text = row.text.map((item) =>
                item
                    .replaceAll(
                        "*s*",
                        `<span class="font-bold text-indigo-600">`
                    )
                    .replaceAll("*e*", "</span>")
            );
            return (
                <div class="flex flex-wrap gap-x-8 gap-y-0.5">
                    {text.map((item) => (
                        <span class="whitespace-nowrap" innerHTML={item}></span>
                    ))}
                </div>
            );
        },
    },
    {
        title: "文件名",
        key: "name",
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
        title: "年级",
        key: "grade",
        render: (row) => <span>{grades[row.exam.grade]}</span>,
        cellProps: cellProps,
    },
    {
        title: "科目",
        key: "course",
        render: (row) => <span>{courses[row.exam.course]}</span>,
        cellProps: cellProps,
    },
    {
        title: "版本",
        key: "version",
        render: (row) => (
            <div class="flex gap-1">
                <n-tag class="!cursor-pointer" type="info">
                    {row.paper.owner}
                </n-tag>
                {row.paper.comment &&
                    row.paper.comment.split().map((item) => (
                        <n-tag class="!cursor-pointer" type="info">
                            {item}
                        </n-tag>
                    ))}
            </div>
        ),
        cellProps: cellProps,
    },
    {
        title: "类型",
        key: "type",
        render: (row) => file_types[row.type],
        cellProps: cellProps,
    },
    {
        title: "日期",
        key: "date",
        render: (row) => <span>{row.exam.date}</span>,
        cellProps: cellProps,
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
        <span class="whitespace-nowrap md:text-lg">文件</span>
        <n-input
            ref="inputRef"
            :size="collapsed ? 'medium' : 'large'"
            v-model:value="searchInfo.s"
            @keyup.enter="goQuery"
            placeholder="文件内容"
        >
            <template #prefix>
                <n-icon :component="Search" />
            </template>
        </n-input>
        <n-button :size="collapsed ? 'medium' : 'large'" @click="goQuery">
            检索
        </n-button>
    </div>
    <div class="mx-auto my-4 w-full self-start px-8 md:w-[80vw] lg:w-[60vw]">
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
                <template #suffix> 份文件 </template>
            </n-statistic>
        </div>
        <div v-if="queryResult.cnt">
            <n-data-table
                :columns="tableColumns"
                :data="queryResult.list"
                :loading="loading"
                class="whitespace-nowrap"
                default-expand-all
            />
            <n-pagination
                class="justify-end mt-3"
                v-model:page="pagination.page"
                :page-count="pagination.pageCount"
                @update:page="goQuery"
            />
        </div>
        <n-empty class="mt-12" description="什么也没找到" v-else></n-empty>
    </div>
</template>
