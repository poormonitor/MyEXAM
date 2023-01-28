<script setup lang="jsx">
import { useRoute, useRouter } from "vue-router";
import { GetYearMonth } from "../func";
import { courses, grades } from "../const";

const axios = inject("axios");
const route = useRoute();
const router = useRouter();

const gotoExam = (eid) => {
    router.push({ name: "exam", params: { eid: eid } });
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
        title: "时间",
        key: "date",
        cellProps: cellProps,
    },
    {
        title: "浏览量",
        key: "views",
        cellProps: cellProps,
    },
];

const data = await axios
    .get("/list/examgroup", {
        params: {
            egid: route.params.egid,
        },
    })
    .then((response) => {
        if (response.data.examgroup) return response.data.examgroup;
    });
</script>

<template>
    <div class="flex justify-between mb-8">
        <div>
            <p class="text-2xl mb-0.5 text-purple-800">
                {{ data.union.name }}
            </p>
            <p class="text-4xl font-bold mb-3">
                <span class="whitespace-nowrap mr-2">
                    {{ GetYearMonth(data.date) }}
                </span>
                <span class="whitespace-nowrap">
                    {{ data.name }}
                </span>
            </p>
        </div>
        <div class="flex items-center mb-8">
            <Share type="union" :id="route.params.egid" />
        </div>
    </div>
    <n-divider title-placement="left">
        <span class="text-xl font-bold"> 考试信息 </span>
    </n-divider>
    <div class="flex flex-wrap gap-x-8 sm:gap-x-24 gap-y-4 mb-8 mx-2">
        <InfoTag label="联盟">
            <RouterLink
                class="router-link"
                :to="{
                    name: 'union',
                    params: { nid: data.union.nid },
                }"
            >
                {{ data.union.name }}
            </RouterLink>
        </InfoTag>
        <InfoTag label="考试名称">
            <span class="whitespace-nowrap mr-2">
                {{ GetYearMonth(data.date) }}
            </span>
            <span class="whitespace-nowrap">
                {{ data.name }}
            </span>
        </InfoTag>
        <InfoTag label="考试年月">
            {{ GetYearMonth(data.date) }}
        </InfoTag>
    </div>
    <n-divider title-placement="left">
        <span class="text-xl font-bold"> 考试列表 </span>
    </n-divider>
    <div>
        <n-data-table :data="data.exams" :columns="tableColumns" />
    </div>
</template>
