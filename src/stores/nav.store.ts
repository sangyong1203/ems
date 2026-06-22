import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'

export const useNavStore = defineStore(
    'nav',
    () => {
        const router = useRouter()
        const data: any = ref({
            authAction: [],
            nav: [],
            route: '',
        })
        const init = () => {
            data.value = {
                authAction: [],
                nav: [],
                route: '',
            }
        }
        const getNav = () => {
            return data.value.nav
        }

        const setNav = (nav: Array<{ name: string; path: string; data?: any }>) => {
            data.value.nav = nav
        }

        const getRoute = () => {
            return data.value.route
        }

        const setRoute = (route: string) => {
            data.value.route = route
        }

        const getAuthAction = (): string[] => {
            return data.value.authAction
        }

        const setAuthAction = (items: any, path: string) => {
            items.forEach((item: any) => {
                if (item.path === path) {
                    const action = item.authAction.split(',')
                    data.value.authAction = action
                } else if (item.children) {
                    setAuthAction(item.children, path)
                }
            })
        }

        const navTo = (name: string, path: string, data?: any) => {
            const nav = getNav()
            console.log('navTo', nav, name)
            if (nav.length === 0 || nav.at(-1).name !== name) {
                nav.push({ name: name, path: path, data: data })
                setNav(nav)
                setRoute(path)
            }
            router.push(path)
        }

        const backTo = () => {
            const nav = getNav()
            if (nav.length > 2) {
                nav.pop()
                setNav(nav)
                router.back()
            }
        }
        const getNavData = () => {
            let param = null
            if (data.value.nav.length > 1) {
                param = data.value.nav.at(-1)?.data
            }
            return param
        }
        return {
            data,
            init,
            getNav,
            setNav,
            getRoute,
            setRoute,
            getAuthAction,
            setAuthAction,
            navTo,
            backTo,
            getNavData,
        }
    },
    {
        persist: true,
    },
)
