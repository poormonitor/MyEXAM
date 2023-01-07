<script setup lang="jsx">
import { useRoute, useRouter } from "vue-router";
import { paramsError } from "../discrete";
import { getYearMonth } from "../func";
import { courses, grades } from "../const";
import { ArrowForwardOutline } from "@vicons/ionicons5";
import InfoTag from "../components/InfoTag.vue";

const axios = inject("axios");
const route = useRoute();
const router = useRouter();

if (!route.query.egid) {
    paramsError();
}

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
        title: "年级",
        key: "grade",
        render: (row) => <span>{grades[row.grade]}</span>,
    },
    {
        title: "科目",
        key: "course",
        render: (row) => <span>{courses[row.course]}</span>,
    },
    {
        title: "时间",
        key: "date",
    },
    {
        title: "浏览量",
        key: "views",
    },
];

const data = await axios
    .get("/list/examgroup", {
        params: {
            egid: route.query.egid,
        },
    })
    .then((response) => {
        if (response.data.examgroup) return response.data.examgroup;
    });
</script>

<template>
    <div class="mb-8">
        <p class="text-2xl mb-0.5 text-purple-800">
            {{ data.union.name }}
        </p>
        <p class="text-4xl font-bold mb-3">
            <span class="whitespace-nowrap mr-2">
                {{ getYearMonth(data.date) }}
            </span>
            <span class="whitespace-nowrap">
                {{ data.name }}
            </span>
        </p>
    </div>
    <n-divider title-placement="left">
        <span class="text-xl font-bold"> 考试信息 </span>
    </n-divider>
    <div
        class="grid grid-cols-3 sm:grid-cols-6 lg:grid-cols-9 gap-y-4 mb-8 mx-2"
    >
        <InfoTag class="col-span-3" label="联盟">
            <RouterLink
                class="router-link"
                :to="{
                    name: 'union',
                    query: { nid: data.union.nid },
                }"
            >
                {{ data.union.name }}
            </RouterLink>
        </InfoTag>
        <InfoTag class="col-span-3" label="考试名称">
            <span class="whitespace-nowrap mr-2">
                {{ getYearMonth(data.date) }}
            </span>
            <span class="whitespace-nowrap">
                {{ data.name }}
            </span>
        </InfoTag>
        <InfoTag class="col-span-3" label="考试年月">
            {{ getYearMonth(data.date) }}
        </InfoTag>
    </div>
    <n-divider title-placement="left">
        <span class="text-xl font-bold"> 考试列表 </span>
    </n-divider>
    <div>
        <n-data-table :data="data.exams" :columns="tableColumns" />
    </div>
</template>
