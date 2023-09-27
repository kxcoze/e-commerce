<!-- Products -->

<template>
    <h1>Hello there!</h1>
    <n-space>
        <n-card v-for="product in productList" :title="product.name" size="large">
            <n-space vertical>
                <div>Цена: {{ product.price }}</div>
                <div>Описание: {{ truncateDescription(product.description) }}</div>
            </n-space>
            <template #action>
                <n-space justify="end">
                    <n-button>Buy me!</n-button>
                </n-space>
            </template>
        </n-card>
    </n-space>
</template>


<script setup>
import { ref } from 'vue'
import { Product } from '../api/products'


const fetchProductList = async () => {
  try {
    return await Product.list()
  } catch (error) {
    console.error(error)
    return []
  }
}

const productList = ref([])

fetchProductList().then(data => {
  productList.value = data
})

const truncateDescription = (description, maxLength = 50) => {
  return description.length > maxLength
    ? description.slice(0, maxLength) + '...'
    : description
}
</script>


<style scoped>
.n-card {
    width: 260px;
    height: 400px;
    margin: 4px;
    padding: 6px;
}

</style>