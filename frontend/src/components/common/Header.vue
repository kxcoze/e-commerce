<template> 
  <n-layout-header bordered>
    <n-button text @click="router.go(0)">
      <icon type="refresh" size="20" :depth="2" />
    </n-button>
    <n-breadcrumb>
      <n-breadcrumb-item>
        <router-link :to="{ name: 'home' }">
          E-commerce
        </router-link> 
      </n-breadcrumb-item>
      <n-breadcrumb-item>
        <router-link :to="{ name: 'products' }">
          Products
        </router-link>
      </n-breadcrumb-item>
    </n-breadcrumb>

    <n-space :size="20" align="center" style="line-height: 1">
      <n-tooltip>
        <template #trigger>
          <!-- <router-link :to="{ name: 'about' }">
            <icon type="help" size="22" :depth="2" />
          </router-link> -->
          <icon type="cart" size="22" :depth="2" />
        </template>
        Your cart
      </n-tooltip>


      <n-popover trigger="click" placement="bottom-end" :width="300">
        <template #trigger>
          <n-badge dot processing>
            <icon type="notifications" size="22" :depth="2" />
          </n-badge>
        </template>
        <n-tabs type="line" justify-content="space-evenly" style="--pane-padding: 0">
          <n-tab-pane name="notifications" tab="Notifications (5)">
            <n-list style="margin: 0">
              <n-list-item v-for="i in 5" :key="i"> Notification {{ i }} </n-list-item>
            </n-list>
          </n-tab-pane>
          <n-tab-pane name="messages" tab="Messages (6)">
            <n-list style="margin: 0">
              <n-list-item v-for="i in 6" :key="i"> Message {{ i }} </n-list-item>
            </n-list>
          </n-tab-pane>
        </n-tabs>
      </n-popover>
      
      <n-dropdown :options="options">
        <n-avatar size="small" round />
      </n-dropdown>
    </n-space>
  </n-layout-header>
</template>

<script setup>
import Icon from '../Icon.vue'
import { h } from 'vue'
import { useRouter, RouterLink } from 'vue-router'


const router = useRouter()

const renderIcon = (icon) => {
  return () => {
    return h(Icon, {type: icon})
  }
}

const options = [
  {
    label: () => h(RouterLink, { to: 'profile' }, 'Profile'),
    key: "profile",
    icon: renderIcon('user')
  }, 
  {
    label: () => h(RouterLink, { to: 'logout' }, 'Logout'),
    key: "logout",
    icon: renderIcon('logout')
  }
];
</script>


<style scoped>
.n-layout-header {
  position: sticky;
  top: 0;
  z-index: 1;
  display: flex;
  align-items: center;
  padding: 9px 18px;
}
.n-button {
  margin-right: 15px;
}
.n-space {
  margin-left: auto;
}
</style>