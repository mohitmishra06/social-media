import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthComponent } from '../pages/auth/auth';
import { LoginComponent } from '../pages/auth/login/login';
import { RegisterComponent } from '../pages/auth/register/register';
import { ForgotPasswordComponent } from '../pages/auth/forgot-password/forgot-password';
import { ChangePasswordComponent } from '../pages/auth/change-password/change-password';
import { OtpValidatorComponent } from '../pages/auth/otp-validator/otp-validator';

export const auth_routes: Routes = [
  { 
    path: '',
    component: AuthComponent,
    children:[
      {
        path:'',
        component:LoginComponent
      },
      {
        path:'sign-up',
        component:RegisterComponent,
      },
      {
        path:'otp-validator/:email',
        component:OtpValidatorComponent,
      },
      {
        path:'forgot-password',
        component:ForgotPasswordComponent
      },
      {
        path:'change-password/:id',
        component:ChangePasswordComponent
      },
    ]
  }
];