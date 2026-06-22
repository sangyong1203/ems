<template>
    <div class="time">
        <span class="time-lable">{{ props.label }} : </span>
        <span class="time-value">{{ currentTime }}</span>
        <span class="time-value time-second">{{ currentSecond }}</span>
    </div>
</template>
<script lang="ts" setup>
import dayjs from 'dayjs'
import { ref, onBeforeUnmount } from 'vue'

export interface CurrentTimeProps {
    label: string
}
const props = defineProps<CurrentTimeProps>()
const currentTime = ref(dayjs().format('YYYY-MM-DD HH:mm:'))
const currentSecond = ref(dayjs().format('ss'))
const timer = setInterval(() => {
    currentTime.value = dayjs(new Date()).format('YYYY-MM-DD HH:mm:')
    currentSecond.value = dayjs().format('ss')
}, 1000)
onBeforeUnmount(() => {
    clearInterval(timer)
})
</script>
<style lang="scss" scope>
.time {
    margin: 0 20px;
    font-weight: 500;
}
.time-lable {
    font-size: 16px;
}
.time-value {
    font-size: 17px;
}
.time-second {
    width: 20px;
    display: inline-block;
    text-align: left;
}
</style>
