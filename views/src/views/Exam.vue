<script setup lang="jsx">
import { useRoute } from "vue-router";
import { paramsError } from "../discrete";
import { courses, grades, office_ext } from "../const";
import { getYearMonth } from "../func";
import { CloudDownloadOutline, Easel, AttachOutline } from "@vicons/ionicons5";
import FileList from "../components/FileList.vue";
import InfoTag from "../components/InfoTag.vue";
import Preview from "../components/Preview.vue";
import { Suspense } from "vue";

const axios = inject("axios");
const route = useRoute();
const showData = ref(null);

const preview = reactive({
    show: false,
    src: null,
    ext: "",
    title: "文件预览",
});

if (!route.query.eid) {
    paramsError();
}

const previewFile = (fid, ext, name) => {
    axios
        .get("/list/file", {
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
            .get("/list/exam", { params: { eid: route.query.eid } })
            .then((response) => {
                if (response.data.exam) {
                    showData.value = response.data.exam;
                }
                resolve();
            });
    });
};

const renderTitle = (title, icon) => {
    return () => (
        <div class="mx-2 flex gap-x-1 items-center whitespace-nowrap">
            <n-icon size="1rem" component={icon}></n-icon>
            {title}
        </div>
    );
};

const tableColumns = [
    {
        title: renderTitle("标签", Easel),
        key: "comment",
        render: (row) =>
            row.comment
                .split()
                .map((item) => <n-tag type="success">{item}</n-tag>),
    },
    {
        title: renderTitle("下载量", CloudDownloadOutline),
        key: "views",
    },
    {
        title: renderTitle("文件列表", AttachOutline),
        key: "files",
        className: "w-full",
        render: (row) => (
            <div>
                <n-collapse>
                    <n-collapse-item title="单击展开" name="1">
                        <Suspense>
                            {{
                                fallback: () => (
                                    <n-spin>
                                        {{
                                            description: () => (
                                                <span>加载中</span>
                                            ),
                                        }}
                                    </n-spin>
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
                <div class="text-blue-600 my-2">共计 {row.fcnt} 个文件</div>
            </div>
        ),
    },
];

await fetchExam();
</script>

<template>
    <Preview
        :src="preview.src"
        :ext="preview.ext"
        v-model:show="preview.show"
        :title="preview.title"
    />
    <div class="mb-4 lg:mb-8">
        <p class="text-2xl mb-0.5 text-purple-800">
            {{ showData.union.name }}
        </p>
        <p class="text-4xl font-bold mb-3">
            <span class="whitespace-nowrap mr-2">
                {{ getYearMonth(showData.examgroup.date) }}
            </span>
            <span class="whitespace-nowrap">
                {{ showData.examgroup.name }}
            </span>
        </p>
        <p class="text-xl text-zinc-700">
            {{ grades[showData.grade] }}
            {{ courses[showData.course] }}
        </p>
    </div>
    <div>
        <n-divider title-placement="left">
            <span class="text-xl font-bold"> 考试信息 </span>
        </n-divider>
        <div
            class="grid grid-cols-2 sm:grid-cols-6 lg:grid-cols-12 gap-y-4 mb-8 mx-2"
        >
            <InfoTag class="col-span-3" label="联盟">
                <RouterLink
                    class="router-link"
                    :to="{
                        name: 'union',
                        query: { nid: showData.union.nid },
                    }"
                >
                    {{ showData.union.name }}
                </RouterLink>
            </InfoTag>
            <InfoTag class="col-span-3" label="考试名称">
                <RouterLink
                    class="router-link"
                    :to="{
                        name: 'examgroup',
                        query: { egid: showData.examgroup.egid },
                    }"
                >
                    <span class="whitespace-nowrap mr-2">
                        {{ getYearMonth(showData.examgroup.date) }}
                    </span>
                    <span class="whitespace-nowrap">
                        {{ showData.examgroup.name }}
                    </span>
                </RouterLink>
            </InfoTag>
            <InfoTag class="col-span-2" label="考试日期">
                {{ showData.date }}
            </InfoTag>
            <InfoTag class="col-span-2" label="年级">
                {{ grades[showData.grade] }}
            </InfoTag>
            <InfoTag class="col-span-2" label="科目">
                {{ courses[showData.course] }}
            </InfoTag>
        </div>
        <n-divider title-placement="left">
            <span class="text-xl font-bold"> 可用试卷 </span>
        </n-divider>
        <div class="flex flex-row divide-y">
            <n-data-table
                :data="showData.papers"
                :columns="tableColumns"
            ></n-data-table>
        </div>
    </div>
</template>
