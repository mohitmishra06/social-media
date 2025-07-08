import { Routes } from '@angular/router';
import { userAuthGuard } from './pages/auth/guards/authorized/user-auth-guard';
import { unauthorizedGuard } from './pages/auth/guards/unauthorized/unauthorized-guard';

export const routes: Routes = [
    {
        path:'',
        loadChildren: () => import('./routes/layout/layout.routes').then(m => m.layout_routes),
        canActivate:[userAuthGuard]
    },
    { 
        path: 'auth',
        loadChildren: () => import('./routes/auth.routes').then(m => m.auth_routes),
        canActivate: [unauthorizedGuard] // ✅ This guard now protects /auth from logged-in users
    },
];

    