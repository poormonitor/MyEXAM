<script setup>
import { provide, ref, watch, computed } from 'vue';
import { onLaunch } from '@dcloudio/uni-app';

const reward = '';
const interstitial = '';
const s = ref('');
const cart = ref([]);
const left = ref(0);
const lefttotal = 2;
const loading = ref(false);

const lefts = {
	reduce: function () {
		if (left.value == 0) return false;
		left.value -= 1;
		return true;
	},
	reset: function () {
		left.value = lefttotal;
	},
	length: function () {
		return left.value;
	}
};

const carts = {
	add: function (id) {
		if (cart.value.length >= 100) {
			uni.showToast({
				title: '最多收藏100个',
				icon: 'error',
				duration: 2000
			});
		} else {
			cart.value.push(id);
			this.update();
		}
	},
	remove: function (id) {
		cart.value = cart.value.filter((item) => item != id);
		this.update();
	},
	has: function (id) {
		return cart.value.includes(id);
	},
	get: function () {
		return cart.value;
	},
	clean: function () {
		cart.value = [];
		this.update();
	},
	update: function () {
		uni.setStorageSync('myexam_cart', cart.value);
	},
	fetch: function () {
		cart.value = uni.getStorageSync('myexam_cart') || [];
	},
	length: function () {
		return cart.value.length;
	}
};

provide('s', s);
provide('lefts', lefts);
provide('carts', carts);
provide('loading', loading);
provide('interstitial', interstitial);
provide('reward', reward);

watch(loading, (val) => {
	if (val) uni.showLoading({ title: '加载中' });
	else setTimeout(() => uni.hideLoading(), 200);
});

onLaunch(carts.fetch);
</script>

<style lang="scss">
@import './styles/generate.scss';
@import './styles/expand.scss';

.underline {
	text-decoration: underline;
}

page {
	background-color: #fafafa;
}

.whitespace-nowrap {
	white-space: nowrap;
}

button[type='info'] {
	color: #fff;
	background-color: #a11326;
}

button[type='info']:hover {
	background-color: #7f0f1d;
}
</style>
