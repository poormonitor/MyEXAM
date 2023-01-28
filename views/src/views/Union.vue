<script setup lang="jsx">
import { useRoute, useRouter } from "vue-router";
import { GetYearMonth } from "../func";
import { courses, grades } from "../const";

const axios = inject("axios");
const route = useRoute();
const router = useRouter();

const gotoExamGroup = (egid) => {
    router.push({ name: "examgroup", params: { egid: egid } });
};

const gotoExam = (eid) => {
    router.push({ name: "exam", params: { eid: eid } });
};

const cellProps = (row) => {
    return {
        class: "cursor-pointer",
        onClick: () => gotoExamGroup(row.egid),
    };
};

const tableColumns = [
    {
        title: "考试名称",
        key: "name",
        render: (row) => <span>{GetYearMonth(row.date) + " " + row.name}</span>,
        rowSpan: (rowData) => (rowData.e === 0 ? rowData.cnt : 1),
        cellProps: cellProps,
    },
    {
        title: "时间",
        key: "date",
        rowSpan: (rowData) => (rowData.e === 0 ? rowData.cnt : 1),
        cellProps: cellProps,
    },
    { title: "年级", key: "grade", cellProps: cellProps },
    {
        title: "科目",
        key: "course",
        render: (row) => (
            <div class="flex gap-2">
                {row.courses.map((item) => (
                    <n-tag
                        type="primary"
                        class="!cursor-pointer"
                        onClick={() => gotoExam(item[1])}
                    >
                        {courses[item[0]]}
                    </n-tag>
                ))}
            </div>
        ),
    },
    {
        title: "浏览量",
        key: "views",
        rowSpan: (rowData) => (rowData.e === 0 ? rowData.cnt : 1),
        cellProps: cellProps,
    },
];

const data = await axios
    .get("/list/union", {
        params: {
            nid: route.params.nid,
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
    <div class="flex justify-between">
        <div>
            <p class="text-4xl font-bold mb-4">
                {{ data.name }}
            </p>
            <div class="mb-4" v-if="data.member">
                <n-tag type="info" v-for="item in data.member.split('\n')">
                    {{ item }}
                </n-tag>
            </div>
        </div>
        <div class="flex items-center mb-8">
            <Share type="union" :id="route.params.nid" />
        </div>
    </div>
    <n-divider title-placement="left">
        <span class="text-xl font-bold"> 考试列表 </span>
    </n-divider>
    <div>
        <n-data-table
            class="whitespace-nowrap"
            :data="tableData"
            :columns="tableColumns"
        />
    </div>
</template>
