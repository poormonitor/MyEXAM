<script setup>
import { message } from "../discrete";
import pkg from "../../package.json";

const axios = inject("axios");
const showVersion = ref(false);
const ViewVersion = __MYEXAM_VIEW_VERSION__;
const ApiVersion = ref("");
const ApiDeps = ref([]);
const ObjectCnt = ref({
    union: 0,
    examgroup: 0,
    exam: 0,
    paper: 0,
    file: 0,
    user: 0,
    task: 0,
});
const LatestTask = ref(null);
const StaColumns = [
    { name: "联盟", key: "union", unit: "个" },
    { name: "联考", key: "examgroup", unit: "场" },
    { name: "考试", key: "exam", unit: "场" },
    { name: "试卷", key: "paper", unit: "张" },
    { name: "文件", key: "file", unit: "个" },
    { name: "用户", key: "user", unit: "个" },
    { name: "任务", key: "task", unit: "个" },
];

const CleanAction = () => {
    axios.post("/system/clean").then((response) => {
        if (response.data.result === "success") {
            message.success("清理成功。");
        }
    });
};

const CleanIsolateAction = () => {
    axios.post("/system/isolate").then((response) => {
        if (response.data.result === "success") {
            message.success("清理成功。");
        }
    });
};

const CleanMissAction = () => {
    axios.post("/system/miss").then((response) => {
        if (response.data.result === "success") {
            message.success("清理成功。");
        }
    });
};

const UpgradeAction = () => {
    axios.post("/system/upgrade").then((response) => {
        if (response.data.result === "success") {
            message.success("拉取成功，正在更新。");
        }
    });
};

const FetchApiSta = () => {
    axios.get("/system/statistic").then((response) => {
        if (response.data) {
            ObjectCnt.value = response.data.cnt;
            ApiVersion.value = response.data.version;
            ApiDeps.value = response.data.deps;
            LatestTask.value = response.data.task;
        }
    });
};

FetchApiSta();
</script>

<template>
    <p class="text-3xl font-bold pb-8 pt-2">系统管理</p>
    <n-card class="mb-8">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-y-4">
            <n-statistic
                :label="column.name"
                tabular-nums
                v-for="column in StaColumns"
            >
                <n-number-animation :from="0" :to="ObjectCnt[column.key]" />
                <template #suffix> {{ column.unit + column.name }} </template>
            </n-statistic>
            <n-statistic label="当前任务" v-if="LatestTask">
                <n-popover>
                    <template #trigger>
                        <span>{{ LatestTask.status * 100 }} %</span>
                    </template>
                    <div>
                        <p>
                            创建时间:
                            <span>
                                {{
                                    new Date(
                                        LatestTask.created
                                    ).toLocaleString()
                                }}
                            </span>
                        </p>
                        <p>任务类型: <span>{{ LatestTask.type }}</span></p>
                    </div>
                </n-popover>
            </n-statistic>
        </div>
    </n-card>
    <div class="flex flex-col gap-y-8">
        <n-card title="清理未完成试卷">
            清理系统中用户创建但没有完成上传的试卷。
            <template #action>
                <div class="flex justify-end">
                    <n-button type="primary" @click="CleanAction">
                        清理
                    </n-button>
                </div>
            </template>
        </n-card>
        <n-card title="清理孤立项目">
            清理系统中孤立的项目，包括考试、试卷和文件。
            <template #action>
                <div class="flex justify-end">
                    <n-button type="primary" @click="CleanIsolateAction">
                        清理
                    </n-button>
                </div>
            </template>
        </n-card>
        <n-card title="清理丢失文件">
            清理存在于数据库但在对象存储中丢失的文件。
            <template #action>
                <div class="flex justify-end">
                    <n-button type="primary" @click="CleanMissAction">
                        清理
                    </n-button>
                </div>
            </template>
        </n-card>
        <n-modal v-model:show="showVersion">
            <n-card
                class="!mx-8 sm:!w-[30rem] sm:!mx-auto"
                title="依赖版本"
                :bordered="false"
                size="huge"
                role="dialog"
                aria-modal="true"
            >
                <p class="text-lg font-bold mb-2">前端</p>
                <ul class="mb-2">
                    <li
                        class="flex flex-wrap"
                        v-for="k in Object.keys(pkg.dependencies)"
                    >
                        <span>{{ k }}</span>
                        <span class="ml-auto">{{ pkg.dependencies[k] }}</span>
                    </li>
                    <li
                        class="flex flex-wrap"
                        v-for="k in Object.keys(pkg.devDependencies)"
                    >
                        <span>{{ k }}</span>
                        <span class="ml-auto">
                            {{ pkg.devDependencies[k] }}
                        </span>
                    </li>
                </ul>
                <p class="text-lg font-bold mb-2">后端</p>
                <ul class="mb-2">
                    <li class="flex flex-wrap" v-for="item in ApiDeps">
                        <span>{{ item.name }}</span>
                        <span class="ml-auto">{{ item.version }}</span>
                    </li>
                </ul>
            </n-card>
        </n-modal>
        <n-card title="更新系统">
            <p>
                更新MyExam程序文件，并重新构建前端应用。后端可能需要手动重启。
            </p>
            <p>当前前端构建版本：{{ ViewVersion }}</p>
            <p>当前后端运行版本：{{ ApiVersion }}</p>
            <n-button text @click="showVersion = true" type="success">
                依赖信息
            </n-button>
            <template #action>
                <div class="flex justify-end">
                    <n-button type="primary" @click="UpgradeAction">
                        更新
                    </n-button>
                </div>
            </template>
        </n-card>
    </div>
</template>
