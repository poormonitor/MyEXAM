<script setup>
import { getYearMonth } from "../func";
import { courses, grades } from "../const";
import { Eye } from "@vicons/ionicons5";
import { useRouter } from "vue-router";

const router = useRouter();
const axios = inject("axios");
const data = ref(null);
const requestForm = reactive({
    course: null,
    grade: null,
});

const resetForm = () => {
    requestForm.course = null;
    requestForm.grade == null;
};

const getOptions = (items) =>
    items.map((item, index) => ({
        label: item,
        value: index,
    }));

const gotoExam = (eid) => {
    router.push({
        name: "exam",
        query: {
            eid: eid,
        },
    });
};

const getExamName = (item) => {
    let union = item.union.name;
    let name = item.examgroup.name;
    let date = getYearMonth(item.examgroup.date);
    return `${union} ${date} ${name}`;
};

watch(
    requestForm,
    () => {
        data.value = null;
        axios
            .post("/discover/exams", {
                course: requestForm.course,
                grade: requestForm.grade,
            })
            .then((response) => {
                if (response.data.list) {
                    data.value = response.data.list;
                }
            });
    },
    { immediate: true }
);
</script>

<template>
    <div class="mx-8 w-auto lg:mx-auto lg:w-[60vw] mt-8 overflow-y-hidden">
        <p class="text-3xl font-bold mb-4">找试卷</p>
        <div class="md:w-3/4 lg:2/3 mx-auto mb-4">
            <n-form inline>
                <n-form-item class="basis-1/2" label="学科">
                    <n-select
                        v-model:value="requestForm.course"
                        :options="getOptions(courses)"
                        clearable
                    />
                </n-form-item>
                <n-form-item class="basis-1/2" label="年级">
                    <n-select
                        v-model:value="requestForm.grade"
                        :options="getOptions(grades)"
                        clearable
                    />
                </n-form-item>
            </n-form>
        </div>
        <div v-if="data && data.length">
            <n-list hoverable clickable bordered>
                <n-list-item v-for="item in data">
                    <n-thing
                        @click="gotoExam(item.eid)"
                        :title="getExamName(item)"
                    >
                        <template #description>
                            <n-space size="small" class="mt-2">
                                <n-tag type="info" size="small">
                                    {{ courses[item.course] }}
                                </n-tag>
                                <n-tag type="info" size="small">
                                    {{ grades[item.grade] }}
                                </n-tag>
                                <span class="ml-4 flex items-center gap-x-1">
                                    <n-icon><Eye /></n-icon>
                                    {{ item.views }}
                                </span>
                            </n-space>
                        </template>
                    </n-thing>
                </n-list-item>
            </n-list>
        </div>
        <div v-else-if="data && data.length === 0">
            <n-empty description="什么也找不到">
                <template #extra>
                    <n-button size="small" @click="resetForm">
                        看看别的
                    </n-button>
                </template>
            </n-empty>
        </div>
        <div class="flex place-content-center mt-4" v-else>
            <n-spin> 加载中 </n-spin>
        </div>
    </div>
</template>
