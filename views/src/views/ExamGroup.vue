<script setup lang="jsx">
import { useRoute, useRouter } from "vue-router";
import { GetYearMonth } from "../func";
import { courses, grades } from "../const";

const axios = inject("axios");
const route = useRoute();
const router = useRouter();
const PreviewImage = ref(null);
const PreviewRef = ref(null);
const LoadingPreview = ref(false);

const gotoExam = (eid) => {
    router.push({ name: "exam", params: { eid: eid } });
};

const goPreviewAssign = (aid) => {
    LoadingPreview.value = true;
    axios.get("/list/assign_url", { params: { aid: aid } }).then((response) => {
        if (response.data.url) {
            PreviewImage.value = response.data.url;
        }
    });
};

const previewReady = () => {
    PreviewRef.value.click();
    LoadingPreview.value = false;
};

const cellProps = (row) => {
    return {
        class: "cursor-pointer",
        onClick: () => gotoExam(row.eid),
    };
};

const AssignCellProps = (row) => {
    return {
        class: "cursor-pointer",
        onClick: () => goPreviewAssign(row.aid),
    };
};

const assignTableColumns = [
    {
        title: "赋分表",
        key: "comment",
        cellProps: AssignCellProps,
    },
    {
        title: "上传时间",
        key: "upload_time",
        render: (row) => new Date(row.upload_time).toLocaleString(),
        cellProps: AssignCellProps,
    },
    {
        title: "浏览量",
        key: "views",
        cellProps: AssignCellProps,
    },
];

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
    <n-image
        ref="PreviewRef"
        class="!hidden"
        :src="PreviewImage"
        :on-load="previewReady"
    />
    <div class="flex justify-between mb-8">
        <div>
            <p class="text-2xl mb-0.5 text-red-800">
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
            <Share type="examgroup" :id="route.params.egid" />
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
        <span class="text-xl font-bold"> 赋分表 </span>
    </n-divider>
    <div>
        <n-data-table
            :loading="LoadingPreview"
            :data="data.assigns"
            :columns="assignTableColumns"
        />
    </div>
    <n-divider title-placement="left">
        <span class="text-xl font-bold"> 考试列表 </span>
    </n-divider>
    <div>
        <n-data-table :data="data.exams" :columns="tableColumns" />
    </div>
</template>
