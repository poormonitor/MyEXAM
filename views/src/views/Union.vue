<script setup lang="jsx">
import { useRoute, useRouter } from "vue-router";
import { paramsError } from "../discrete";
import { getYearMonth } from "../func";
import { courses, grades } from "../const";
import { ArrowForwardOutline } from "@vicons/ionicons5";

const axios = inject("axios");
const route = useRoute();
const router = useRouter();

if (!route.query.nid) {
    paramsError();
}

const gotoExamGroup = (egid) => {
    router.push({ name: "examgroup", query: { egid: egid } });
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
                on-click={() => gotoExamGroup(row.egid)}
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
        rowSpan: (rowData) => (rowData.e === 0 ? rowData.cnt : 1),
    },
    {
        title: "考试名称",
        key: "name",
        render: (row) => <span>{getYearMonth(row.date) + " " + row.name}</span>,
        rowSpan: (rowData) => (rowData.e === 0 ? rowData.cnt : 1),
    },
    {
        title: "时间",
        key: "date",
        rowSpan: (rowData) => (rowData.e === 0 ? rowData.cnt : 1),
    },
    { title: "年级", key: "grade" },
    {
        title: "科目",
        key: "course",
        render: (row) => (
            <div>
                {row.courses.map((item) => (
                    <n-tag type="primary">{courses[item]}</n-tag>
                ))}
            </div>
        ),
    },
    {
        title: "浏览量",
        key: "views",
        rowSpan: (rowData) => (rowData.e === 0 ? rowData.cnt : 1),
    },
];

const data = await axios
    .get("/list/union", {
        params: {
            nid: route.query.nid,
        },
    })
    .then((response) => {
        if (response.data.union) return response.data.union;
    });

const tableData = [];
data.examgroups.forEach((examgroup) => {
    let eg = Object.assign(examgroup);
    Object.keys(examgroup.courses).forEach((grade, index) => {
        eg.e = index;
        eg.cnt = examgroup.courses.length;
        eg.grade = grades[grade];
        eg.courses = examgroup.courses[grade];
        tableData.push(eg);
    });
});
</script>

<template>
    <p class="text-4xl font-bold mb-4">
        {{ data.name }}
    </p>
    <div class="mb-8">
        <n-tag type="info" v-for="item in data.member.split('\n')">
            {{ item }}</n-tag
        >
    </div>
    <n-divider title-placement="left">
        <span class="text-xl font-bold"> 考试列表 </span>
    </n-divider>
    <div>
        <n-data-table :data="tableData" :columns="tableColumns" />
    </div>
</template>
