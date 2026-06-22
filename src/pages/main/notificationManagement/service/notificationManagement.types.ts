import type { APIResponse } from '@/http/type'

export type TemplateList = {
    id: number
    type: string
    title: string
    activeFlag: string[]
    updatedAt: string
}

export type TemplateItem = {
    id: number
    type: string
    typeId?: number
    title: string
    body?: string
    activeFlag: string[]
    updatedAt: string
}

export type TemplateType = {
    id: number
    type: string
    description: string
}

export type SearchParams = {
    pageNumber: number
    pageSize: number
    activeFlag?: string[]
    searchType?: string
    searchKeyword?: string
    sortColumn?: string
    sortDirection?: string
}

export type TemplateListResponse = Omit<APIResponse, 'data'> & {
    data: {
        list: TemplateList[]
        totalCount: number
    }
}

export type TemplateDetailResponse = Omit<APIResponse, 'data'> & {
    data: TemplateItem | null
}

export type TemplateTypesResponse = Omit<APIResponse, 'data'> & {
    data: TemplateType[]
}
