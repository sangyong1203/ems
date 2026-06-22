export const isSuccessResponse = (result?: string) => {
    return String(result ?? '').toUpperCase() === 'SUCCESS'
}

export const getActionClass = (classList: string[]) => {
    const action = ['GET', 'POST', 'PUT', 'DELETE']
    let result = ''
    action.forEach(act => {
        for (const idx in classList) {
            if (classList[idx] == act) {
                result = act
                break
            }
        }
    })
    return result
}

export const createQueryString = (params: any) => {
    const parts: string[] = []
    const encodeKey = (key: string) =>
        encodeURIComponent(key).replace(/%2E/g, '.')
    const appendPart = (key: string, value: unknown) => {
        if (value === undefined || value === null) {
            return
        }

        parts.push(`${encodeKey(key)}=${encodeURIComponent(String(value))}`)
    }

    for (const key in params) {
        if (Object.prototype.hasOwnProperty.call(params, key)) {
            const value = params[key]

            if (Array.isArray(value)) {
                value.forEach((item, index) => {
                    if (item != null && typeof item === 'object') {
                        Object.entries(item).forEach(([fieldKey, fieldValue]) => {
                            appendPart(`${key}[${index}].${fieldKey}`, fieldValue)
                        })
                        return
                    }

                    appendPart(key, item)
                })
            } else if (value != null && typeof value === 'object') {
                Object.entries(value).forEach(([fieldKey, fieldValue]) => {
                    appendPart(`${key}[${fieldKey}]`, fieldValue)
                })
            } else {
                appendPart(key, value)
            }
        }
    }

    return parts.join('&')
}
