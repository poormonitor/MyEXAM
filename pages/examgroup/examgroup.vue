<script setup>
import { ref, inject } from 'vue';
import { GetYearMonth } from '../../func';
import { courses, grades } from '../../const';

const props = defineProps(['egid']);
const data = ref(null);
const loading = inject('loading');

const gotoExam = (eid) => {
	uni.navigateTo({
		url: '/pages/exam/exam?eid=' + eid
	});
};

const gotoUnion = (nid) => {
	uni.navigateTo({
		url: '/pages/union/union?nid=' + nid
	});
};

const previewAssign = (aid) => {
	loading.value = true;
	uni.request({
		url: 'https://exam.techo.cool/api/list/assign_url',
		data: { aid: aid },
		success: (response) => {
			if (response.data.url) {
				loading.value = false;
				uni.previewImage({
					urls: [response.data.url]
				});
			}
		}
	});
};

if (props.egid) {
	loading.value = true;
	uni.request({
		url: 'https://exam.techo.cool/api/list/examgroup',
		data: { egid: props.egid },
		success: (response) => {
			if (response.data.examgroup) data.value = response.data.examgroup;
			loading.value = false;
		}
	});
} else {
	uni.switchTab({
		url: '/pages/index/index'
	});
}
</script>

<template>
	<view class="p-30" v-if="data">
		<view class="flex justify-between">
			<view id="title" class="mb-20">
				<view
					class="text-xl text-red mb-3 flex items-start"
					@click="gotoUnion(data.union.nid)"
				>
					<text>{{ data.union.name }}</text>
					<image
						src="../../static/icons8-share-24.png"
						style="width: 16px; height: 16px"
						mode="scaleToFill"
						class="ml-4"
					></image>
				</view>
				<view class="text-2xl text-bold mb-2">
					{{ GetYearMonth(data.date) }} {{ data.name }}
				</view>
				<view class="text-sm">{{ data.views }} 浏览</view>
			</view>
			<!--  #ifdef MP -->
			<view class="pt-30">
				<button open-type="share" size="mini" type="info">分享</button>
			</view>
			<!--  #endif -->
		</view>
		<view v-if="data.assigns.length">
			<view class="text-center text-bold mb-16">赋分表</view>
			<view v-for="item in data.assigns">
				<uni-card @click="previewAssign(item.aid)">
					<view class="py-4">
						<view class="text-bold text-xl text-black mb-4">
							{{ item.comment }}
						</view>
						<text class="mr-10">
							{{ item.upload_time.replace('T', ' ') }}
						</text>
						<text>{{ item.views }} 浏览</text>
					</view>
				</uni-card>
			</view>
		</view>
		<view>
			<view class="text-center text-bold mb-12">考试列表</view>
			<view v-for="item in data.exams">
				<uni-card @click="gotoExam(item.eid)">
					<view class="py-4">
						<view class="text-bold text-xl text-black mb-4">
							{{ grades[item.grade] }} {{ courses[item.course] }}
						</view>
						<text class="mr-10">{{ item.date }}</text>
						<text>{{ item.views }} 浏览</text>
					</view>
				</uni-card>
			</view>
		</view>
	</view>
</template>
