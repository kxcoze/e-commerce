<template>
    <n-layout position="absolute">  
      <Header/>
      <Content/>
      <Footer/>
    </n-layout>
  </template>
  
  
  <script setup>
    import Header from './common/Header.vue'
    import Content from './common/Content.vue'
    import Footer from './common/Footer.vue'
  </script>