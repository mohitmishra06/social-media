import { inject } from '@angular/core'; 
import { CanActivateFn, Router } from '@angular/router';
import { ApiCallingService } from '../../../../services/api/api-calling.service';
import { map, catchError, of } from 'rxjs';

export const userAuthGuard: CanActivateFn = (route, state) => {
  const _apiCall = inject(ApiCallingService);
  const _router = inject(Router);

  return _apiCall.postApi('auth/token_validation/', {}).pipe(
    map((res: any) => {
      if (res.data === false) {
        _router.navigate(['/auth']);
        return false; // Don't allow access to /auth
      }
      // You can check response here and return true/false accordingly
      return res.data === true;  // or just `true` if token valid
    }),
    catchError((err) => {
      console.error('Auth guard error:', err);
      _router.navigate(['/auth']);
      return of(false);
    })
  );
};