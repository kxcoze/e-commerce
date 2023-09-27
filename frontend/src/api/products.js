import { HTTP } from './common.js'


export const Product = {
    list() {
        return HTTP.get('/products/').then(response => {
            return response.data
        })
    },
    get(product) {
        return HTTP.get(`/product/${product.id}`).then(response => {
            return response.data
        })
    }
}