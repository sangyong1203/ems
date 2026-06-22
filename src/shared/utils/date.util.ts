import dayjs from 'dayjs'
import utc from 'dayjs/plugin/utc'
import timezone from 'dayjs/plugin/timezone'
import { Notification } from '@/shared/composables/useFeedback'

dayjs.extend(utc)
dayjs.extend(timezone)

export const dateFormat = (date: any, format: string) => {
    if (date == null || date == undefined || date == '') {
        return ''
    }

    return dayjs(date).format(format)
}

export const localeDateFormat = (date: any, format: string) => {
    const timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone

    if (date == null || date == undefined || date == '') {
        return '-'
    }

    if (typeof date === 'number') {
        return dayjs(date).tz(timeZone).format(format)
    }

    return dayjs.utc(date).tz(timeZone).format(format)
}

export const dateSelectionLimit = (
    startDate: string,
    endDate: string,
    dateKey: 'year' | 'month' | 'day',
    limit?: number,
) => {
    const stD = dayjs(startDate)
    const enD = dayjs(endDate)
    let limitDate = 0
    let isOverLimit = false

    if (dateKey === 'year') {
        limitDate = limit ? limit : 3
        const duration = enD.diff(stD, 'year')
        if (duration > limitDate) {
            Notification.warning(`최대 ${limitDate}년 이내로 선택해주세요.`)
            isOverLimit = true
        }
    }

    if (dateKey === 'month') {
        limitDate = limit ? limit : 12
        const duration = enD.diff(stD, 'month')
        if (duration > limitDate) {
            Notification.warning(`최대 ${limitDate}개월 이내로 선택해주세요.`)
            isOverLimit = true
        }
    }

    if (dateKey === 'day') {
        limitDate = limit ? limit : 14
        const duration = enD.diff(stD, 'day')
        if (duration > limitDate) {
            Notification.warning(`최대 ${limitDate}일 이내로 선택해주세요.`)
            isOverLimit = true
        }
    }

    return isOverLimit
}

export const getTime = (minuts: number) => {
    const hours = Math.floor(minuts / 60)
    const minutes = Math.floor(minuts % 60)
    const hourStr = hours ? `${String(hours)} hour` : ''
    const minuteStr = `${String(minutes)} min`
    return `${hourStr} ${minuteStr}`
}

export const isDateRangeExceed = (startDate: string, endDate: string, limitDate: number) => {
    const start = dayjs(startDate)
    const end = dayjs(endDate)
    const dif = end.diff(start, 'day')
    return dif > limitDate
}
