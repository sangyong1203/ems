import { ElMessage, ElMessageBox, ElNotification } from 'element-plus'
import type { Action } from 'element-plus'


export const Message = {
    success(message: string) {

        ElMessage({
            message: message,
            type: 'success',
            placement: 'bottom',
        })
    },
    warning(message: string) {
        ElMessage({
            message: message,
            type: 'warning',
            placement: 'bottom',
        })
    },
    error(message: string) {

        ElMessage({
            message: message,
            type: 'error',
            placement: 'bottom',
        })
    },
    info(message: string) {

        ElMessage({
            message: message,
            type: 'info',
            placement: 'bottom',
        })
    },
}


export const Notification = {
    success(message: string, title?: string) {

        ElNotification({
            title: title ?? 'Success',
            message: message,
            position: 'top-right',
            type: 'success',
            duration: 3000,
        })
    },
    warning(message: string, title?: string) {
        ElNotification({
            title: title ?? 'Warning',
            message: message,
            position: 'top-right',
            type: 'warning',
            duration: 3000,
        })
    },
    error(message: string, title?: string) {

        ElNotification({
            title: title ?? 'Error',
            message: message,
            position: 'top-right',
            type: 'error',
            duration: 3000,
        })
    },
    info(message: string, title?: string) {

        ElNotification({
            title: title ?? 'Note',
            message: message,
            position: 'top-right',
            type: 'info',
            duration: 3000,
        })
    },
}


export const useGlobalDialog = (
    message: string,
    title: string,
    type: 'CONFIRM_YN' | 'YN' | 'OK',
    options?: {
        confirmButtonText?: string
        cancelButtonText?: string
    },
) => {

    let doConfirm: any = () => {}
    const onConfirm = (callback: () => void) => {
        doConfirm = callback
        return dialog
    }

    let docancel: any = () => {}
    const onCancel = (callback: () => void) => {
        docancel = callback
        return dialog
    }

    let doClose: any = () => {}
    const onClose = (callback: () => void) => {
        doClose = callback
        return dialog
    }

    if (type === 'CONFIRM_YN') {
        ElMessageBox.confirm(message, title, {
            confirmButtonText: (options && options.confirmButtonText) ?? 'Confirm',
            cancelButtonText: (options && options.cancelButtonText) ?? 'Cancel',
            distinguishCancelAndClose: true,
            closeOnClickModal: false,
            callback: (action: Action) => {
                action == 'confirm' ? doConfirm() : action == 'cancel' ? docancel() : doClose()
            },
        })
    }
    if (type === 'YN') {
        ElMessageBox.confirm(message, title, {
            confirmButtonText: (options && options.confirmButtonText) ?? 'Yes',
            cancelButtonText: (options && options.cancelButtonText) ?? 'No',
            distinguishCancelAndClose: true,
            closeOnClickModal: false,
            callback: (action: Action) => {
                action == 'confirm' ? doConfirm() : action == 'cancel' ? docancel() : doClose()
            },
        })
    }
    if (type === 'OK') {
        ElMessageBox.confirm(message, title, {
            confirmButtonText: (options && options.confirmButtonText) ?? 'Ok',
            showCancelButton: false,
            showClose: false,
            callback: () => {
                doConfirm()
            },
        })
    }
    const dialog = {
        onConfirm,
        onCancel,
        onClose,
    }

    return dialog
}
