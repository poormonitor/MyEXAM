<script setup lang="jsx">
import { HeartOutline, HeartDislikeOutline, Ribbon } from "@vicons/ionicons5";
import { Suspense } from "vue";
import { useRoute } from "vue-router";
import { courses, grades, office_ext } from "../const";
import { message } from "../discrete";
import { GetYearMonth } from "../func";
import { useCartStore } from "../stores/cart";

const axios = inject("axios");
const route = useRoute();
const showData = ref(null);
const cartStore = useCartStore();

const preview = reactive({
    show: false,
    src: null,
    ext: "",
    title: "文件预览",
});

const previewFile = (fid, ext, name) => {
    axios
        .get("/list/url", {
            params: { fid: fid },
        })
        .then((response) => {
            if (response.data.url) {
                let file_url = response.data.url;
                preview.src = office_ext.includes(ext)
                    ? "http://view.officeapps.live.com/op/view.aspx?src=" +
                      encodeURI(file_url)
                    : file_url;
                preview.ext = ext;
                preview.title = name;
                preview.show = true;
            }
        });
};

const fetchExam = async () => {
    return new Promise((resolve) => {
        axios
            .get("/list/exam", { params: { eid: route.params.eid } })
            .then((response) => {
                if (response.data.exam) {
                    showData.value = response.data.exam;
                }
                resolve();
            });
    });
};

const delCart = (pid) => {
    cartStore.del(pid);
    message.success("删除成功。");
};

const addCart = (pid) => {
    cartStore.add(pid);
    message.success("添加成功。");
};

const tableColumns = [
    {
        title: "上传者",
        key: "uploader",
        render: (row) => (
            <div class="flex flex-col gap-y-1 justify-center">
                {row.owner && (
                    <div>
                        <n-tooltip trigger="hover">
                            {{
                                trigger: () => (
                                    <span class="flex items-center gap-x-0.5 text-green-600 mb-1">
                                        <n-icon component={Ribbon}></n-icon>
                                        <span>{row.owner}</span>
                                    </span>
                                ),
                                default: () => "认证的用户",
                            }}
                        </n-tooltip>
                    </div>
                )}
                {row.comment && (
                    <div>
                        {row.comment.split().map((item) => (
                            <n-tag type="success">{item}</n-tag>
                        ))}
                    </div>
                )}
                <div class='text-center'>{row.views} 浏览</div>
                <div class='flex justify-center mt-2'>
                    <n-button
                        circle
                        secondary
                        type={cartStore.has(row.pid) ? "error" : "success"}
                        onClick={
                            cartStore.has(row.pid)
                                ? () => delCart(row.pid)
                                : () => addCart(row.pid)
                        }
                    >
                        {{
                            icon: () => (
                                <n-icon
                                    size="1.2rem"
                                    component={
                                        cartStore.has(row.pid)
                                            ? HeartDislikeOutline
                                            : HeartOutline
                                    }
                                ></n-icon>
                            ),
                        }}
                    </n-button>
                </div>
            </div>
        ),
    },
    {
        title: "文件列表",
        key: "files",
        className: "w-full",
        render: (row) => (
            <div id={row.pid}>
                <n-collapse default-expanded-names={defaultExpanded}>
                    <n-collapse-item title="文件列表" name={"#" + row.pid}>
                        <Suspense>
                            {{
                                fallback: () => (
                                    <div class="flex justify-center">
                                        <n-spin>
                                            {{
                                                description: () => (
                                                    <span>加载中</span>
                                                ),
                                            }}
                                        </n-spin>
                                    </div>
                                ),
                                default: () => (
                                    <FileList
                                        onPreview={previewFile}
                                        pid={row.pid}
                                    />
                                ),
                            }}
                        </Suspense>
                    </n-collapse-item>
                </n-collapse>
                <div class="text-green-600 my-2">共计 {row.fcnt} 个文件</div>
            </div>
        ),
    },
];

onMounted(() => {
    if (route.hash) {
        document.getElementById(route.hash.substring(1))?.scrollIntoView();
    }
});

await fetchExam();

const defaultExpanded = route.hash
    ? route.hash
    : "#" + (showData.value.papers.length ? showData.value.papers[0].pid : "");
</script>

<template>
    <Preview
        :src="preview.src"
        :ext="preview.ext"
        v-model:show="preview.show"
        :title="preview.title"
    />
    <div class="flex justify-between mb-4 lg:mb-8">
        <div>
            <p class="text-2xl mb-0.5 text-purple-800">
                {{ showData.union.name }}
            </p>
            <p class="text-4xl font-bold mb-3">
                <span class="whitespace-nowrap mr-2">
                    {{ GetYearMonth(showData.examgroup.date) }}
                </span>
                <span class="whitespace-nowrap">
                    {{ showData.examgroup.name }}
                </span>
            </p>
            <p class="text-xl text-zinc-700 dark:text-zinc-400">
                {{ grades[showData.grade] }}
                {{ courses[showData.course] }}
            </p>
        </div>
        <div class="flex items-center">
            <Share type="exam" :id="route.params.eid" />
        </div>
    </div>
    <div>
        <n-divider title-placement="left">
            <span class="text-xl font-bold"> 考试信息 </span>
        </n-divider>
        <div class="flex flex-wrap gap-x-8 sm:gap-x-24 gap-y-4 mb-8 mx-2">
            <InfoTag label="联盟">
                <RouterLink
                    class="router-link"
                    :to="{
                        name: 'union',
                        params: { nid: showData.union.nid },
                    }"
                >
                    {{ showData.union.name }}
                </RouterLink>
            </InfoTag>
            <InfoTag label="考试名称">
                <RouterLink
                    class="router-link"
                    :to="{
                        name: 'examgroup',
                        params: { egid: showData.examgroup.egid },
                    }"
                >
                    <span class="whitespace-nowrap mr-2">
                        {{ GetYearMonth(showData.examgroup.date) }}
                    </span>
                    <span class="whitespace-nowrap">
                        {{ showData.examgroup.name }}
                    </span>
                </RouterLink>
            </InfoTag>
            <InfoTag label="考试日期">
                {{ showData.date }}
            </InfoTag>
            <InfoTag label="年级">
                {{ grades[showData.grade] }}
            </InfoTag>
            <InfoTag label="科目">
                {{ courses[showData.course] }}
            </InfoTag>
        </div>
        <n-divider title-placement="left">
            <span class="text-xl font-bold"> 可用试卷 </span>
        </n-divider>
        <div class="flex flex-row divide-y">
            <n-data-table
                class="whitespace-nowrap"
                row-class-name="table-no-hover"
                :data="showData.papers"
                :columns="tableColumns"
            ></n-data-table>
        </div>
    </div>
</template>

<style>
.table-no-hover:hover,
.table-no-hover:hover > .n-data-table-td {
    background-color: transparent !important;
}
</style>
