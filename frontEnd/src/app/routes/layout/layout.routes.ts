import { Routes } from '@angular/router';
import { LayoutComponent } from '../../components/layout/layout';
export const layout_routes: Routes = [
  {
    path:'', 
    component: LayoutComponent,
    children:[
      {
        path:'dashboard',
        // loadChildren: () => import('../dashboard/dashboard.routes').then(m => m.dashboard_routes)
        loadComponent:() => import('../../pages/dashboard/dashboard').then(m => m.Dashboard)
      },
      {
        path:'profile/:id',
        loadComponent: () => import('../../pages/profile/profile').then(m => m.Profile)
      }
    ]
  }
];