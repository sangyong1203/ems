import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useNavStore } from './nav.store'

export type Menu = {
    id: number
    parentId: number
    title: string
    path: string
    icon: any
    useYn: string
    children: Menu[]
}

export const useMenuStore = defineStore(
    'menu',
    () => {
        const data = ref<Menu[]>([])

        const init = () => {
            data.value = []
        }

        const getMenu = (): Menu[] => {
            return data.value
        }

        const setMenu = (arr: Menu[]) => {
            data.value = arr
        }

        const setTempMenu = (userLevel: string) => {
            data.value = tempMenu.filter(menu => menu.userLevel.some(level => level.toLowerCase() === userLevel.toLowerCase()))
        }

        const searchRecursive = (items: Menu[], path: string) => {
            const nav: Array<{ name: string; path: string }> = []
            items.forEach((item: Menu) => {
                if (item.path === path) {
                    nav.push({ name: item.title, path: item.path })
                } else if (item.children) {
                    const ids = searchRecursive(item.children, path)
                    if (ids.length) {
                        nav.push({ name: item.title, path: item.path })
                        ids.forEach(itemA => nav.push({ name: itemA.name, path: itemA.path }))
                    }
                }
            })
            return nav
        }

        const handleClickMenu = (path: string, menu: Menu[]) => {
            const navStore = useNavStore()
            navStore.setNav(searchRecursive(menu, path))
            navStore.setRoute(path)
        }

        return {
            data,
            init,
            getMenu,
            setMenu,
            setTempMenu,
            handleClickMenu,
        }
    },
    { persist: true },
)

const tempMenu = [
    {
        id: 10,
        parentId: 1,
        title: '대시보드',
        path: '/dashboard',
        icon: 'IconDashboard',
        useYn: 'Y',
        userLevel: ['PLATFORM_ADMIN'],
        children: [],
    },
    {
        id: 20,
        parentId: 1,
        title: '태양광',
        path: '/solar',
        icon: 'IconSolar',
        useYn: 'Y',
        userLevel: ['PLATFORM_ADMIN'],
        children: [],
    },
    {
        id: 30,
        parentId: 1,
        title: 'ESS',
        path: '/ess',
        icon: 'IconEss',
        useYn: 'Y',
        userLevel: ['PLATFORM_ADMIN'],
        children: [],
    },
    {
        id: 40,
        parentId: 1,
        title: '전력 흐름',
        path: '/power-flow',
        icon: 'IconPowerFlow',
        useYn: 'Y',
        userLevel: ['PLATFORM_ADMIN'],
        children: [],
    },
    {
        id: 50,
        parentId: 1,
        title: '트렌드',
        path: '/trend',
        icon: 'IconTrend',
        useYn: 'Y',
        userLevel: ['PLATFORM_ADMIN'],
        children: [],
    },
    {
        id: 60,
        parentId: 1,
        title: '장비 관리',
        path: '/device-management',
        icon: 'IconDeviceManagement',
        useYn: 'Y',
        userLevel: ['PLATFORM_ADMIN'],
        children: [],
    },
    {
        id: 70,
        parentId: 1,
        title: '정비 관리',
        path: '/maintenance-management',
        icon: 'IconMaintenance',
        useYn: 'Y',
        userLevel: ['PLATFORM_ADMIN'],
        children: [],
    },
    {
        id: 80,
        parentId: 1,
        title: '알림 이력',
        path: '/alarm-history',
        icon: 'IconAlarmHistory',
        useYn: 'Y',
        userLevel: ['PLATFORM_ADMIN'],
        children: [],
    },
    {
        id: 90,
        parentId: 1,
        title: '운전 리포트',
        path: '/operation-report',
        icon: 'IconOperationReport',
        useYn: 'Y',
        userLevel: ['PLATFORM_ADMIN'],
        children: [],
    },
    {
        id: 100,
        parentId: 1,
        title: '설정',
        path: '/settings',
        icon: 'IconSetting',
        useYn: 'Y',
        userLevel: ['PLATFORM_ADMIN'],
        children: [],
    },
]
