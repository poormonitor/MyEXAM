<script setup lang="jsx">
import { useRoute, useRouter } from "vue-router";
import { getYearMonth } from "../func";
import { courses, grades } from "../const";
import { Search, ArrowForwardOutline } from "@vicons/ionicons5";

const axios = inject("axios");
const collapsed = inject("collapsed");
const route = useRoute();
const router = useRouter();

const cntRef = ref(null);
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

const getOptions = (items) =>
    items.map((item, index) => ({
        label: item,
        value: index,
    }));

const goQuery = () => {
    loading.value = true;
    if (searchInfo.s) router.push({ query: { s: searchInfo.s } });
    axios
        .post("/search/exam", {
            name: searchInfo.s,
            start: searchInfo.range[0],
            end: searchInfo.range[1],
            courses: searchInfo.courses,
            grade: searchInfo.grade,
        })
        .then((response) => {
            if (response.data.list) {
                queryResult.list = response.data.list;
                queryResult.cnt = response.data.count;
                loading.value = false;
                cntRef.value?.play();
            }
        });
};

const gotoExam = (eid) => {
    router.push({ name: "exam", query: { eid: eid } });
};

const tableColumns = [
    {
        title: "查看",
        key: "go",
        render: (row) => (
            <n-button
                size="small"
                type="info"
                quaternary
                on-click={() => gotoExam(row.eid)}
            >
                {{
                    icon: (
                        <n-icon>
                            <ArrowForwardOutline />
                        </n-icon>
                    ),
                }}
            </n-button>
        ),
    },
    {
        title: "联盟",
        key: "union",
        render: (row) => (
            <router-link
                class="text-sky-800 hover:text-sky-900 transition"
                to={{ name: "union", query: { nid: row.union.nid } }}
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
                to={{ name: "examgroup", query: { egid: row.examgroup.egid } }}
            >
                {getYearMonth(row.examgroup.date) + " " + row.examgroup.name}
            </router-link>
        ),
    },
    {
        title: "日期",
        key: "date",
        render: (row) => <span>{row.date}</span>,
        sorter: (row1, row2) => new Date(row1.date) - new Date(row2.date),
    },
    {
        title: "版本",
        key: "version",
        render: (row) => (
            <div>
                {row.papers.map((item) => (
                    <n-tag type="info">{item.comment}</n-tag>
                ))}
            </div>
        ),
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
        sorter: (row1, row2) => row1.views - row2.views,
    },
];

if (route.query.s) {
    goQuery();
}
</script>

<template>
    <div class="mt-8 flex flex-col items-center md:mt-10">
        <n-tabs type="segment">
            <n-tab-pane name="exam" tab="搜索考试">
                <QueryExam />
            </n-tab-pane>
            <n-tab-pane name="file" tab="搜索文件">
                <QueryFile />
            </n-tab-pane>
        </n-tabs>
    </div>
</template>

<style lang="postcss">
.n-tabs-nav {
    @apply justify-center mb-1;
}

.n-tabs-rail {
    @apply w-64 !important;
}

.paperTable tr:hover td {
    @apply bg-blue-50;
}
</style>
