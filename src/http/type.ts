export type PathVariables = { 
    [key: string]: any 
}
export type Params = { 
    [key: string]: any 
}

export type PayloadModel = {
    path?: any
    query?: any
    body?: any
}

export type APIResponse<T = any> = {
    result: string
    resultMessage: string 
    data: T
}
