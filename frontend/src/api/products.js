import { HTTP } from './common.js'


export const Product = {
    async list() {
        const response = await HTTP.get('/products/')
        return response.data
    },
    async get(product) {
        const response = await HTTP.get(`/product/${product.id}`)
        return response.data
    }
}