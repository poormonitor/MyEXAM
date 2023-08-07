import { createRouter, createWebHashHistory } from "vue-router";
import { useUserStore } from "../stores/user";

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        {
            path: "/",
            name: "index",
            redirect: { name: "home" },
            component: () => import("../views/Index.vue"),
            meta: {
                requiresAuth: false,
                requiresAdmin: false,
            },
            children: [
                {
                    path: "",
                    name: "home",
                    component: () => import("../views/Home.vue"),
                    meta: {
                        title: "首页",
                    },
                },
                {
                    path: "login",
                    name: "login",
                    component: () => import("../views/Login.vue"),
                    meta: {
                        title: "用户登录",
                    },
                },
                {
                    path: "query",
                    name: "query",
                    component: () => import("../views/Query.vue"),
                    meta: {
                        title: "搜索",
                    },
                },
                {
                    path: "discover",
                    name: "discover",
                    component: () => import("../views/Discover.vue"),
                    meta: {
                        title: "热门",
                    },
                },
                {
                    path: "view",
                    name: "view",
                    redirect: { name: "home" },
                    component: () => import("../views/View.vue"),
                    children: [
                        {
                            path: "exam/:eid",
                            name: "exam",
                            component: () => import("../views/Exam.vue"),
                            meta: {
                                title: "试卷",
                            },
                        },
                        {
                            path: "union/:nid",
                            name: "union",
                            component: () => import("../views/Union.vue"),
                            meta: {
                                title: "联盟",
                            },
                        },
                        {
                            path: "examgroup/:egid",
                            name: "examgroup",
                            component: () => import("../views/ExamGroup.vue"),
                            meta: {
                                title: "考试",
                            },
                        },
                    ],
                },
            ],
        },
        {
            path: "/admin",
            name: "admin",
            redirect: { name: "manage" },
            component: () => import("../views/Admin.vue"),
            meta: {
                requiresAuth: true,
                requiresAdmin: false,
            },
            children: [
                {
                    path: "upload",
                    name: "upload",
                    component: () => import("../views/Upload.vue"),
                    meta: {
                        title: "上传试卷",
                    },
                },
                {
                    path: "manage",
                    name: "manage",
                    component: () => import("../views/Manage.vue"),
                    meta: {
                        title: "试卷管理",
                    },
                },
                {
                    path: "user",
                    name: "user",
                    component: () => import("../views/User.vue"),
                    meta: {
                        title: "用户管理",
                        requiresAdmin: true,
                    },
                },
                {
                    path: "system",
                    name: "system",
                    component: () => import("../views/System.vue"),
                    meta: {
                        title: "系统管理",
                        requiresAdmin: true,
                    },
                },
            ],
        },
        {
            path: "/:pathMatch(.*)*",
            name: "lost",
            component: () => import("../views/NotFound.vue"),
        },
    ],
});

router.beforeEach((to, from) => {
    if (to.meta.title) {
        document.title = to.meta.title + " - MyEXAM";
    }
    const userStore = useUserStore();

    if (
        to.meta.requiresAuth &&
        userStore.uid &&
        userStore.expires <= new Date().getTime()
    ) {
        userStore.logout();
        return { name: "login" };
    }
    if (to.meta.requiresAuth && !userStore.uid) return { name: "login" };
    if (to.meta.requiresAdmin && !userStore.admin) return { name: "home" };
    if (userStore.uid && ["login", "reg"].includes(to.name))
        return { name: "home" };
});

export default router;
