<script setup lang="jsx">
import { Suspense } from "vue";
import { courses, grades } from "../const";
import { message } from "../discrete";
import EditFile from "./EditFile.vue";

const axios = inject("axios");
const props = defineProps(["type", "id", "show"]);
const emits = defineEmits(["update:show", "update:modify"]);
const tpe = ref(null);
const data = ref(null);
const comp = ref(null);
const visible = computed({
    get() {
        return props.show;
    },
    set(value) {
        emits("update:show", value);
    },
});

const getOptions = (items) =>
    items.map((item, index) => ({
        label: item,
        value: index,
    }));

const types = [
    {
        key: "union",
        name: "联盟",
        id: "nid",
        options: [
            { key: "name", value: "联盟名称", type: "input" },
            { key: "member", value: "联盟成员", type: "textarea" },
        ],
    },
    {
        key: "examgroup",
        name: "联考",
        id: "egid",
        options: [
            { key: "name", value: "联考名称", type: "input" },
            { key: "date", value: "联考年月", type: "month" },
        ],
    },
    {
        key: "exam",
        name: "考试",
        id: "eid",
        options: [
            {
                key: "grade",
                value: "考试年级",
                type: "select",
                options: getOptions(grades),
            },
            {
                key: "course",
                value: "考试科目",
                type: "select",
                options: getOptions(courses),
            },
            { key: "date", value: "考试日期", type: "date" },
        ],
    },
    {
        key: "paper",
        name: "试卷",
        id: "pid",
        options: [
            { key: "comment", value: "备注", type: "input" },
            {
                key: "file",
                value: "文件",
                type: "component",
                component: (pid) => (
                    <Suspense>
                        {{
                            default: () => (
                                <EditFile
                                    onClose={() => {
                                        visible.value = false;
                                    }}
                                    pid={pid}
                                    ref={comp}
                                />
                            ),
                            fallback: () => <n-spin>加载中</n-spin>,
                        }}
                    </Suspense>
                ),
            },
        ],
    },
];

const fetchData = async () => {
    tpe.value = types.find((item) => item.key == props.type);
    let q = {};
    q[tpe.value.id] = props.id;
    await axios
        .get(`/list/${tpe.value.key}`, {
            params: q,
        })
        .then((response) => {
            if (response.data[tpe.value.key]) {
                let d = response.data[tpe.value.key];
                if (d.date) {
                    d.date = new Date(d.date).getTime();
                }
                data.value = d;
            }
        });
};

const SubmitModify = () => {
    let q = {};
    q[tpe.value.id] = props.id;
    for (let item of tpe.value.options) {
        q[item.key] = data.value[item.key];
    }
    if (comp.value) comp.value.submit();
    axios.post(`/manage/edit/${tpe.value.key}`, q).then((response) => {
        if (response.data.result === "success") {
            visible.value = false;
            message.success(`${tpe.value.name}修改成功。`);
            emits("update:modify");
        }
    });
};

const DeleteSelf = () => {
    let q = {};
    q[tpe.value.id] = props.id;
    axios.post(`/manage/delete/${tpe.value.key}`, q).then((response) => {
        if (response.data.result === "success") {
            visible.value = false;
            message.success(`${tpe.value.name}删除成功。`);
            emits("update:modify");
        }
    });
};

fetchData();
watch(() => props.id, fetchData);
</script>

<template>
    <n-modal
        v-model:show="visible"
        :title="'修改' + tpe.name"
        preset="dialog"
        positive-text="确认"
        negative-text="取消"
        @positive-click="SubmitModify"
        :style="{
            width: tpe.key === 'paper' ? '70%' : null,
        }"
    >
        <n-form v-if="data">
            <div class="mx-8 mb-6 mt-10">
                <div v-for="item in tpe.options">
                    <n-form-item
                        :label="item.value"
                        :key="item.key"
                        v-if="item.type !== 'component'"
                    >
                        <n-input
                            v-model:value="data[item.key]"
                            v-if="item.type === 'input'"
                        ></n-input>
                        <n-input
                            v-model:value="data[item.key]"
                            type="textarea"
                            v-else-if="item.type === 'textarea'"
                        ></n-input>
                        <n-select
                            v-model:value="data[item.key]"
                            :options="item.options"
                            v-else-if="item.type === 'select'"
                        ></n-select>
                        <n-date-picker
                            v-model:value="data[item.key]"
                            type="month"
                            class="w-full"
                            v-else-if="item.type === 'month'"
                        ></n-date-picker>
                        <n-date-picker
                            v-model:value="data[item.key]"
                            class="w-full"
                            v-else-if="item.type === 'date'"
                        ></n-date-picker>
                    </n-form-item>
                    <div class="mb-3" v-else>
                        <p class="mb-1">{{ item.value }}</p>
                        <component :is="item.component(props.id)" />
                    </div>
                </div>
                <div class="flex justify-center" v-if="tpe.key === 'file'">
                    <n-popconfirm @positive-click="DeleteSelf">
                        <template #trigger>
                            <n-button type="error" size="small" secondary>
                                删除{{ tpe.name }}
                            </n-button>
                        </template>
                        您确认要删除吗？
                    </n-popconfirm>
                </div>
            </div>
        </n-form>
        <n-spin v-else>加载中</n-spin>
    </n-modal>
</template>
