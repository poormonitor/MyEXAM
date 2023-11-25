<script setup lang="jsx">
import { TrashBin } from "@vicons/ionicons5";
import { Suspense } from "vue";
import { courses, grades, office_ext } from "../const";
import { GetYearMonth } from "../func";
import { useCartStore } from "../stores/cart";
import FileList from "./FileList.vue";

const cartStore = useCartStore();
const axios = inject("axios");
const showData = ref([]);
const loading = ref(false);

const pagination = reactive({
    page: 1,
    pageCount: 0,
    pageSize: 3,
});

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

const fetchData = () => {
    loading.value = true;

    if (!cartStore.cart.length) {
        showData.value = [];
        loading.value = false;
        return;
    }

    pagination.pageCount = Math.ceil(
        cartStore.cart.length / pagination.pageSize
    );

    let pids = cartStore.cart.slice(
        (pagination.page - 1) * pagination.pageSize,
        pagination.page * pagination.pageSize
    );

    axios.post("/list/papers", { pids: pids }).then((response) => {
        if (response.data.list) {
            showData.value = response.data.list;
            loading.value = false;
        }
    });
};

const clearCart = () => {
    cartStore.reset();
    showData.value = [];
    pagination.pageCount = 0;
    pagination.page = 1;
};

const tableColumns = [
    {
        title: "试卷",
        key: "paper",
        render: (row) => (
            <div>
                <p class="text-red-800/70">{row.union.name}</p>
                <p class="text-lg">
                    {GetYearMonth(row.examgroup.date) +
                        " " +
                        row.examgroup.name}
                </p>
                <p class="mb-2 text-zinc-800/70">
                    {grades[row.exam.grade]}
                    {courses[row.exam.course]}
                </p>
                <div>
                    {row.comment && row.comment.split().map((item) => (
                        <n-tag type="success">{item}</n-tag>
                    ))}
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
                <Suspense>
                    {{
                        fallback: () => (
                            <div class="flex justify-center">
                                <n-spin>
                                    {{
                                        description: () => <span>加载中</span>,
                                    }}
                                </n-spin>
                            </div>
                        ),
                        default: () => (
                            <FileList
                                onPreview={previewFile}
                                data={row.files}
                            />
                        ),
                    }}
                </Suspense>
                <div class="text-red-800 my-2">
                    共计 {row.files.length} 个文件
                </div>
            </div>
        ),
    },
    {
        key: "delete",
        title: "删除",
        render: (row) => (
            <n-button
                circle
                secondary
                type="error"
                onClick={() => {
                    cartStore.del(row.pid);
                    fetchData();
                }}
            >
                {{ icon: () => <n-icon component={TrashBin}></n-icon> }}
            </n-button>
        ),
    },
];

fetchData();
</script>
<template>
    <Preview
        :src="preview.src"
        :ext="preview.ext"
        v-model:show="preview.show"
        :title="preview.title"
    />
    <div v-if="showData">
        <n-data-table
            class="whitespace-nowrap"
            :columns="tableColumns"
            :data="showData"
            :loading="loading"
        ></n-data-table>
        <n-pagination
            class="justify-end mt-3"
            v-model:page="pagination.page"
            :page-count="pagination.pageCount"
            @update:page="fetchData"
        >
            <template #prefix>
                <n-popconfirm @positive-click="clearCart">
                    <template #trigger>
                        <n-button type="error" size="small" secondary>
                            清空收藏
                        </n-button>
                    </template>
                    确认要清空收藏吗？
                </n-popconfirm>
            </template>
        </n-pagination>
    </div>
    <div class="flex justify-center" v-else>
        <n-spin>
            <template #description>加载中</template>
        </n-spin>
    </div>
</template>
