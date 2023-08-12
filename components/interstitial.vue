<script setup>
import { inject, ref } from 'vue';
import { onShow } from '@dcloudio/uni-app';

const adUnitId = inject('interstitial');

var loaded = false;
var AdObject = null;

const onadclose = (e) => {
	const detail = e.detail;
	emits('confirm');
};

const onadload = (e) => {
	console.log(e.detail);
	loaded = true;
};

const onaderror = (e) => {
	console.log(e.detail);
};

const query = (callback) => {
	if (!loaded) return callback();
	AdObject.show();
};

onShow(() => {
	if (wx.createInterstitialAd && adUnitId) {
		AdObject = wx.createInterstitialAd({ adUnitId });
		AdObject.onLoad(onadload);
		AdObject.onError(onaderror);
		AdObject.onclose(onadclose);
	}
});

defineExpose({ query });
</script>
