

const mainRoutes = [
    {
        name: 'home',
        path: '/',
        component: () => import('../views/Home.vue')
    },
    {
        name: 'products',
        path: '/products',
        component: () => import('../views/Products.vue')
    },
    {
        name: 'profile',
        path: '/profile',
        component: () => import('../views/Profile.vue')
    }
]



const routes = [
    {
        name: 'layout',
        path: '/',
        component: () => import('../components/Index.vue'),
        children: [...mainRoutes]
    }
]




export default routes
