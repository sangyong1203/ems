import fileDownload from 'js-file-download'
import { Message } from '@/shared/composables/useFeedback'
import html2canvas from 'html2canvas'
import failedImage from '@/assets/images/failedImage.svg'
import { dateFormat } from './date.util'
export * from './api.util'
export * from './date.util'

export const REG_EXPS = {

    EMAIL: /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/,

    PASSWORD_CASE_1: /^(?=.*[a-z])(?=.*\d)(?=.*[!@^*_-])[a-z\d!@^*_-]{8,15}$/,

    PASSWORD_CASE_2: /^(?=.*[A-Z])(?=.*\d)(?=.*[!@^*_-])[A-Z\d!@^*_-]{8,15}$/,

    PASSWORD_CASE_3: /^(?=.*[a-z])(?=.*[A-Z])(?=.*[!@^*_-])[a-zA-Z!@^*_-]{8,15}$/,

    PASSWORD_CASE_4: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,15}$/,

    PASSWORD_CASE_5: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@^*_-])[a-zA-Z\d!@^*_-]{8,15}$/,

    MOBILE_PHONE: /^01([0|1|6|7|8|9])-?([0-9]{3,4})-?([0-9]{4})$/,
    // MacAddress
    MAC_ADDRESS: /^([0-9a-fA-F]{2}[:.-]?){5}[0-9a-fA-F]{2}$/g,
    // IPAddress
    IPV4: /^(([1-9]?\d|1\d{2}|2([0-4]\d)|25[0-5])\.){3}([1-9]?\d|1\d{2}|2([0-4]\d)|25[0-5])$/,
} as const


export const base64ToUrl = (vo: any) => {
    return URL.createObjectURL(vo)
}


export const isNumber = (str: string) => {
    const regx = /^[0-9]+$/
    return regx.test(str)
}

/**
 * Null 판단
 * @param {*} value
 */
export const isEmpty = (value: any) => {
    if (
        value == '' ||
        value == null ||
        value == undefined ||
        (value != null && typeof value == 'object' && !Object.keys(value).length)
    ) {
        return true
    } else {
        return false
    }
}
/**
 * Object 복사
 * @param obj
 * @returns
 */
export const cloneObject = (obj: any) => {
    const clone: any = {}
    for (const key in obj) {
        if (typeof obj[key] == 'object' && obj[key] != null) {
            clone[key] = cloneObject(obj[key])
        } else {
            clone[key] = obj[key]
        }
    }

    return clone
}


export const lpad = (str: string, padLen: number, padStr: string | any[]) => {
    if (padStr.length > padLen) return str

    str += ''
    padStr += ''
    while (str.length < padLen) str = padStr + str
    str = str.length >= padLen ? str.substring(0, padLen) : str
    return str
}


export const formatBytes = (byte: number, digit: number = 2) => {
    if (0 === byte) return '0 Bytes'
    const c = 1024
    const unit = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    const f = Math.floor(Math.log(byte) / Math.log(c))
    return parseFloat((byte / Math.pow(c, f)).toFixed(digit)) + ' ' + unit[f]
}

export const getFormatCurrency = (n: number) => {
    if (0 == n) return '0'
    const c = 1000
    const e = ['', 'k', 'm', 'g', 't', 'p', 'e', 'z', 'y']
    const f = Math.floor(Math.log(n) / Math.log(c))
    return parseFloat((n / Math.pow(c, f)).toFixed()) + e[f]
}


export const addComma = (num: { toString: () => string } | undefined) => {
    if (num == undefined) return ''
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

export const formatOrganizationLabel = (enName?: string | null, krName?: string | null) => {
    const normalizedEnName = enName?.trim() ?? ''
    const normalizedKrName = krName?.trim() ?? ''

    if (!normalizedEnName && !normalizedKrName) {
        return '-'
    }

    if (normalizedEnName === normalizedKrName) {
        return normalizedEnName || normalizedKrName
    }

    return `${normalizedEnName} ${normalizedEnName && normalizedKrName ? '/' : ''} ${normalizedKrName}`.trim()
}

export const isMobile = () => {
    const UserAgent = navigator.userAgent

    if (
        UserAgent.match(
            /iPhone|iPod|Android|Windows CE|BlackBerry|Symbian|Windows Phone|webOS|Opera Mini|Opera Mobi|POLARIS|IEMobile|lgtelecom|nokia|SonyEricsson/i,
        ) != null ||
        UserAgent.match(/LG|SAMSUNG|Samsung/) != null
    ) {
        return true
    } else {
        return false
    }
}

export const validatePhoneNumer = (value: string) => {
    if (value == '') {
        return false
    }
    const regex = /^(01[016789])-?\d{3,4}-?\d{4}$/
    const rs = regex.test(value)
    return rs
}

export const validateEmail = (value: string) => {
    if (value == '') {
        return false
    }
    const regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/i
    const rs = regex.test(value)
    console.log('email', rs)
    return rs
}

export const validatePassword = (value: string) => {
    const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{9,16}$/
    const rs = regex.test(value)
    return rs
}


export const getTableSelection = (tableRef: any, val: any[]): any[] => {

    const hasMultiple = Object.keys(tableRef.value?.$attrs).includes('multiple')
    let resData: any = []

    if (hasMultiple) {
        resData = tableRef.value?.getSelectionRows()
    } else {
        if (val.length == 2 && JSON.stringify(val[0]) === JSON.stringify(val[1])) {
            val.forEach((item: any) => {
                tableRef.value?.toggleRowSelection(item, false)
            })
            resData = tableRef.value?.getSelectionRows()
        } else {
            val.forEach((item: any, index) => {
                if (index < val.length - 1) {
                    tableRef.value?.toggleRowSelection(item, false)
                }
            })
        }
        resData = tableRef.value?.getSelectionRows()
    }
    return resData
}


export const excelDownload = (data: any, fileName: string, fileType?:string) => {
    fileDownload(data, `${fileName}_ExcelFile_${dateFormat(new Date(), 'YYYY_MM_DD_HH_mm_ss')}.${fileType ?? 'csv'}`)
}


export const setNewpageSession = () => {

    const user = sessionStorage.getItem('User') ?? ''
    localStorage.setItem('mommoss-user', user)
    setTimeout(() => {
        localStorage.removeItem('mommoss-user')
    }, 1000)
}


export const numberFormatter = (value: string) => {
    if (!value) return ''
    const numbers = value.replace(/\D/g, '')
    return numbers
}

export const phoneFormatter = (value: string) => {
    if (!value) return ''
    const numbers = value.replace(/\D/g, '')
    console.log('phoneFormatter', numbers)

    if (numbers.length <= 3) {
        return numbers
    } else if (numbers.length > 3 && numbers.length <= 6) {
        return numbers.slice(0, 3) + '-' + numbers.slice(3, 6)
    } else if (numbers.length >= 6 && numbers.length <= 10) {
        return numbers.slice(0, 3) + '-' + numbers.slice(3, 6) + '-' + numbers.slice(6)
    } else if (numbers.length === 11) {
        return numbers.slice(0, 3) + '-' + numbers.slice(3, 7) + '-' + numbers.slice(7)
    }
    return numbers
}

export const phoneParse = (value: string) => {
    return value.replace(/-/g, '')
}
// -----------------------------


export const indexMethod = (rowSize: number, page: number) => {
    return rowSize * (page - 1) + 1
}

export const indexInverseMethod = (totalCount: number, rowSize: number, page: number, index: number) => {
    return totalCount - rowSize * (page - 1) - index
}


export const pngDownload = (element: HTMLElement) => {
    element &&
        html2canvas(element, { backgroundColor: '#161616', useCORS: true }).then(canvas => {
            const imgData = canvas.toDataURL('image/png')
            const link = document.createElement('a')
            link.href = imgData
            link.download = 'downloaded_png_file.png'
            link.click()
        })
}


export const copyContext = (row: any, column: any, cell: HTMLTableCellElement, event: Event) => {
    event.preventDefault()
    navigator.clipboard.writeText(row[column.property])
    Message.success('Copy successed!')
}

export const onImageError = (event: any) => {
    event.target.src = failedImage
}


export const clearIntervals = (timers: number[]) => {
    for (const item of timers) {
        clearInterval(item)
    }
}

export const fieldValidationMessages = (fields: any) => {
    for (const key in fields) {
        Message.error(fields[key][0].message ?? '')
    }
}

export const getValueByKey = (list: any[], key: string, value: string) => {
    const item = list.find(item => item[key] === value)
    return item ? item : null
}

export const getFileType = (fileName: string) => {
    const extension = fileName.split('.').pop()?.toLowerCase()
    switch (extension) {
        case 'jpg':
        case 'jpeg':
        case 'png':
        case 'gif':
            return 'image/' + extension
        case 'pdf':
            return 'application/pdf'
        case 'doc':
        case 'docx':
            return 'application/msword'
        default:
            return 'application/octet-stream'
    }
}


