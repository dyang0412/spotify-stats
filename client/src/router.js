import Vue from 'vue';
import Router from 'vue-router';
import StatSection from './components/StatSection.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: '/',
  routes: [
    {
      path: '/',
      name: 'index',
      component: StatSection,
    },
  ],
});
