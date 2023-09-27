<template>
  <router-view />
</template>
  
  <script setup>
  import { useLoadingBar } from 'naive-ui'
  import router from '../router'
  
  // todo: route transtion
  
  const loadingBar = useLoadingBar()
  
  router.beforeEach(() => loadingBar?.start())
  
  router.afterEach(() => loadingBar?.finish())
  </script>