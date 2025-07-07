import { createRouter, createWebHistory } from 'vue-router';
import CreatePage from '../pages/CreatePage.vue';
import ViewPage from '../pages/ViewPage.vue';
import ArchivePage from '../pages/ArchivePage.vue';

const router = createRouter(
  {
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
      {
        path: '/',
        name: 'create',
        component: CreatePage,
      },
      {
        path: '/:uuid',
        name: 'view',
        component: ViewPage,
        props: true,
      },
      {
        path: '/archive/',
        name: 'archive',
        component: ArchivePage,
      },
    ],
  }
);

export default router;
