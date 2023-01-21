<script setup>
import { message } from "../discrete";
import pkg from "../../package.json";

const axios = inject("axios");
const version = __MYEXAM_VIEW_VERSION__;
const showVersion = ref(false);

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

const UpgradeAction = () => {
    axios.post("/system/upgrade").then((response) => {
        if (response.data.result === "success") {
            message.success("更新请求成功。");
        }
    });
};
</script>

<template>
    <p class="text-3xl font-bold pb-8 pt-2">系统管理</p>
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
        <n-modal v-model:show="showVersion">
            <n-card
                class="!mx-8 sm:!w-[30rem] sm:!mx-auto"
                title="依赖版本"
                :bordered="false"
                size="huge"
                role="dialog"
                aria-modal="true"
            >
                <ul>
                    <li
                        class="flex flex-wrap"
                        v-for="k in Object.keys(pkg.dependencies)"
                    >
                        <span>{{ k }}</span>
                        <span class="ml-auto">{{ pkg.dependencies[k] }}</span>
                    </li>
                </ul>
                <ul>
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
            </n-card>
        </n-modal>
        <n-card title="更新系统">
            <p>
                更新MyExam程序文件，并重新构建前端应用。后端可能需要手动重启。
            </p>
            <p>当前构建版本：{{ version }}</p>
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
