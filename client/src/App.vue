<template>
  <div>
    
    <router-view/>
  </div>
</template>

<script>
import StatSection from './components/StatSection.vue'
import SearchBar from './components/SearchBar.vue'
export default {
  components: {
    appStatSection: StatSection,
    appSearchBar: SearchBar
  }
}
</script>

<style>
*{
    position: relative;
    margin: 0;

    box-sizing: border-box
  }

  html, body{
    display: grid;
    height: 100%;
    width: 100%;
    scroll-behavior: smooth;
    -webkit-text-size-adjust: 100%;
    -webkit-font-smoothing: antialiased
  }


</style>
