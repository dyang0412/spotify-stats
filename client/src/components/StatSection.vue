<template>
    <div class="stat-page">
        <app-search-bar></app-search-bar>
    </div>
</template>

<script>
import SearchBar from './SearchBar.vue'
export default {
   components:{
       appSearchBar: SearchBar
   }
}
</script>

<style scoped>
    .stat-page{
        background-color: rgb(20, 19, 19);;
        min-height: 100vh;
        min-width: 100%;
    }
</style>