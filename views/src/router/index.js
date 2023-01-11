import { createRouter, createWebHashHistory } from "vue-router";
import { useUserStore } from "../stores/user";

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        {
            path: "/",
            name: "home",
            component: () => import("../views/Home.vue"),
            meta: {
                requiresAuth: false,
                title: "首页",
            },
        },
        {
            path: "/login",
            name: "login",
            component: () => import("../views/Login.vue"),
            meta: {
                requiresAuth: false,
                title: "用户登录",
            },
        },
        {
            path: "/reg",
            name: "reg",
            component: () => import("../views/Reg.vue"),
            meta: {
                requiresAuth: false,
                title: "用户注册",
            },
        },
        {
            path: "/query",
            name: "query",
            component: () => import("../views/Query.vue"),
            meta: {
                requiresAuth: false,
                title: "搜试卷",
            },
        },
        {
            path: "/discover",
            name: "discover",
            component: () => import("../views/Discover.vue"),
            meta: {
                requiresAuth: false,
                title: "探索",
            },
        },
        {
            path: "/upload",
            name: "upload",
            component: () => import("../views/Upload.vue"),
            meta: {
                requiresAuth: false,
                title: "传试卷",
            },
        },
        {
            path: "/view",
            redirect: { name: "home" },
            component: () => import("../views/View.vue"),
            children: [
                {
                    path: "exam",
                    name: "exam",
                    component: () => import("../views/Exam.vue"),
                    meta: {
                        requiresAuth: false,
                        title: "试卷",
                    },
                },
                {
                    path: "union",
                    name: "union",
                    component: () => import("../views/Union.vue"),
                    meta: {
                        requiresAuth: false,
                        title: "联盟",
                    },
                },
                {
                    path: "examgroup",
                    name: "examgroup",
                    component: () => import("../views/ExamGroup.vue"),
                    meta: {
                        requiresAuth: false,
                        title: "考试",
                    },
                },
            ],
        },
    ],
});

router.beforeEach((to, from) => {
    if (to.meta.title) {
        document.title = to.meta.title + " - MyEXAM";
    }
    const userStore = useUserStore();

    if (to.meta.requiresAuth && !userStore.uid) return { name: "login" };
    if (userStore.uid && ["login", "reg"].includes(to.name))
        return { name: "home" };
});

export default router;
