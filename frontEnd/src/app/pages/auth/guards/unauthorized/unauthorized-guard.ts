import { inject } from '@angular/core'; 
import { CanActivateFn, Router } from '@angular/router';
import { ApiCallingService } from '../../../../services/api/api-calling.service';
import { map, catchError, of } from 'rxjs';

export const unauthorizedGuard: CanActivateFn = (route, state) => {
  const _apiCall = inject(ApiCallingService);
  const _router = inject(Router);

  return _apiCall.postApi('auth/token_validation/', {}).pipe(
    map((res: any) => {
      if (res.data === true) {
        _router.navigate(['/']);
        return false; // Don't allow access to /auth
      }
      return true; // Allow if not logged in
    }),
    catchError((err) => {
      console.error('Auth guard error:', err);
      return of(false);
    })
  );
};