<script setup>
import { ref, watch, inject } from 'vue';
import { onShow } from '@dcloudio/uni-app';
import { grades, courses } from '../../const.js';
import { GetYearMonth } from '../../func.js';
import filelist from '../../components/filelist.vue';
import Empty from '../../components/empty.vue';

const carts = inject('carts');
const last = ref([]);
const loading = inject('loading');
const data = ref([]);
const loadingDialog = ref(null);
const alertDialog = ref(null);

onShow(() => {
	let current = carts.get();
	if (!current.every((e) => last.value.includes(e))) goQuery();
	else data.value = data.value.filter((item) => current.includes(item.pid));
});

const gotoExam = (eid, pid) => {
	uni.redirectTo({
		url: '/pages/exam/exam?eid=' + eid + '&pid=' + pid
	});
};

const goQuery = () => {
	if (!carts.length()) return;
	loading.value = true;
	uni.request({
		url: 'https://exam.techo.cool/api/list/papers',
		method: 'POST',
		data: { pids: [...carts.get()] },
		success: (response) => {
			last.value = [...carts.get()];
			data.value = response.data.list;
			loading.value = false;
		}
	});
};

const removeItem = (pid) => {
	carts.remove(pid);
	data.value = data.value.filter((item) => item.pid != pid);
};

const cleanItem = () => {
	carts.clean();
	data.value = [];
	last.value = [];
};
</script>

<template>
	<uni-popup ref="alertDialog" type="dialog">
		<uni-popup-dialog
			type="warn"
			cancelText="取消"
			confirmText="好的"
			title="确认清空"
			content="确认要清空收藏？操作不可撤销"
			@confirm="cleanItem"
		></uni-popup-dialog>
	</uni-popup>
	<div class="mt-20 flex justify-center items-center" v-if="data.length">
		<div class="mx-20 mb-4 text-center">
			<span>共计收藏了</span>
			<span class="mx-2">{{ carts.length() }}</span>
			<span>张试卷</span>
		</div>
		<view>
			<button size="mini" type="info" @click="alertDialog.open()">
				清空
			</button>
		</view>
	</div>
	<div class="mx-20 mt-20" v-if="data.length">
		<uni-card
			:is-full="true"
			@click="gotoExam(item.exam.eid, item.pid)"
			v-for="item in data"
		>
			<view class="flex justify-between mb-8">
				<view>
					<view class="flex gap-8 text-base text-black">
						<text>{{ item.union.name }}</text>
						<text>
							{{ GetYearMonth(item.examgroup.date) }}
							{{ item.examgroup.name }}
						</text>
						<view>
							{{ grades[item.exam.grade] }}
							{{ courses[item.exam.course] }}
						</view>
					</view>
					<view class="flex gap-15">
						<text>{{ item.owner }}</text>
						<text v-if="item.comment">{{ item.comment }}</text>
						<text>{{ item.files.length }} 份文件</text>
					</view>
				</view>
			</view>
			<view class="flex justify-between">
				<filelist :files="item.files" />
				<view>
					<button size="mini" @click="removeItem(item.pid)">
						删除
					</button>
				</view>
			</view>
		</uni-card>
	</div>
	<view v-else-if="!carts.length()">
		<Empty />
	</view>
</template>
