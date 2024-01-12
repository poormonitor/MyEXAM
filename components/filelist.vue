<script setup>
import { ref, inject, onMounted } from 'vue';
import { file_types } from '../const.js';

const props = defineProps(['files', 'fid']);
const data = ref(null);
const downloadObject = ref(null);
const loading = inject('loading');
const rewardRef = inject('rewardRef');

const checkIsAllowed = (fid) => {
	rewardRef.value.query(() => {
		previewFile(fid);
	});
};

const previewFile = (fid) => {
	loading.value = true;
	uni.request({
		url: 'https://exam.techo.cool/api/list/url',
		data: { fid: fid }
	})
		.then((response) => {
			return uni.downloadFile({
				url: response.data.url
			});
		})
		.then((result) => {
			return uni.saveFile({
				tempFilePath: result.tempFilePath
			});
		})
		.then((result) => {
			return uni.openDocument({
				filePath: result.savedFilePath,
				showMenu: true
			});
		})
		.finally(() => {
			loading.value = false;
		});
};

data.value = props.files;
onMounted(() => {
	uni.pageScrollTo({
		selector: '#' + props.fid
	});
});
</script>

<template>
	<view class="flex flex-col gap-4">
		<view v-for="file in data">
			<view @click.stop="checkIsAllowed(file.fid)">
				<text
					class="text-base"
					:class="props.fid === file.fid ? 'text-purple' : 'text-red'"
					:id="file.fid"
				>
					{{ file.name }}
				</text>
				<view>
					<text class="text-sm text-gray">
						{{ file_types[file.type] }}
					</text>
					<text class="text-sm text-gray ml-8">
						{{ file.views }}次下载
					</text>
				</view>
			</view>
		</view>
	</view>
</template>
