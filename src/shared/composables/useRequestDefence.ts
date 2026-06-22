import { ref } from 'vue'

const requestCount = ref(0)
const startRequestTime = ref(Date.now())
const limitDuration = ref(5000)
const isWaiting = ref(false)
const maxRequestCount = ref(100)

const addRequestCount = () => {
    requestCount.value += 1
}

const initRequestCount = () => {
    requestCount.value = 0
    startRequestTime.value = Date.now()
}

const getRequestDurationTime = () => Date.now() - startRequestTime.value

const setLimitDurationTime = (milliseconds: number) => {
    limitDuration.value = milliseconds
}

const isOverRequest = () => {
    addRequestCount()
    const requestDurationTime = getRequestDurationTime()

    if (requestCount.value >= maxRequestCount.value && requestDurationTime <= limitDuration.value) {
        isWaiting.value = true
        setTimeout(() => {
            initRequestCount()
            isWaiting.value = false
        }, limitDuration.value)
    } else if (requestDurationTime > limitDuration.value) {
        initRequestCount()
    }

    return isWaiting.value
}

export const useRequestDefence = () => {
    return {
        maxRequestCount,
        isOverRequest,
        setLimitDurationTime,
    }
}
