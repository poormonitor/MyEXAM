<script setup>
import { ref, inject } from 'vue';
import { GetYearMonth } from '../../func';
import { courses, grades } from '../../const';

const props = defineProps(['nid']);
const data = ref(null);
const examgroups = ref(null);
const cnt = ref(0);
const page = ref(1);
const loading = inject('loading');

const gotoExamGroup = (egid) => {
	uni.navigateTo({
		url: '/pages/examgroup/examgroup?egid=' + egid
	});
};

const goRequest = () => {
	loading.value = true;
	uni.request({
		url: 'https://exam.techo.cool/api/list/union',
		data: { nid: props.nid },
		success: (response) => {
			if (response.data.union) data.value = response.data.union;
		}
	});
	uni.request({
		url: 'https://exam.techo.cool/api/list/examgroups',
		data: { nid: props.nid },
		success: (response) => {
			if (response.data.examgroups) {
				examgroups.value = response.data.examgroups;
				cnt.value = response.data.count;
				loading.value = false;
			}
		}
	});
};

if (props.nid) {
	goRequest();
} else {
	uni.switchTab({
		url: '/pages/index/index'
	});
}
</script>

<template>
	<view class="p-30" v-if="data">
		<view class="flex justify-between">
			<view id="title" class="mb-30">
				<view class="text-2xl text-bold mb-8">{{ data.name }}</view>
				<view class="mb-10" v-if="data.member">
					<uni-tag
						type="error"
						class="mr-3 mb-3"
						:text="tag"
						v-for="tag in data.member.split(' ')"
					></uni-tag>
				</view>
				<view class="text-sm">{{ data.views }} 浏览</view>
			</view>
			<!--  #ifdef MP -->
			<view class="pt-6">
				<button open-type="share" size="mini" type="info">分享</button>
			</view>
			<!--  #endif -->
		</view>
		<view>
			<view v-for="eg in examgroups">
				<uni-card @click="gotoExamGroup(eg.egid)" :is-full="true">
					<view class="py-8 px-4">
						<view class="text-bold text-xl text-black mb-12">
							{{ GetYearMonth(eg.date) + ' ' + eg.name }}
						</view>
						<view v-for="i in Object.keys(eg.courses)">
							<text class="mb-6 mr-10 text-black">
								{{ grades[i] }}
							</text>
							<uni-tag
								class="mr-3 mb-3"
								type="error"
								:text="courses[e[0]]"
								v-for="e in eg.courses[i]"
							></uni-tag>
						</view>
					</view>
				</uni-card>
			</view>
		</view>
		<view class="mx-30 mt-20">
			<uni-pagination :total="cnt" v-model="page" @change="goRequest" />
		</view>
	</view>
</template>
