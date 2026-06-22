export type SearchParams = {
    pageNumber: number
    pageSize: number
    activeFlag?: string[]
    searchType?: string
    searchKeyword?: string
    sortColumn?: string
    sortDirection?: string
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
